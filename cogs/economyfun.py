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

from framework import Wealth


class EconomyFunCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.collection = MongoClient(environ["MONGODB_URL"])["Coins"]["UserCoins"]
        self.color = 0x2F3136

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

        rep = Wealth.fetch_user(user.id, "Reputation")

        reputation_point = 1 + rep
        last_used = str(now.strftime("%m/%d/%Y, %H:%M:%S"))

        self.collection.update_one({"_id": user.id}, {"$set": {"Reputation": reputation_point}})
        self.collection.update_one({"_id": ctx.author.id}, {"$set": {"TargetMember": user.id}})
        self.collection.update_one({"_id": ctx.author.id}, {"$set": {"LastUsed": last_used}})

        embed = Embed(title="Reputation", description=f"{ctx.author.mention} You added `+1` Reputation to {user.mention}", color=self.color)
        await ctx.send(embed=embed)

    @reputation.error
    async def reputation_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/rep <@user>`")
        if isinstance(error, commands.CommandOnCooldown):
            a = error.retry_after
            a = round(a)
            await ctx.send(f"Sorry {ctx.author.mention} This command in on cooldown, Try again in {a} seconds.")


    @commands.command(help="Info on your last given rep point.")
    async def repinfo(self, ctx):
        now = datetime.now()

        if not (Wealth._has_account(ctx.author.id)):
            await Wealth._create_account(ctx.author.id)

        if not self.collection.find_one({"_id": ctx.author.id}):
            return await ctx.send(f"Sorry {ctx.author.mention} you havent gave anyone a rep point!\nTry using the command `rep` to give a reputation point to someone you think deserves it.")

        if self.collection.find_one({"_id": ctx.author.id})["LastUsed"] == "Isnotset":
            return await ctx.send(f"Sorry {ctx.author.mention} you havent gave anyone a rep point!\nTry using the command `rep` to give a reputation point to someone you think deserves it.")

        result = self.collection.find_one({"_id": ctx.author.id}):
        last_used = result["LastUsed"]
        target_user = result["TargetMember"]

        embed = Embed(
            title="Last Reputation",
            description=f"{ctx.author.mention} You gave <@{target_user}> `1` Reputation point\nDate: `{last_used}`",
            color=self.color
            )
        await ctx.send(embed=embed)

    @commands.command()
    async def profile(self, ctx, user: Member=None):
        if not (Wealth._has_account(ctx.author.id)):
            await Wealth._create_account(ctx.author.id)

        user = user or ctx.author

        result = Wealth.mass_fetch(user.id)

        noob_b, beginner_b, leader_b, marry, bank_, beans, pizza, waffles, fish, coins, rep, afk = Wealth.extract_props(result, ['BadgeSlot1', 'BadgeSlot2', 'BadgeSlot3', 'MarriedTo', "Bank", "beans", "pizza", "waffles", "Fish", "coins", "Reputation", "afk"])

        last_trans, cookie, poop, apple, chocolate, created = Wealth.extract_props(result, ["LastTransfer", "cookie", "poop", "apple", "choc", "AccountCreated"])

        page1 = Embed(title='Page 1/3', description=f"{user}'s Profile", colour=self.color).add_field(name="<:memberlogo:765649915031846912> | Account", value=f"Account Type: `World Account`\nCoins: `{coins}`\nBank: `{bank_}`\nReputation: `{rep}`\nStatus: `{afk}`")

        page2 = Embed(title='Page 2/3', description=f"{user}'s Profile", colour=self.color).add_field(name=":handbag: | Inventory", value=f":cookie: Cookies: `{cookie}`\n:chocolate_bar: Chocbars: `{chocolate}`\n:apple: Apples: `{apple}`\n:poop: Poop: `{poop}`\n<:beanworld:774371828629635132> Beans: `{beans}`\n:pizza: Pizza: `{pizza}`\n:waffle: Waffles `{waffles}`\n:fish: Fish: `{fish}`")

        page3 = Embed(title="Page 3/3", description=f"{user}'s Profile", colour=self.color).add_field(name="<:shufflelogo:765652804387471430> | Other", value=f"Created World Account: `{created}`\nYour Last Transfer: `{last_trans}`\nMarried to: `{marry}`\nBadges:\n{noob_b} Badge\n{beginner_b} Badge\n{leader_b} Badge")

        pages = [page1,page2,page3]

        message = await ctx.send(embed=page1)

        await message.add_reaction('\u23ee')
        await message.add_reaction('\u25c0')
        await message.add_reaction('\u25b6')
        await message.add_reaction('\u23ed')
        await message.add_reaction('\u23F9')

        i=0
        emoji = ''

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
            if str(res[1])!='World#4520':
                emoji=str(res[0].emoji)

        await message.clear_reactions()


    @commands.command(help="Badge Shop!", aliases=["bshop"])
    async def badgeshop(self, ctx):
        embed = Embed(
            title="World Badge Shop!",
            description=dedent("""
                - World Noob
                `Cost 900 Coins!`
                - World Beginner
                `Cost 3,500 Coins!`
                - World Leader
                `Cost 9,500 Coins!`
                """),
            color=0x2F3136
            )
        await ctx.send(embed=embed)

    @commands.command(help="Buy a World Badge.")
    async def buybadge(self, ctx, item: str):
        if not (Wealth._has_account(ctx.author.id)):
            await Wealth._create_account(ctx.author.id)

        result = Wealth.mass_fetch(ctx.author.id)
        if item.lower() == "noob":
            noob_b = result["BadgeSlot1"] # Noob Badge
            user_coins = result["coins"]

            cost_of_b = int(900)
            total_cost = user_coins - cost_of_b

            if self.collection.find_one({"_id": ctx.author.id})["coins"] < 900:
                embed = Embed(title="Error!", description=f"Sorry {ctx.author.mention} You dont have enough coins to buy `World Noob Badge`", color=self.color)
                return await ctx.send(embed=embed)
            if self.collection.find_one({"_id": ctx.author.id})["BadgeSlot1"] == "<:WorldBadge1:779192872402026516>":
                embed = Embed(title="Error!", description=f"Sorry {ctx.author.mention} You already have `World Noob Badge`.", color=self.color)
                return await ctx.send(embed=embed)

            self.collection.update_one({"_id": ctx.author.id}, {"$set": {"coins": total_cost}})
            self.collection.update_one({"_id": ctx.author.id}, {"$set": {"BadgeSlot1": "<:WorldBadge1:779192872402026516>"}})

            embed = Embed(
                title="World Badge",
                description="You have bought `World Noob Badge` for `900` Coins. <:WorldBadge1:779192872402026516>",
                color=0x2F3136
                )
            await ctx.send(embed=embed)

        if item.lower() == "beginner":
            noob_b2 = result["BadgeSlot2"] # Beginner badge
            user_coins2 = result["coins"]

            cost_of_b2 = int(3500)
            total_cost2 = user_coins2 - cost_of_b2

            if self.collection.find_one({"_id": ctx.author.id})["coins"] < 3500:
                embed = Embed(title="Error!", description=f"Sorry {ctx.author.mention} You dont have enough coins to buy `World Beginner Badge`", color=self.color)
                return await ctx.send(embed=embed)

            if self.collection.find_one({"_id": ctx.author.id})["BadgeSlot2"] == "<:WorldBadge2:779192938617241600>":
                embed = Embed(title="Error!", description=f"Sorry {ctx.author.mention} You already have `World Beginner Badge`.", color=self.color)
                return await ctx.send(embed=embed)

            self.collection.update_one({"_id": ctx.author.id}, {"$set": {"coins": total_cost2}})
            self.collection.update_one({"_id": ctx.author.id}, {"$set": {"BadgeSlot2": "<:WorldBadge2:779192938617241600>"}})

            embed = Embed(
                title="World Badge",
                description="You have bought `World Beginner Badge` for `3,500` Coins. <:WorldBadge2:779192938617241600>",
                color=0x2F3136
                )
            await ctx.send(embed=embed)

        if item.lower() == "leader":
            noob_b3 = result["BadgeSlot3"] # Leader badge
            user_coins3 = result["coins"]

            cost_of_b3 = int(9500)
            total_cost3 = user_coins3 - cost_of_b3

            if self.collection.find_one({"_id": ctx.author.id})["coins"] < 9500:
                embed = Embed(title="Error!", description=f"Sorry {ctx.author.mention} You dont have enough coins to buy `World Leader Badge`", color=self.color)
                return await ctx.send(embed=embed)

            if self.collection.find_one({"_id": ctx.author.id})["BadgeSlot2"] == "<:WorldBadge3:779193003024973835>":
                embed = Embed(title="Error!", description=f"Sorry {ctx.author.mention} You already have `World Leader Badge`.", color=self.color)
                return await ctx.send(embed=embed)

            self.collection.update_one({"_id": ctx.author.id}, {"$set": {"coins": total_cost3}})
            self.collection.update_one({"_id": ctx.author.id}, {"$set": {"BadgeSlot3": "<:WorldBadge3:779193003024973835>"}})

            embed = Embed(
                title="World Badge",
                description="You have bought `World Leader Badge` for `9,500` Coins. <:WorldBadge3:779193003024973835>",
                color=0x2F3136
                )
            await ctx.send(embed=embed)

    @buybadge.error
    async def buybadge_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/buybadge <BadgeName>`")


    @commands.command(help="Marry a specified user!")
    @commands.cooldown(rate=1, per=120, type=commands.BucketType.member)
    async def marry(self, ctx, user: Member):
        now = datetime.now()
        m_date = str(now.strftime("%m/%d/%Y"))

        if not (Wealth._has_account(ctx.author.id)):
            await Wealth._create_account(ctx.author.id)

        if user == ctx.author:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send(f"Sorry {ctx.author.mention} but you can't marry yourself!")

        result = Wealth.mass_fetch(ctx.author.id)
        Marriedto_ = result["MarriedTo"]
        MarriedDate = result["MarriedDate"]

        if self.collection.find_one({"_id": ctx.author.id})["MarriedTo"] == str(user):
            ctx.command.reset_cooldown(ctx)
            embed = Embed(title="Error!", description=f"Sorry {ctx.author.mention} You're already married to `{user}`.", color=self.color)
            return await ctx.send(embed=embed)

        if not self.collection.find_one({"_id": ctx.author.id})["MarriedTo"] == "Nobody":
            ctx.command.reset_cooldown(ctx)
            embed = Embed(title="Error!", description=f"Sorry {ctx.author.mention} You're already married.", color=self.color)
            return await ctx.send(embed=embed)

        msg = await ctx.send(f"Hey {user.mention} {ctx.author.mention} wants to marry you.\nPlease react.")

        emoji = ''
        await msg.add_reaction('☑')
        await msg.add_reaction('❎')
        try:
            res = await self.bot.wait_for('reaction_add', check=lambda r, u: u.id == user.id and r.message.id == msg.id, timeout=13)
        except:
            await msg.clear_reactions()

        if str(res[1])!='World#4520':
            emoji=str(res[0].emoji)

        if emoji == "☑":
            self.collection.update_one({"_id": ctx.author.id}, {"$set": {"MarriedTo": str(user)}})
            self.collection.update_one({"_id": ctx.author.id}, {"$set": {"MarriedDate": str(m_date)}})
            self.collection.update_one({"_id": user.id}, {"$set": {"MarriedTo": str(ctx.author)}})
            self.collection.update_one({"_id": user.id}, {"$set": {"MarriedDate": str(m_date)}})

            embed = Embed(title="Marry", description=f"{ctx.author.mention} has married {user.mention}", color=self.color)
            await msg.delete()
            return await ctx.send(embed=embed)

        if emoji == "❎":
            await msg.delete()
            embed = Embed(title="Marry", description=f"{user.mention} didn't want to marry {ctx.author.mention}", color=self.color)
            return await ctx.send(embed=embed)

    @marry.error
    async def marry_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/marry <@user>`")
        if isinstance(error, commands.CommandOnCooldown):
            a = error.retry_after
            a = round(a)
            await ctx.send(f"Sorry {ctx.author.mention} This command in on cooldown, Try again in {a} seconds.")

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
        self.collection.update_one({"_id": user.id}, {"$set": {"MarriedTo": "Nobody"}})
        self.collection.update_one({"_id": user.id}, {"$set": {"MarriedDate": "No date"}})

        embed = Embed(title="Divorce", description=f"{ctx.author.mention} has divorced {user.mention}", color=self.color)
        return await ctx.send(embed=embed)


    @divorce.error
    async def divorce_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/divorce <@user>`")
        if isinstance(error, commands.CommandOnCooldown):
            a = error.retry_after
            a = round(a)
            await ctx.send(f"Sorry {ctx.author.mention} This command in on cooldown, Try again in {a} seconds.")


    @commands.command(help="Deposit money into your World bank account", aliases=["dep"])
    async def deposit(self, ctx, amount: int):
        if not (Wealth._has_account(ctx.author.id)):
            await Wealth._create_account(ctx.author.id)

        if amount < 0:
            return await ctx.send(f"Sorry {ctx.author.mention} No signed integers or 0!")

        if self.collection.find_one({"_id": ctx.author.id})["coins"] < amount:
            embed = Embed(title="Error!", description=f"Sorry {ctx.author.mention} You can't deposit because you don't have that much money.")
            return await ctx.send(embed=embed)

        Wealth._deposit_coins(ctx.author.id, amount)

        embed = Embed(title="Deposit", description=f"{ctx.author.mention} You have deposited `{amount}` coin(s)", color=self.color)
        return await ctx.send(embed=embed)



    @commands.command(help="Withdraw money from your World bank account.", aliases=["with"])
    async def withdraw(self, ctx, amount: int):
        if not (Wealth._has_account(ctx.author.id)):
            await Wealth._create_account(ctx.author.id)

        if amount < 0:
            return await ctx.send(f"Sorry {ctx.author.mention} No signed integers or 0!")

        result = Wealth.mass_fetch(ctx.author.id)
        bank_ = result["Bank"]
        coins_ = result["coins"]

        total_coins = coins_ + amount
        remove_coins = bank_ - amount

        if self.collection.find_one({"_id": ctx.author.id})["Bank"] < amount:
            embed = Embed(title="Error!", description=f"Sorry {ctx.author.mention} You can't withdraw because you don't have that much money in the bank.", color=self.color)
            return await ctx.send(embed=embed)

        self.collection.update_one({"_id": ctx.author.id}, {"$set": {"Bank": remove_coins}})
        self.collection.update_one({"_id": ctx.author.id}, {"$set": {"coins": total_coins}})

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

        while True:
            if emoji == '✅':
                if random == "https://im-a-dev.xyz/QqoZ2M6m.png":
                    user_coin = Wealth.fetch_user(ctx.author.id, "coins")

                    user_coin = result["coins"]

                    amount_won = user_coin + 250

                    self.collection.update_one({"_id": ctx.author.id}, {"$set": {"coins": amount_won}})

                    await message.delete()
                    return await ctx.send(f"Hey {ctx.author.mention} you caught World in the act! and have earned a total of `250` coins. Well done!")
                else:
                    await message.delete()
                    return await ctx.send(f"Sorry {ctx.author.mention} you chose the wrong one! try again next time.")

            if emoji == '❎':
                if random == "https://im-a-dev.xyz/BvdekLII.png":
                    user_coin = Wealth.fetch_user(ctx.author.id, "coins")

                    user_coin = result["coins"]

                    amount_won = user_coin + 100

                    self.collection.update_one({"_id": ctx.author.id}, {"$set": {"coins": amount_won}})

                    await message.delete()
                    return await ctx.send(f"Hey {ctx.author.mention} you have found innocent World! and have earned a total of `100` coins. Well done!")
                else:
                    await message.delete()
                    return await ctx.send(f"Sorry {ctx.author.mention} you chose the wrong one! try again next time.")

            if emoji == '🚫':
                if random == "https://im-a-dev.xyz/MfSnYYAa.png":
                    await message.delete()
                    return await ctx.send(f"Hey {ctx.author.mention} you found nothing...")
                else:
                    await message.delete()
                    return await ctx.send(f"Sorry {ctx.author.mention} you chose the wrong one! try again next time.")
            try:
                res = await self.bot.wait_for('reaction_add', check=lambda r, u: u.id == ctx.author.id and r.message.id == message.id, timeout=4)

                if not res:
                    break

                if str(res[1])!='World#4520':
                    emoji=str(res[0].emoji)

            except:
                await message.delete()
                return await ctx.send(f"Sorry {ctx.author.mention} you werent fast enough and World got away...")

        await message.clear_reactions()

    @shootout.error
    async def shootout_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            a = error.retry_after
            a = round(a)
            await ctx.send(f"Sorry {ctx.author.mention} This command in on cooldown, Try again in {a} seconds.")


    @commands.command(help="Fish for things in the lake", aliases=["fish", "worldfishing"])
    @commands.cooldown(rate=1, per=120, type=commands.BucketType.member)
    async def fishing(self, ctx):
        if not (Wealth._has_account(ctx.author.id)):
            Wealth._create_account(ctx.author.id)

        random = Wealth.fishing_ran()

        if random == "https://im-a-dev.xyz/1kKJXQSr.png":
            embed = Embed(title="Fishing", description="There are no fish in the lake right now, come again soon!", color=self.color)
            embed.set_image(url="https://im-a-dev.xyz/1kKJXQSr.png")
            return await ctx.send(embed=embed)

        if random == "https://im-a-dev.xyz/ImWqkaSy.png":
            user_fish = Wealth.fetch_user(ctx.author.id, "Fish")

            new_amount = user_fish + int(1)

            self.collection.update_one({"_id": ctx.author.id}, {"$set": {"Fish": new_amount}})

            embed = Embed(title="Fishing", description=f"Great, looks like you have caught a fish! you now have a total of `{new_amount}` Fish!", color=self.color)
            embed.set_image(url="https://im-a-dev.xyz/ImWqkaSy.png")
            return await ctx.send(embed=embed)

        if random == "https://im-a-dev.xyz/sqPSfhJJ.png":
            user_cookie = Wealth.fetch_user(ctx.author.id, "cookie")

            box_cookies = user_cookie + int(5)

            self.collection.update_one({"_id": ctx.author.id}, {"$set": {"cookie": box_cookies}})

            embed = Embed(title="Fishing", description=f"Wow, you caught a box of cookies while fishing?! you now have a total of `{box_cookies}` Cookies!", color=self.color)
            embed.set_image(url="https://im-a-dev.xyz/sqPSfhJJ.png")
            return await ctx.send(embed=embed)

        if random == "https://im-a-dev.xyz/syTQUdrV.png":
            user_coin = Wealth.fetch_user(ctx.author.id, "coins")

            random_coins = randint(1, 50)

            bagof_coins = user_coin + random_coins

            self.collection.update_one({"_id": ctx.author.id}, {"$set": {"coins": bagof_coins}})

            embed = Embed(title="Fishing", description=f"Wow, you caught a bag of coins while fishing?!\nCoins in the bag: `{random_coins}`\nyou now have a total of `{bagof_coins}` Coins!", color=self.color)
            embed.set_image(url="https://im-a-dev.xyz/syTQUdrV.png")
            return await ctx.send(embed=embed)


    @fishing.error
    async def fishing_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            a = error.retry_after
            a = round(a)
            await ctx.send(f"Sorry {ctx.author.mention} This command in on cooldown, Try again in {a} seconds.")


    @commands.command(help="What badges do you have?", aliases=["mybadges", "showbadges", "badge"])
    async def badges(self, ctx):
        if not (Wealth._has_account(ctx.author.id)):
            await Wealth._create_account(ctx.author.id)

        result = Wealth.mass_fetch(ctx.author.id)

        noob = result["BadgeSlot1"]
        beginner = result["BadgeSlot2"]
        leader = result["BadgeSlot3"]

        embed = Embed(title="Your badges", description=f"Noob: {noob}\nBeginner: {beginner}\nLeader: {leader}\n\n[`Noob`](https://cdn.discordapp.com/emojis/779192872402026516.png?v=1) | [`Beginner`](https://cdn.discordapp.com/emojis/779192938617241600.png?v=1) | [`Leader`](https://cdn.discordapp.com/emojis/779193003024973835.png?v=1)", color=self.color)
        await ctx.send(embed=embed)


    @commands.command(help="Show your reputation", aliases=["myrep", "myreputation", "reputationcount"])
    async def repcount(self, ctx):
        if not (Wealth._has_account(ctx.author.id)):
            await Wealth._create_account(ctx.author.id)

        rep = Wealth.fetch_user(ctx.author.id, "Reputation")

        embed = Embed(title="Your Reputation", description=f"Reputation Points: `{rep}`", color=self.color)
        await ctx.send(embed=embed)

    @commands.command(help="Show your World status", aliases=["mystat", "worldstatus"])
    async def mystatus(self, ctx):
        if not (Wealth._has_account(ctx.author.id)):
            await Wealth._create_account(ctx.author.id)

        status = Wealth.fetch_user(ctx.author.id, "afk")

        embed = Embed(title="Your Status", description=f"World status: `{status}`",color=self.color)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(EconomyFunCog(bot))