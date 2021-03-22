from textwrap import dedent
from random import randint
from discord import Embed, Member
from discord.ext import commands
from datetime import datetime
from typing import Optional
from PIL import Image, ImageFont, ImageDraw
from framework import Wealth, Misc, Paginator, require_account

class EconomyFunCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.items_order = ("coins", "Bank", "cookie", "choc", "apple", "poop", "beans", "pizza", "waffles", "Fish")
        self.badge_urls = ("https://cdn.discordapp.com/emojis/779192872402026516.png", "https://cdn.discordapp.com/emojis/779192938617241600.png", "https://cdn.discordapp.com/emojis/779193003024973835.png")
        self.badges_ctx = { # short name, (Order for "BadgeSlot{number}", price, emoji, full name)
            "noob": (1, 900, "<:WorldBadge1:779192872402026516>", "Noob Badge"),
            "beginner": (2, 3500, "<:WorldBadge2:779192938617241600>", "Beginner Badge"),
            "leader": (3, 9500, "<:WorldBadge3:779193003024973835>", "Leader Badge")
        }
        self.shoot_ctx = ( # emoji, image url, amount, success message
            ('✅', "https://im-a-dev.xyz/QqoZ2M6m.png", 250, "you caught World in the act! and have earned a total of `250` coins. Well done!"),
            ('❎', "https://im-a-dev.xyz/BvdekLII.png", 100, "you have found innocent World! and have earned a total of `100` coins. Well done!"),
            ('🚫', "https://im-a-dev.xyz/MfSnYYAa.png", None, "you found nothing...")
        )

    @commands.command(help="Add reputation points to a user.", aliases=["rep"])
    @commands.cooldown(rate=1, per=1800, type=commands.BucketType.member)
    @require_account()
    async def reputation(self, ctx, user: Member):
        now = datetime.now()

        if user.id == ctx.author.id:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send(f"Sorry {ctx.author.mention} You can\'t give yourself a reputation point.")
            
        last_used = now.strftime("%m/%d/%Y, %H:%M:%S")

        Wealth.collection.update_one({"_id": user.id}, {"$inc": {"Reputation": 1}})
        Wealth.collection.update_one({"_id": ctx.author.id}, {"$set": {
            "TargetMember": user.id,
            "LastUsed": last_used
        }})

        await ctx.send(embed=Embed(title="Reputation", description=f"{ctx.author.mention} You added `+1` Reputation to {user.mention}", color=self.bot.color))

    @reputation.error
    async def reputation_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/rep <@user>`")
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"Sorry {ctx.author.mention} This command in on cooldown, Try again in {round(error.retry_after)} seconds.")

    @commands.command(help="Info on your last given rep point.")
    @require_account()
    async def repinfo(self, ctx):
        data = Wealth.collection.find_one({"_id": ctx.author.id})
        if not data:
            return await ctx.send(f"Sorry {ctx.author.mention} you havent gave anyone a rep point!\nTry using the command `rep` to give a reputation point to someone you think deserves it.")
        elif data["LastUsed"] == "Isnotset":
            return await ctx.send(f"Sorry {ctx.author.mention} you havent gave anyone a rep point!\nTry using the command `rep` to give a reputation point to someone you think deserves it.")
        await ctx.send(embed=Embed(
            title="Last Reputation",
            description=f"{ctx.author.mention} You gave <@{data['TargetMember']}> `1` Reputation point\nDate: `{data['LastUsed']}`",
            color=self.bot.color
        ))
    
    async def profile_canvas(self, user, result):
        pfp = await Misc.fetch_pfp(user)
        pfp_resize = pfp.resize((49, 49))
        font = ImageFont.truetype("./fonts/Whitney-Medium.ttf", 30)
        fontm = ImageFont.truetype("./fonts/Whitney-Medium.ttf", 25)
        fontmm = ImageFont.truetype("./fonts/Whitney-Medium.ttf", 20)
        
        main = Image.open("./images/profile_template.png")
        draw = ImageDraw.Draw(main)
        if pfp.mode != "RGBA":
            main.paste(pfp_resize, (0, 0))
        else:
            main.paste(pfp_resize, (0, 0), pfp_resize)
        
        draw.text((60, 5), user.display_name, font=font, fill=(255, 255, 255))
        draw.text((10, 60), f"Created account {Misc._delayfstr(result['AccountCreated'])} ago\nLast transfer: {Misc._delayfstr(result['LastTransfer'])} ago\nMarried to: {result['MarriedTo']}\nReputation: {result['Reputation']:,}", font=fontmm, fill=(255, 255, 255))
    
        cursor = 60
        for item in self.items_order:
            width = font.getsize(f"{result[item]:,}")[0]
            draw.text((564 - width, cursor), f"{result[item]:,}", font=fontm, fill=(255, 255, 255))
            cursor += 40

        cursor = 10
        for i in range(3):
            if not result[f"BadgeSlot{i + 1}"].startswith("<:"):
                continue
            badge_image = await Misc.image_from_url(self.bot, self.badge_urls[i])
            badge_image = badge_image.convert("RGBA").resize((90, 90))
            main.paste(badge_image, (cursor, 260), badge_image)
            cursor += 94
        
        pfp.close()
        del draw, cursor, pfp, font, fontm, fontmm
        return Misc.save_image(main)

    @commands.command()
    @require_account()
    async def profile(self, ctx, user: Optional[Member], option: Optional[str]):
        user = user or ctx.author
        result = Wealth.collection.find_one({'_id': user.id})

        if not option:
            buffer = await self.profile_canvas(user, result)
            return await ctx.send(file=buffer)

        elif option == "--embed":
            paginator = Paginator(ctx, [
                Embed(title='Page 1/3', description=f"{user}'s Profile", colour=self.bot.color).add_field(name="<:memberlogo:765649915031846912> | Account", value=f"Account Type: `World Account`\nCoins: `{result['coins']}`\nBank: `{result['Bank']}`\nReputation: `{result['Reputation']}`\nStatus: `{result['afk']}`"),
                Embed(title='Page 2/3', description=f"{user}'s Profile", colour=self.bot.color).add_field(name=":handbag: | Inventory", value=f":cookie: Cookies: `{result['cookie']}`\n:chocolate_bar: Chocbars: `{result['choc']}`\n:apple: Apples: `{result['apple']}`\n:poop: Poop: `{result['poop']}`\n<:beanworld:774371828629635132> Beans: `{result['beans']}`\n:pizza: Pizza: `{result['pizza']}`\n:waffle: Waffles `{result['waffles']}`\n:fish: Fish: `{result['Fish']}`"),
                Embed(title="Page 3/3", description=f"{user}'s Profile", colour=self.bot.color).add_field(name="<:shufflelogo:765652804387471430> | Other", value=f"Created World Account: `{result['AccountCreated']}`\nYour Last Transfer: `{result['LastTransfer']}`\nMarried to: `{result['MarriedTo']}`\nBadges:\n{result['BadgeSlot1']} Badge\n{result['BadgeSlot2']} Badge\n{result['BadgeSlot3']} Badge")
            ])
            return await paginator.execute()

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
            color=self.bot.color
        ))

    @commands.command(help="Buy a World Badge.")
    @require_account()
    async def buybadge(self, ctx, item: str):
        result = Wealth.collection.find_one({'_id': ctx.author.id})
        if not self.badges_ctx.get(item.lower()): # the person entered something other than `noob, beginner, leader`
            return await ctx.send(embed=Embed(title="Error!", description=f"Sorry {ctx.author.mention}, please select the correct badge, Badges available: `{', '.join(self.badges_ctx.keys())}`", color=self.bot.color))
        
        order, price, emoji, full_name = self.badges_ctx[item.lower()]
        if result["coins"] < price:
            return await ctx.send(embed=Embed(title="Error!", description=f"Sorry {ctx.author.mention} You dont have enough coins to buy `World {full_name}`", color=self.bot.color))
        elif result["BadgeSlot1"] == emoji:
            return await ctx.send(embed=Embed(title="Error!", description=f"Sorry {ctx.author.mention} You already have `World {full_name}`.", color=self.bot.color))
        
        await ctx.send(embed=Embed(
            title="World Badge",
            description=f"You have bought `World {full_name}` for `{price:,}` Coins. {emoji}",
            color=self.bot.color
        ))
        Wealth.collection.update_one({"_id": ctx.author.id}, {"$inc": {"coins": -price}})
        Wealth.collection.update_one({"_id": ctx.author.id}, {"$set": {f"BadgeSlot{order}": emoji}})

    @buybadge.error
    async def buybadge_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/buybadge <BadgeName>`")


    @commands.command(help="Marry a specified user!")
    @commands.cooldown(rate=1, per=120, type=commands.BucketType.member)
    @require_account()
    async def marry(self, ctx, user: Member):
        now = datetime.now()
        m_date = now.strftime("%m/%d/%Y")

        if user == ctx.author:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send(f"Sorry {ctx.author.mention} but you can't marry yourself!")

        result = Wealth.collection.find_one({'_id': ctx.author.id})

        if result["MarriedTo"] == str(user):
            ctx.command.reset_cooldown(ctx)
            return await ctx.send(embed=Embed(title="Error!", description=f"Sorry {ctx.author.mention} You're already married to `{user}`.", color=self.bot.color))

        if not result["MarriedTo"] == "Nobody":
            ctx.command.reset_cooldown(ctx)
            return await ctx.send(embed=Embed(title="Error!", description=f"Sorry {ctx.author.mention} You're already married.", color=self.bot.color))
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
            Wealth.collection.update_one({"_id": ctx.author.id}, {"$set": {
                "MarriedTo": str(user),
                "MarriedDate": str(m_date)
            }})
            Wealth.collection.update_one({"_id": user.id}, {"$set": {
                "MarriedTo": str(ctx.author),
                "MarriedDate": str(m_date)
            }})

            await msg.delete()
            return await ctx.send(embed=Embed(title="Marry", description=f"{ctx.author.mention} has married {user.mention}", color=self.bot.color))

        if emoji == "❎":
            await msg.delete()
            return await ctx.send(embed=Embed(title="Marry", description=f"{user.mention} didn't want to marry {ctx.author.mention}", color=self.bot.color))

    @marry.error
    async def marry_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/marry <@user>`")
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"Sorry {ctx.author.mention} This command in on cooldown, Try again in {round(error.retry_after)} seconds.")

    @commands.command(help="Divorce a specified user!")
    @commands.cooldown(rate=1, per=120, type=commands.BucketType.member)
    @require_account()
    async def divorce(self, ctx, user: Member):
        if user == ctx.author:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send(f"Sorry {ctx.author.mention} but you can't divorce yourself!")

        result = Wealth.collection.find_one({'_id': ctx.author.id})

        if result["MarriedTo"] == "Nobody":
            ctx.command.reset_cooldown(ctx)
            return await ctx.send(embed=Embed(title="Error!", description=f"Sorry {ctx.author.mention} You are not married yet!.", color=self.bot.color))

        if not result["MarriedTo"] == str(user):
            ctx.command.reset_cooldown(ctx)
            return await ctx.send(embed=Embed(title="Error!", description=f"Sorry {ctx.author.mention} You're not married to {user}.", color=self.bot.color))

        Wealth.collection.update_one({"_id": ctx.author.id}, {"$set": {"MarriedTo": "Nobody"}})
        Wealth.collection.update_one({"_id": user.id}, {"$set": {
            "MarriedTo": "Nobody",
            "MarriedDate": "No date"
        }})

        return await ctx.send(embed=Embed(title="Divorce", description=f"{ctx.author.mention} has divorced {user.mention}", color=self.bot.color))


    @divorce.error
    async def divorce_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/divorce <@user>`")
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"Sorry {ctx.author.mention} This command in on cooldown, Try again in {round(error.retry_after)} seconds.")


    @commands.command(help="Deposit money into your World bank account", aliases=["dep"])
    @require_account()
    async def deposit(self, ctx, amount: int):
        if amount < 0:
            return await ctx.send(f"Sorry {ctx.author.mention} No signed integers or 0!")

        if Wealth.collection.find_one({"_id": ctx.author.id})["coins"] < amount:
            return await ctx.send(embed=Embed(title="Error!", description=f"Sorry {ctx.author.mention} You can't deposit because you don't have that much money."))

        Wealth._deposit_coins(ctx.author.id, amount)
        return await ctx.send(embed=Embed(title="Deposit", description=f"{ctx.author.mention} You have deposited `{amount}` coin(s)", color=self.bot.color))

    @commands.command(help="Withdraw money from your World bank account.", aliases=["with"])
    @require_account()
    async def withdraw(self, ctx, amount: int):
        if amount < 0:
            return await ctx.send(f"Sorry {ctx.author.mention} No signed integers or 0!")

        result = Wealth.collection.find_one({'_id': ctx.author.id})
        if result["Bank"] < amount:
            return await ctx.send(embed=Embed(title="Error!", description=f"Sorry {ctx.author.mention} You can't withdraw because you don't have that much money in the bank.", color=self.bot.color))

        Wealth.collection.update_one({"_id": ctx.author.id}, {"$inc": {
            "Bank": -amount,
            "coins": amount
        }})
        await ctx.send(embed=Embed(title="Withdraw", description=f"{ctx.author.mention} you have just withdrawn `{amount}` coins.", color=self.bot.color))

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
    @require_account()
    async def shootout(self, ctx):
        random = Wealth.shootout_ran()
        message = await ctx.send(embed=Embed(title="Shootout", description="Is World a shooter?", color=self.bot.color).set_image(url=random).set_footer(text="|✅ - shooter|❎ - innocent|🚫 - nothing"))

        for _emoji in self.shoot_ctx:
            await message.add_reaction(_emoji[0])

        emoji = ''

        while True:
            for _emoji, _image_url, _amount, _message in self.shoot_ctx:
                if emoji == _emoji:
                    await message.delete()
                    if (random == _image_url):
                        if _amount:
                            Wealth.collection.update_one({"_id": ctx.author.id}, {"$inc": {"coins": _amount}})
                        return await ctx.send(f"Hey {ctx.author.mention} {_message}")
                    return await ctx.send(f"Sorry {ctx.author.mention} you chose the wrong one! try again next time.")
            
            try:
                res = await self.bot.wait_for('reaction_add', check=lambda r, u: u.id == ctx.author.id and r.message.id == message.id, timeout=4)

                if not res:
                    break

                if res[1].id != 700292147311542282:
                    emoji = str(res[0].emoji)

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
    @require_account()
    async def fishing(self, ctx):
        random = Wealth.fishing_ran()
        doc = Wealth.collection.find_one({'_id': ctx.author.id})
        random_coins = randint(1, 50)
        fishing_ctx = { # using it here because it has randint() in it
            "https://im-a-dev.xyz/1kKJXQSr.png": None, # key_name, amount_added_to_db, message
            "https://im-a-dev.xyz/ImWqkaSy.png": ("Fish", 1, f"Great, looks like you have caught a fish! you now have a total of `{(doc['Fish'] + 1):,}` Fish!"),
            "https://im-a-dev.xyz/sqPSfhJJ.png": ("cookie", 5, f"Wow, you caught a box of cookies while fishing?! you now have a total of `{(doc['cookie'] + 5):,}` Cookies!"),
            "https://im-a-dev.xyz/syTQUdrV.png": ("coins", random_coins, f"Wow, you caught a bag of coins while fishing?!\nCoins in the bag: `{random_coins}`\nyou now have a total of `{(doc['coins'] + random_coins):,}` Coins!")
        }        

        if not fishing_ctx[random]: # they didn't caught anything
            return await ctx.send(embed=Embed(title="Fishing", description="There are no fish in the lake right now, come again soon!", color=self.bot.color).set_image(url="https://im-a-dev.xyz/1kKJXQSr.png"))
        # otherwise, they caught something
        key_name, amount_added_to_db, message = fishing_ctx[random]
        Wealth.collection.update_one({"_id": ctx.author.id}, {"$inc": {key_name: amount_added_to_db}})
        return await ctx.send(embed=Embed(title="Fishing", description=message, color=self.bot.color).set_image(url=random))

    @fishing.error
    async def fishing_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"Sorry {ctx.author.mention} This command in on cooldown, Try again in {round(error.retry_after)} seconds.")

    @commands.command(help="What badges do you have?", aliases=["mybadges", "showbadges", "badge"])
    @require_account()
    async def badges(self, ctx):
        result = Wealth.collection.find_one({'_id': ctx.author.id})
        await ctx.send(embed=Embed(title="Your badges", description=f"Noob: {result['BadgeSlot1']}\nBeginner: {result['BadgeSlot2']}\nLeader: {result['BadgeSlot3']}\n\n[`Noob`](https://cdn.discordapp.com/emojis/779192872402026516.png?v=1) | [`Beginner`](https://cdn.discordapp.com/emojis/779192938617241600.png?v=1) | [`Leader`](https://cdn.discordapp.com/emojis/779193003024973835.png?v=1)", color=self.bot.color))

    @commands.command(help="Show your reputation", aliases=["myrep", "myreputation", "reputationcount"])
    @require_account()
    async def repcount(self, ctx):
        await ctx.send(embed=Embed(title="Your Reputation", description=f"Reputation Points: `{Wealth.collection.find_one({'_id': ctx.author.id})['Reputation']}`", color=self.bot.color))

    @commands.command(help="Show your World status", aliases=["mystat", "worldstatus"])
    @require_account()
    async def mystatus(self, ctx):
        await ctx.send(embed=Embed(title="Your Status", description=f"World status: `{Wealth.collection.find_one({'_id': ctx.author.id})['afk']}`", color=self.bot.color))

    @commands.command(help="Find things in the Trash!", aliases=["trashbin", "bin"])
    @commands.cooldown(rate=1, per=120, type=commands.BucketType.member)
    @require_account()
    async def trash(self, ctx):
        random = Wealth.trash_ran()
        doc = Wealth.collection.find_one({'_id': ctx.author.id})
        random_coins = randint(1, 18)
        random_cookies = randint(1, 21)
        trash_ctx = {
            "https://im-a-dev.xyz/i8HiGmwU.png": None, # key_name, amount_added_to_db, message
            "https://im-a-dev.xyz/ogWxLI7K.png": ("Reputation", 1, f"Wow, You found some Reputation in the trash! Good job, You now have a total of `{(doc['Reputation'] + 1)}` Rep points!"),
            "https://im-a-dev.xyz/zqyCJ9sH.png": ("cookie", random_cookies, f"Amazing, You found `{random_cookies}` cookies in the trash bin, You now have `{(doc['cookie'] + random_cookies):,}` Cookies!"),
            "https://im-a-dev.xyz/om3vsD0s.png": ("coins", random_coins, f"Nice you found a bag of coins in the trash bin!\nCoins in the bag: `{random_coins}`\nyou now have a total of `{(doc['coins'] + random_coins):,}` Coins!")
        }        

        if not trash_ctx[random]: # they didn't caught anything
            return await ctx.send(embed=Embed(title="Trash Search", description="Nothing found in this bin, Try again soon!", color=self.bot.color).set_image(url="https://im-a-dev.xyz/i8HiGmwU.png"))
        # otherwise, they caught something
        key_name, amount_added_to_db, message = trash_ctx[random]
        Wealth.collection.update_one({"_id": ctx.author.id}, {"$inc": {key_name: amount_added_to_db}})
        return await ctx.send(embed=Embed(title="Trash Search", description=message, color=self.bot.color).set_image(url=random))

    @trash.error
    async def trash_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"Sorry {ctx.author.mention} This command in on cooldown, Try again in {round(error.retry_after)} seconds.")

def setup(bot):
    bot.add_cog(EconomyFunCog(bot))