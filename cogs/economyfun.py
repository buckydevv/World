from os import environ
from textwrap import dedent
from random import randint
from discord import Embed, Member
from discord.ext.commands import command
from discord.ext import commands
from discord.ext.commands import Cog
from pymongo import MongoClient
from datetime import datetime
from typing import Optional
from PIL import Image, ImageFont, ImageDraw
from framework import Wealth, Misc

class EconomyFunCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.collection = MongoClient(environ["MONGODB_URL"])["Coins"]["UserCoins"]
        self.color = 0x2F3136
        self.items_order = ("coins", "Bank", "cookie", "choc", "apple", "poop", "beans", "pizza", "waffles", "Fish")
        self.badge_urls = ("https://cdn.discordapp.com/emojis/779192872402026516.png", "https://cdn.discordapp.com/emojis/779192938617241600.png", "https://cdn.discordapp.com/emojis/779193003024973835.png")
        self.badges_ctx = { # short name, (Order for "BadgeSlot{number}", price, emoji, full name)
            "noob": (1, 900, "<:WorldBadge1:779192872402026516>", "Noob Badge"),
            "beginner": (2, 3500, "<:WorldBadge2:779192938617241600>", "Beginner Badge"),
            "leader": (3, 9500, "<:WorldBadge3:779193003024973835>", "Leader Badge")
        }
        

    @commands.command(help="Add reputation points to a user.", aliases=["rep"])
    @commands.cooldown(rate=1, per=1800, type=commands.BucketType.member)
    async def reputation(self, ctx, user: Member):
        now = datetime.now()

        if user.id == ctx.author.id:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send(f"Sorry {ctx.author.mention} You cant give yourself a reputation point.")

        if not (Wealth._has_account(user.id)):
            ctx.command.reset_cooldown(ctx)
            return await ctx.send(f"Sorry {ctx.author.mention} that user does not have a World account")

        if not (Wealth._has_account(ctx.author.id)):
            await Wealth._create_account(ctx.author.id)
        last_used = now.strftime("%m/%d/%Y, %H:%M:%S")

        self.collection.update_one({"_id": user.id}, {"$inc": {"Reputation": 1}})
        self.collection.update_one({"_id": ctx.author.id}, {"$set": {
            "TargetMember": user.id,
            "LastUsed": last_used
        }})

        embed = Embed(title="Reputation", description=f"{ctx.author.mention} You added `+1` Reputation to {user.mention}", color=self.color)
        await ctx.send(embed=embed)

    @reputation.error
    async def reputation_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/rep <@user>`")
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"Sorry {ctx.author.mention} This command in on cooldown, Try again in {round(error.retry_after)} seconds.")


    @commands.command(help="Info on your last given rep point.")
    async def repinfo(self, ctx):
        now = datetime.now()

        if not (Wealth._has_account(ctx.author.id)):
            await Wealth._create_account(ctx.author.id)

        if not self.collection.find_one({"_id": ctx.author.id}):
            return await ctx.send(f"Sorry {ctx.author.mention} you havent gave anyone a rep point!\nTry using the command `rep` to give a reputation point to someone you think deserves it.")

        if self.collection.find_one({"_id": ctx.author.id})["LastUsed"] == "Isnotset":
            return await ctx.send(f"Sorry {ctx.author.mention} you havent gave anyone a rep point!\nTry using the command `rep` to give a reputation point to someone you think deserves it.")

        result = self.collection.find_one({"_id": ctx.author.id})
        last_used = result["LastUsed"]
        target_user = result["TargetMember"]

        embed = Embed(
            title="Last Reputation",
            description=f"{ctx.author.mention} You gave <@{target_user}> `1` Reputation point\nDate: `{last_used}`",
            color=self.color
            )
        await ctx.send(embed=embed)
    
    async def profile_canvas(self, user, result): # the function that draws everything
        pfp = await Misc.fetch_pfp(user) # fetch the user pfp
        font = ImageFont.truetype("./fonts/Whitney-Medium.ttf", 30) # epic
        fontm = ImageFont.truetype("./fonts/Whitney-Medium.ttf", 25) # variable
        fontmm = ImageFont.truetype("./fonts/Whitney-Medium.ttf", 20) # naming
        
        main = Image.open("./images/profile_template.png") # get the template
        draw = ImageDraw.Draw(main)
        if pfp.mode != "RGBA":
            main.paste(pfp, (0, 0))
        else:
            main.paste(pfp, (0, 0), pfp) # also transparent for good measure
        
        draw.text((60, 5), user.display_name, font=font, fill=(255, 255, 255)) # draw the user name
        draw.text((10, 60), f"Created at: {Misc.__delayfstr(result['AccountCreated'])} ago\nLast transfer: {Misc.__delayfstr(result['LastTransfer'])} ago\nMarried to: {result['MarriedTo']}\nReputation: {result['Reputation']:,}", font=fontmm, fill=(255, 255, 255))
    
        cursor = 60
        for item in self.items_order:
            width = font.getsize(text)[0]
            draw.text((cursor - width, 555), f"{result[item]:,}", font=fontm, fill=(255, 255, 255))
            cursor += 40

        cursor = 10
        for i in range(3):
            if not result[f"BadgeSlot{i + 1}"].startswith("<:"): # if it has a badge then it's a custom emoji
                continue # doesn't have the badge
            badge_image = await Misc.image_from_url(self.bot, self.badge_urls[i])
            badge_image = badge_image.convert("RGBA").resize((30, 30))
            main.paste(badge_image, (cursor, 260), badge_image)
            cursor += 40
        
        pfp.close()
        del draw, cursor, pfp, font, fontm, fontmm
        return Misc.save_image(main)

    @commands.command()
    async def profile(self, ctx, user: Member=None):
        if not (Wealth._has_account(ctx.author.id)):
            await Wealth._create_account(ctx.author.id)
        user = user or ctx.author
        result = Wealth.mass_fetch(user.id)
        if "--card" in ctx.message.content: # idk how to do this, i suck at default discord.py parsing xd
            ctx.message.content = ctx.message.content.replace("--card", "")
            buffer = await self.profile_canvas(user, result)
            return await ctx.send(file=buffer)

        noob_b, beginner_b, leader_b, marry, bank_, beans, pizza, waffles, fish, coins, rep, afk = Wealth.extract_props(result, ['BadgeSlot1', 'BadgeSlot2', 'BadgeSlot3', 'MarriedTo', "Bank", "beans", "pizza", "waffles", "Fish", "coins", "Reputation", "afk"])
        last_trans, cookie, poop, apple, chocolate, created = Wealth.extract_props(result, ["LastTransfer", "cookie", "poop", "apple", "choc", "AccountCreated"])
        page1 = Embed(title='Page 1/3', description=f"{user}'s Profile", colour=self.color).add_field(name="<:memberlogo:765649915031846912> | Account", value=f"Account Type: `World Account`\nCoins: `{coins}`\nBank: `{bank_}`\nReputation: `{rep}`\nStatus: `{afk}`")
        page2 = Embed(title='Page 2/3', description=f"{user}'s Profile", colour=self.color).add_field(name=":handbag: | Inventory", value=f":cookie: Cookies: `{cookie}`\n:chocolate_bar: Chocbars: `{chocolate}`\n:apple: Apples: `{apple}`\n:poop: Poop: `{poop}`\n<:beanworld:774371828629635132> Beans: `{beans}`\n:pizza: Pizza: `{pizza}`\n:waffle: Waffles `{waffles}`\n:fish: Fish: `{fish}`")
        page3 = Embed(title="Page 3/3", description=f"{user}'s Profile", colour=self.color).add_field(name="<:shufflelogo:765652804387471430> | Other", value=f"Created World Account: `{created}`\nYour Last Transfer: `{last_trans}`\nMarried to: `{marry}`\nBadges:\n{noob_b} Badge\n{beginner_b} Badge\n{leader_b} Badge")
        pages = (page1, page2, page3) #tuplesarejustlightweightarrays
        message = await ctx.send(embed=page1)
        await message.add_reaction('\u23ee')
        await message.add_reaction('\u25c0')
        await message.add_reaction('\u25b6')
        await message.add_reaction('\u23ed')
        await message.add_reaction('\u23F9')
        i, emoji = 0, ""

        while True:
            if emoji == '\u23ee':
                i=0
                await message.edit(embed=pages[i])
            if emoji == '\u25c0':
                if i>0:
                    i-=1
                    await message.edit(embed=pages[i])
            if emoji == '\u25b6':
                if i<2:
                    i+=1
                    await message.edit(embed=pages[i])
            if emoji=='\u23ed':
                i=2
                await message.edit(embed=pages[i])
            if emoji == '\u23F9':
                await message.clear_reactions()
                break

            try:
                res = await self.bot.wait_for('reaction_add', check=lambda r, u: u.id == ctx.author.id and r.message.id == message.id, timeout=10)
            except:
                await message.clear_reactions()
                break
            if not res:
                break
            if res[1].id != 700292147311542282: # use ID instead of user name
                emoji = str(res[0].emoji)

        await message.clear_reactions()


    @commands.command(help="Badge Shop!", aliases=["bshop"])
    async def badgeshop(self, ctx):
        return await ctx.send(embed=Embed(
            title="World Badge Shop!",
            description=dedent("""
                - World Noob
                `Cost 900 Coins!`
                - World Beginner
                `Cost 3,500 Coins!`
                - World Leader
                `Cost 9,500 Coins!`
            """),
            color=self.color
        ))

    @commands.command(help="Buy a World Badge.")
    async def buybadge(self, ctx, item: str):
        if not (Wealth._has_account(ctx.author.id)):
            await Wealth._create_account(ctx.author.id)

        result = Wealth.mass_fetch(ctx.author.id)
        if not self.badges_ctx.get(item.lower()): # the person entered something other than `noob, beginner, leader`
            return await ctx.send(embed=Embed(title="Error!", description=f"Sorry {ctx.author.mention}, please select the correct badge, Badges available: `{', '.join(self.badges_ctx.keys())}`", color=self.color))
        
        order, price, emoji, full_name = self.badges_ctx[item.lower()]
        if result["coins"] < price:
            embed = Embed(title="Error!", description=f"Sorry {ctx.author.mention} You dont have enough coins to buy `World {full_name}`", color=self.color)
            return await ctx.send(embed=embed)
        elif result["BadgeSlot1"] == emoji:
            embed = Embed(title="Error!", description=f"Sorry {ctx.author.mention} You already have `World {full_name}`.", color=self.color)
            return await ctx.send(embed=embed)
        
        await ctx.send(embed=Embed(
            title="World Badge",
            description=f"You have bought `World {full_name}` for `{price:,}` Coins. {emoji}",
            color=self.color
        ))
        self.collection.update_one({"_id": ctx.author.id}, {"$inc": {"coins": -price}})
        self.collection.update_one({"_id": ctx.author.id}, {"$set": {f"BadgeSlot{order}": emoji}})

    @buybadge.error
    async def buybadge_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/buybadge <BadgeName>`")


    @commands.command(help="Marry a specified user!")
    @commands.cooldown(rate=1, per=120, type=commands.BucketType.member)
    async def marry(self, ctx, user: Member):
        now = datetime.now()
        m_date = now.strftime("%m/%d/%Y")

        if not (Wealth._has_account(ctx.author.id)):
            await Wealth._create_account(ctx.author.id)

        if user == ctx.author:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send(f"Sorry {ctx.author.mention} but you can't marry yourself!")

        result = Wealth.mass_fetch(ctx.author.id)
        Marriedto_ = result["MarriedTo"]
        MarriedDate = result["MarriedDate"]

        if result["MarriedTo"] == str(user):
            ctx.command.reset_cooldown(ctx)
            return await ctx.send(embed=Embed(title="Error!", description=f"Sorry {ctx.author.mention} You're already married to `{user}`.", color=self.color))

        if not result["MarriedTo"] == "Nobody":
            ctx.command.reset_cooldown(ctx)
            return await ctx.send(embed=Embed(title="Error!", description=f"Sorry {ctx.author.mention} You're already married.", color=self.color))
        msg = await ctx.send(f"Hey {user.mention} {ctx.author.mention} wants to marry you.\nPlease react.")

        emoji = ''
        await msg.add_reaction('☑')
        await msg.add_reaction('❎')
        try:
            res = await self.bot.wait_for('reaction_add', check=lambda r, u: u.id == user.id and r.message.id == msg.id, timeout=13)
        except:
            await msg.clear_reactions()

        if res[1].id != 700292147311542282: # use ID instead of user name
            emoji=str(res[0].emoji)

        if emoji == "☑":
            self.collection.update_one({"_id": ctx.author.id}, {"$set": {
                "MarriedTo": str(user),
                "MarriedDate": str(m_date)
            }})
            self.collection.update_one({"_id": user.id}, {"$set": {
                "MarriedTo": str(ctx.author),
                "MarriedDate": str(m_date)
            }})

            await msg.delete()
            return await ctx.send(embed=Embed(title="Marry", description=f"{ctx.author.mention} has married {user.mention}", color=self.color))

        if emoji == "❎":
            await msg.delete()
            return await ctx.send(embed=Embed(title="Marry", description=f"{user.mention} didn't want to marry {ctx.author.mention}", color=self.color))

    @marry.error
    async def marry_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/marry <@user>`")
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"Sorry {ctx.author.mention} This command in on cooldown, Try again in {round(error.retry_after)} seconds.")

    @commands.command(help="Divorce a specified user!")
    @commands.cooldown(rate=1, per=120, type=commands.BucketType.member)
    async def divorce(self, ctx, user: Member):
        if not (Wealth._has_account(ctx.author.id)):
            await Wealth._create_account(ctx.author.id)

        if user == ctx.author:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send(f"Sorry {ctx.author.mention} but you can't divorce yourself!")

        result = Wealth.mass_fetch(ctx.author.id)
        Marriedto_ = result["MarriedTo"]
        MarriedDate = result["MarriedDate"]

        if self.collection.find_one({"_id": ctx.author.id})["MarriedTo"] == "Nobody":
            ctx.command.reset_cooldown(ctx)
            embed = Embed(title="Error!", description=f"Sorry {ctx.author.mention} You are not married yet!.", color=self.color)
            return await ctx.send(embed=embed)

        if not self.collection.find_one({"_id": ctx.author.id})["MarriedTo"] == str(user):
            ctx.command.reset_cooldown(ctx)
            embed = Embed(title="Error!", description=f"Sorry {ctx.author.mention} You're not married to {user}.", color=self.color)
            return await ctx.send(embed=embed)

        self.collection.update_one({"_id": ctx.author.id}, {"$set": {"MarriedTo": "Nobody"}})
        self.collection.update_one({"_id": user.id}, {"$set": {
            "MarriedTo": "Nobody",
            "MarriedDate": "No date"
        }})

        return await ctx.send(embed=Embed(title="Divorce", description=f"{ctx.author.mention} has divorced {user.mention}", color=self.color))


    @divorce.error
    async def divorce_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/divorce <@user>`")
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"Sorry {ctx.author.mention} This command in on cooldown, Try again in {round(error.retry_after)} seconds.")


    @commands.command(help="Deposit money into your World bank account", aliases=["dep"])
    async def deposit(self, ctx, amount: int):
        if not (Wealth._has_account(ctx.author.id)):
            await Wealth._create_account(ctx.author.id)

        if amount < 0:
            return await ctx.send(f"Sorry {ctx.author.mention} No signed integers or 0!")

        if self.collection.find_one({"_id": ctx.author.id})["coins"] < amount:
            return await ctx.send(embed=Embed(title="Error!", description=f"Sorry {ctx.author.mention} You can't deposit because you don't have that much money."))

        Wealth._deposit_coins(ctx.author.id, amount)
        return await ctx.send(embed=Embed(title="Deposit", description=f"{ctx.author.mention} You have deposited `{amount}` coin(s)", color=self.color))

    @commands.command(help="Withdraw money from your World bank account.", aliases=["with"])
    async def withdraw(self, ctx, amount: int):
        if not (Wealth._has_account(ctx.author.id)):
            await Wealth._create_account(ctx.author.id)

        if amount < 0:
            return await ctx.send(f"Sorry {ctx.author.mention} No signed integers or 0!")

        result = Wealth.mass_fetch(ctx.author.id)
        if result["Bank"] < amount:
            embed = Embed(title="Error!", description=f"Sorry {ctx.author.mention} You can't withdraw because you don't have that much money in the bank.", color=self.color)
            return await ctx.send(embed=embed)

        self.collection.update_one({"_id": ctx.author.id}, {"$inc": {
            "Bank": -amount,
            "coins": amount
        }})
        embed = Embed(title="Withdraw", description=f"{ctx.author.mention} you have just withdrawn `{amount}` coins.", color=self.color)
        await ctx.send(embed=embed)

    @deposit.error
    async def deposit_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/deposit <amount>`")


    @withdraw.error
    async def withdraw_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/withdraw <amount>`")


    @commands.command(help="World shootout", aliases=["shoot", "worldshoot"])
    @commands.cooldown(rate=1, per=15, type=commands.BucketType.member)
    async def shootout(self, ctx):
        if not (Wealth._has_account(ctx.author.id)):
            await Wealth._create_account(ctx.author.id)
        
        random = Wealth.shootout_ran()

        embed = Embed(title="Shootout", description="Is World a shooter?", color=self.color)
        embed.set_image(url=random)
        embed.set_footer(text="|✅ - shooter|❎ - innocent|🚫 - nothing")
        message = await ctx.send(embed=embed)

        await message.add_reaction('✅')
        await message.add_reaction('❎')
        await message.add_reaction('🚫')

        emoji = ''

        while True: # just so you know, $inc increments the number so you don't have to use $set every time
            if emoji == '✅':
                if random == "https://im-a-dev.xyz/QqoZ2M6m.png":
                    self.collection.update_one({"_id": ctx.author.id}, {"$inc": {"coins": 250}})
                    await message.delete()
                    return await ctx.send(f"Hey {ctx.author.mention} you caught World in the act! and have earned a total of `250` coins. Well done!")
                await message.delete()
                return await ctx.send(f"Sorry {ctx.author.mention} you chose the wrong one! try again next time.")

            if emoji == '❎':
                if random == "https://im-a-dev.xyz/BvdekLII.png":
                    self.collection.update_one({"_id": ctx.author.id}, {"$inc": {"coins": 100}})
                    await message.delete()
                    return await ctx.send(f"Hey {ctx.author.mention} you have found innocent World! and have earned a total of `100` coins. Well done!")
                await message.delete()
                return await ctx.send(f"Sorry {ctx.author.mention} you chose the wrong one! try again next time.")

            if emoji == '🚫':
                if random == "https://im-a-dev.xyz/MfSnYYAa.png":
                    await message.delete()
                    return await ctx.send(f"Hey {ctx.author.mention} you found nothing...")
                await message.delete()
                return await ctx.send(f"Sorry {ctx.author.mention} you chose the wrong one! try again next time.")
            try:
                res = await self.bot.wait_for('reaction_add', check=lambda r, u: u.id == ctx.author.id and r.message.id == message.id, timeout=4)

                if not res:
                    break

                if res[1].id != 700292147311542282: # use ID instead of user name
                    emoji=str(res[0].emoji)

            except:
                await message.delete()
                return await ctx.send(f"Sorry {ctx.author.mention} you werent fast enough and World got away...")

        await message.clear_reactions()

    @shootout.error
    async def shootout_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"Sorry {ctx.author.mention} This command in on cooldown, Try again in {round(error.retry_after)} seconds.")


    @commands.command(help="Fish for things in the lake", aliases=["fish", "worldfishing"])
    @commands.cooldown(rate=1, per=120, type=commands.BucketType.member)
    async def fishing(self, ctx):
        if not (Wealth._has_account(ctx.author.id)):
            Wealth._create_account(ctx.author.id)

        random = Wealth.fishing_ran()
        doc = Wealth.mass_fetch(ctx.author.id)
        random_coins = randint(1, 50)
        fishing_ctx = { # using it here because it has randint() in it
            "https://im-a-dev.xyz/1kKJXQSr.png": None, # key_name, amount_added_to_db, message
            "https://im-a-dev.xyz/ImWqkaSy.png": ("Fish", 1, f"Great, looks like you have caught a fish! you now have a total of `{(doc['Fish'] + 1):,}` Fish!"),
            "https://im-a-dev.xyz/sqPSfhJJ.png": ("cookie", 5, f"Wow, you caught a box of cookies while fishing?! you now have a total of `{(doc['cookie'] + 5):,}` Cookies!"),
            "https://im-a-dev.xyz/syTQUdrV.png": ("coins", random_coins, f"Wow, you caught a bag of coins while fishing?!\nCoins in the bag: `{random_coins}`\nyou now have a total of `{(doc['coins'] + random_coins):,}` Coins!")
        }        

        if not fishing_ctx[random]: # they didn't caught anything
            embed = Embed(title="Fishing", description="There are no fish in the lake right now, come again soon!", color=self.color)
            embed.set_image(url="https://im-a-dev.xyz/1kKJXQSr.png")
            return await ctx.send(embed=embed)
        # otherwise, they caught something
        key_name, amount_added_to_db, message = fishing_ctx[random]
        self.collection.update_one({"_id": ctx.author.id}, {"$inc": {key_name: amount_added_to_db}})

        embed = Embed(title="Fishing", description=message, color=self.color)
        embed.set_image(url=random)
        return await ctx.send(embed=embed)

    @fishing.error
    async def fishing_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"Sorry {ctx.author.mention} This command in on cooldown, Try again in {round(error.retry_after)} seconds.")


    @commands.command(help="What badges do you have?", aliases=["mybadges", "showbadges", "badge"])
    async def badges(self, ctx):
        if not (Wealth._has_account(ctx.author.id)):
            await Wealth._create_account(ctx.author.id)

        result = Wealth.mass_fetch(ctx.author.id)
        await ctx.send(embed=Embed(title="Your badges", description=f"Noob: {result['BadgeSlot1']}\nBeginner: {result['BadgeSlot2']}\nLeader: {result['BadgeSlot3']}\n\n[`Noob`](https://cdn.discordapp.com/emojis/779192872402026516.png?v=1) | [`Beginner`](https://cdn.discordapp.com/emojis/779192938617241600.png?v=1) | [`Leader`](https://cdn.discordapp.com/emojis/779193003024973835.png?v=1)", color=self.color))

    @commands.command(help="Show your reputation", aliases=["myrep", "myreputation", "reputationcount"])
    async def repcount(self, ctx):
        if not (Wealth._has_account(ctx.author.id)):
            await Wealth._create_account(ctx.author.id)

        rep = Wealth.fetch_user(ctx.author.id, "Reputation")
        await ctx.send(embed=Embed(title="Your Reputation", description=f"Reputation Points: `{rep}`", color=self.color))

    @commands.command(help="Show your World status", aliases=["mystat", "worldstatus"])
    async def mystatus(self, ctx):
        if not (Wealth._has_account(ctx.author.id)):
            await Wealth._create_account(ctx.author.id)

        status = Wealth.fetch_user(ctx.author.id, "afk")
        await ctx.send(embed=Embed(title="Your Status", description=f"World status: `{status}`",color=self.color))

def setup(bot):
    bot.add_cog(EconomyFunCog(bot))