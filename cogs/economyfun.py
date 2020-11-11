import discord
import pymongo
import os
import textwrap
import datetime
import asyncio
import motor.motor_asyncio
import typing
import random

from discord.ext.commands import command
from discord.ext import commands
from discord.ext.commands import Cog
from pymongo import MongoClient
from datetime import datetime
from typing import Optional
from asyncio import TimeoutError


cluster = MongoClient(os.environ["MONGODB_URL"])
            
db = cluster["Coins"]
collection = db["UserCoins"]



class EconomyFunCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

## Reputation Start ##

    @commands.command(help="Add reputation points to a user.", aliases=["rep"])
    @commands.cooldown(rate=1, per=1800, type=commands.BucketType.member)
    async def reputation(self, ctx, user: discord.Member):
        now = datetime.now()
        if user.id == ctx.author.id:
            return await ctx.send(f"Sorry {ctx.author.mention} You cant give yourself a reputation point.")
        if not (await self._has_account(ctx.author.id)):
            await self._create_account(ctx.author.id)
            query = {"_id": user.id}
            rep_ = collection.find(query)
            post = {"Reputation": user.id}
            for result in rep_:
                _rep = result["Reputation"]
                reputation_point = int(1) + _rep
                last_used = str(now.strftime("%m/%d/%Y, %H:%M:%S"))
                collection.update_one({"_id": user.id}, {"$set": {"Reputation": reputation_point}})
                collection.update_one({"_id": ctx.author.id}, {"$set": {"TargetMember": user.id}})
                collection.update_one({"_id": ctx.author.id}, {"$set": {"LastUsed": last_used}})
                embed = discord.Embed(title="Reputation", description=f"{ctx.author.mention} You added `1+` Reputation to {user.mention}", color=0x2F3136)
                await ctx.send(embed=embed)
        elif collection.find_one({"_id": user.id}):
            query = {"_id": user.id}
            rep_ = collection.find(query)
            post = {"Reputation": user.id}
            for result in rep_:
                _rep = result["Reputation"]
                reputation_point = int(1) + _rep
                last_used = str(now.strftime("%m/%d/%Y, %H:%M:%S"))
                collection.update_one({"_id": user.id}, {"$set": {"Reputation": reputation_point}})
                collection.update_one({"_id": ctx.author.id}, {"$set": {"TargetMember": user.id}})
                collection.update_one({"_id": ctx.author.id}, {"$set": {"LastUsed": last_used}})
                embed = discord.Embed(title="Reputation", description=f"{ctx.author.mention} You added `1+` Reputation to {user.mention}", color=0x2F3136)
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
        if not (await self._has_account(ctx.author.id)):
            await self._create_account(ctx.author.id)
        now = datetime.now()
        if not collection.find_one({"_id": ctx.author.id}):
            return await ctx.send(f"Sorry {ctx.author.mention} you havent gave anyone a rep point!\nTry using the command `rep` to give a reputation point to someone you think deserves it.")
        if collection.find_one({"_id": ctx.author.id})["LastUsed"] == "Isnotset":
            return await ctx.send(f"Sorry {ctx.author.mention} you havent gave anyone a rep point!\nTry using the command `rep` to give a reputation point to someone you think deserves it.")
        query = {"_id": ctx.author.id}
        rep_ = collection.find(query)
        post = {"Reputation": ctx.author.id}
        for result in rep_:
            last_used = result["LastUsed"]
            target_user = result["TargetMember"]
            embed = discord.Embed(
                title="Last Reputation",
                description=f"{ctx.author.mention} You gave <@{target_user}> `1` Reputation point\nDate: `{last_used}`",
                color=0x2F3136
                )
            await ctx.send(embed=embed)

## Reputation End ##

## Profile Start ##

    @commands.command()
    async def profile(self, ctx, user: discord.Member=None):
        if not (await self._has_account(ctx.author.id)):
            await self._create_account(ctx.author.id)
        user = user or ctx.author
        query = {"_id": user.id}
        prof = collection.find(query)
        for result in prof:
            coins = result["coins"]
            rep = result["Reputation"]
            afk = result["afk"]
            cookie = result["cookie"]
            poop = result["poop"]
            apple = result["apple"]
            chocolate = result["choc"]
            created = result["AccountCreated"]
            last_trans = result["LastTransfer"]
            noob_b = result["BadgeSlot1"]
            beginner_b = result["BadgeSlot2"]
            leader_b = result["BadgeSlot3"]
            marry = result["MarriedTo"]
            bank_ = result["Bank"]
            beans = result["beans"]
            pizzas = result["pizza"]
            waffles = result["waffles"]
            fish = result["Fish"]
            page1 = discord.Embed(
                title='Page 1/3',
                description=f"{user}'s Profile",
                colour=0x2F3136
                ).add_field(
                name="<:memberlogo:765649915031846912> | Account",
                value=f"Account Type: `World Account`\nCoins: `{coins:.2f}`\nBank: `{bank_}`\nReputation: `{rep}`\nStatus: `{afk}`"
                )

            page2 = discord.Embed(
                title='Page 2/3',
                description=f"{user}'s Profile",
                colour=0x2F3136
                ).add_field(
                name=":handbag: | Inventory",
                value=f":cookie: Cookies: `{cookie}`\n:chocolate_bar: Chocbars: `{chocolate}`\n:apple: Apples: `{apple}`\n:poop: Poop: `{poop}`\n<:beanworld:774371828629635132> Beans: `{beans}`\n:pizza: Pizza: `{pizzas}`\n:waffle: Waffles `{waffles}`\n:fish: Fish: `{fish}`"
                )

            page3 = discord.Embed(
                title="Page 3/3",
                description=f"{user}'s Profile",
                colour=0x2F3136
                ).add_field(
                name="<:shufflelogo:765652804387471430> | Other",
                value=f"Created World Account: `{created}`\nYour Last Transfer: `{last_trans}`\nMarried to: `{marry}`\nBadges:\n{noob_b} Badge\n{beginner_b} Badge\n{leader_b} Badge"
                )

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
                except TimeoutError:
                    await message.clear_reactions()
                    break
                if res == None:
                    break
                if str(res[1])!='World#4520':
                    emoji=str(res[0].emoji)

            await message.clear_reactions()

## PROFILE FINISH ##

## Badges Start ##

    @commands.command(help="Badge Shop!", aliases=["bshop"])
    async def badgeshop(self, ctx):
        embed = discord.Embed(
            title="World Badge Shop!",
            description=textwrap.dedent("""
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
        if not (await self._has_account(ctx.author.id)):
            await self._create_account(ctx.author.id)
        query = {"_id": ctx.author.id}
        a_ = collection.find(query)
        for result in a_:
            if item.lower() == "noob":
                noob_b = result["BadgeSlot1"] # Nooob badge
                user_coins = result["coins"]
                cost_of_b = int(900)
                total_cost = user_coins - cost_of_b
                if collection.find_one({"_id": ctx.author.id})["coins"] < 900:
                    embed = discord.Embed(title="Error!", description=f"Sorry {ctx.author.mention} You dont have enough coins to buy `World Noob Badge`")
                    return await ctx.send(embed=embed)
                if collection.find_one({"_id": ctx.author.id})["BadgeSlot1"] == "<:WorldBadge1:772220840007565362>":
                    embed = discord.Embed(title="Error!", description=f"Sorry {ctx.author.mention} You already have `World Noob Badge`.")
                    return await ctx.send(embed=embed)
                collection.update_one({"_id": ctx.author.id}, {"$set": {"coins": total_cost}})
                collection.update_one({"_id": ctx.author.id}, {"$set": {"BadgeSlot1": "<:WorldBadge1:772220840007565362>"}})
                embed = discord.Embed(
                    title="World Badge",
                    description="You have bought `World Noob Badge` for `900` Coins. <:WorldBadge1:772220840007565362>",
                    color=0x2F3136
                    )
                await ctx.send(embed=embed)
            if item.lower() == "beginner":
                noob_b2 = result["BadgeSlot2"] # Beginner badge
                user_coins2 = result["coins"]
                cost_of_b2 = int(3500)
                total_cost2 = user_coins2 - cost_of_b2
                if collection.find_one({"_id": ctx.author.id})["coins"] < 3500:
                    embed = discord.Embed(title="Error!", description=f"Sorry {ctx.author.mention} You dont have enough coins to buy `World Beginner Badge`")
                    return await ctx.send(embed=embed)
                if collection.find_one({"_id": ctx.author.id})["BadgeSlot2"] == "<:WorldBadge2:772227094125477910>":
                    embed = discord.Embed(title="Error!", description=f"Sorry {ctx.author.mention} You already have `World Beginner Badge`.")
                    return await ctx.send(embed=embed)
                collection.update_one({"_id": ctx.author.id}, {"$set": {"coins": total_cost2}})
                collection.update_one({"_id": ctx.author.id}, {"$set": {"BadgeSlot2": "<:WorldBadge2:772227094125477910>"}})
                embed = discord.Embed(
                    title="World Badge",
                    description="You have bought `World Beginner Badge` for `3,500` Coins. <:WorldBadge2:772227094125477910>",
                    color=0x2F3136
                    )
                await ctx.send(embed=embed)
            if item.lower() == "leader":
                noob_b3 = result["BadgeSlot3"] # Leader badge
                user_coins3 = result["coins"]
                cost_of_b3 = int(9500)
                total_cost3 = user_coins3 - cost_of_b3
                if collection.find_one({"_id": ctx.author.id})["coins"] < 9500:
                    embed = discord.Embed(title="Error!", description=f"Sorry {ctx.author.mention} You dont have enough coins to buy `World Leader Badge`")
                    return await ctx.send(embed=embed)
                if collection.find_one({"_id": ctx.author.id})["BadgeSlot2"] == "<:WorldBadge3:772228285488168980>":
                    embed = discord.Embed(title="Error!", description=f"Sorry {ctx.author.mention} You already have `World Leader Badge`.")
                    return await ctx.send(embed=embed)
                collection.update_one({"_id": ctx.author.id}, {"$set": {"coins": total_cost3}})
                collection.update_one({"_id": ctx.author.id}, {"$set": {"BadgeSlot3": "<:WorldBadge3:772228285488168980>"}})
                embed = discord.Embed(
                    title="World Badge",
                    description="You have bought `World Leader Badge` for `9,500` Coins. <:WorldBadge3:772228285488168980>",
                    color=0x2F3136
                    )
                await ctx.send(embed=embed)

    @buybadge.error
    async def buybadge_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/buybadge <BadgeName>`")

## Badges end ##

## Marry Start ##

    @commands.command(help="Marry a specified user!")
    @commands.cooldown(rate=1, per=120, type=commands.BucketType.member)
    async def marry(self, ctx, user: discord.Member):
        if not (await self._has_account(ctx.author.id)):
            await self._create_account(ctx.author.id)
        now = datetime.now()
        m_date = str(now.strftime("%m/%d/%Y"))
        if user == ctx.author:
            return await ctx.send(f"Sorry {ctx.author.mention} but you can't marry yourself!")
        query = {"_id": ctx.author.id}
        mar_ = collection.find(query)
        for result in mar_:
            Marriedto_ = result["MarriedTo"]
            MarriedDate = result["MarriedDate"]
            if collection.find_one({"_id": ctx.author.id})["MarriedTo"] == str(user):
                embed = discord.Embed(title="Error!", description=f"Sorry {ctx.author.mention} You're already married to `{user}`.")
                return await ctx.send(embed=embed)
            msg = await ctx.send(f"Hey {user.mention} {ctx.author.mention} wants to marry you.\nPlease react.")
            emoji = ''
            await msg.add_reaction('☑')
            await msg.add_reaction('❎')
            try:
                res = await self.bot.wait_for('reaction_add', check=lambda r, u: u.id == user.id and r.message.id == msg.id, timeout=13)
            except TimeoutError:
                    await msg.clear_reactions()
                    break
            if str(res[1])!='World#4520':
                emoji=str(res[0].emoji)
            if emoji == "☑":
                collection.update_one({"_id": ctx.author.id}, {"$set": {"MarriedTo": str(user)}})
                collection.update_one({"_id": ctx.author.id}, {"$set": {"MarriedDate": str(m_date)}})
                collection.update_one({"_id": user.id}, {"$set": {"MarriedTo": str(ctx.author)}})
                collection.update_one({"_id": user.id}, {"$set": {"MarriedDate": str(m_date)}})
                embed = discord.Embed(title="Marry", description=f"{ctx.author.mention} has married {user.mention}", color=0x2F3136)
                await msg.delete()
                return await ctx.send(embed=embed)
            if emoji == "❎":
                await msg.delete()
                embed = discord.Embed(title="Marry", description=f"{user.mention} didn't want to marry {ctx.author.mention}", color=0x2F3136)
                return await ctx.send(embed=embed)

    @marry.error
    async def marry_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/marry <@user>`")
        if isinstance(error, commands.CommandOnCooldown):
            a = error.retry_after
            a = round(a)
            await ctx.send(f"Sorry {ctx.author.mention} This command in on cooldown, Try again in {a} seconds.")

## Marry End!

## Divorce Start ##

    @commands.command(help="Divorce a specified user!")
    @commands.cooldown(rate=1, per=120, type=commands.BucketType.member)
    async def divorce(self, ctx, user: discord.Member):
        if not (await self._has_account(ctx.author.id)):
            await self._create_account(ctx.author.id)
        if user == ctx.author:
            return await ctx.send(f"Sorry {ctx.author.mention} but you can't divorce yourself!")
        query = {"_id": ctx.author.id}
        mar_ = collection.find(query)
        for result in mar_:
            Marriedto_ = result["MarriedTo"]
            MarriedDate = result["MarriedDate"]
            if collection.find_one({"_id": ctx.author.id})["MarriedTo"] == "Nobody":
                embed = discord.Embed(title="Error!", description=f"Sorry {ctx.author.mention} You are not married yet!.")
                return await ctx.send(embed=embed)
            if not collection.find_one({"_id": ctx.author.id})["MarriedTo"] == str(user):
                embed = discord.Embed(title="Error!", description=f"Sorry {ctx.author.mention} You're not married to {user}.")
                return await ctx.send(embed=embed)
            collection.update_one({"_id": ctx.author.id}, {"$set": {"MarriedTo": "Nobody"}})
            collection.update_one({"_id": user.id}, {"$set": {"MarriedTo": "Nobody"}})
            collection.update_one({"_id": user.id}, {"$set": {"MarriedDate": "No date"}})
            embed = discord.Embed(title="Divorce", description=f"{ctx.author.mention} has divorced {user.mention}", color=0x2F3136)
            return await ctx.send(embed=embed)


    @divorce.error
    async def divorce_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/divorce <@user>`")
        if isinstance(error, commands.CommandOnCooldown):
            a = error.retry_after
            a = round(a)
            await ctx.send(f"Sorry {ctx.author.mention} This command in on cooldown, Try again in {a} seconds.")

## Divorce end ##

## Bank start ##

    @commands.command(help="Deposit money into your World bank account", aliases=["dep"])
    async def deposit(self, ctx, amount: int):
        if not (await self._has_account(ctx.author.id)):
            await self._create_account(ctx.author.id)
        if amount < 0:
            return await ctx.send(f"Sorry {ctx.author.mention} No signed integers or 0!")
        query = {"_id": ctx.author.id}
        dep_ = collection.find(query)
        for result in dep_:
            bank_ = result["Bank"]
            coins_ = result["coins"]
            remove_coins = coins_ - amount
            total_coins = bank_ + amount
            if collection.find_one({"_id": ctx.author.id})["coins"] < amount:
                embed = discord.Embed(title="Error!", description=f"Sorry {ctx.author.mention} You can't deposit because you don't have that much money.")
                return await ctx.send(embed=embed)
            collection.update_one({"_id": ctx.author.id}, {"$set": {"Bank": total_coins}})
            collection.update_one({"_id": ctx.author.id}, {"$set": {"coins": remove_coins}})
            embed = discord.Embed(title="Deposit", description=f"{ctx.author.mention} you have just deposited `{amount}` coins.", color=0x2F3136)
            await ctx.send(embed=embed)

    @commands.command(help="Withdraw money from your World bank account.", aliases=["with"])
    async def withdraw(self, ctx, amount: int):
        if not (await self._has_account(ctx.author.id)):
            await self._create_account(ctx.author.id)
        if amount < 0:
            return await ctx.send(f"Sorry {ctx.author.mention} No signed integers or 0!")
        query = {"_id": ctx.author.id}
        with_ = collection.find(query)
        for result in with_:
            bank_ = result["Bank"]
            coins_ = result["coins"]
            total_coins = coins_ + amount
            remove_coins = bank_ - amount
            if collection.find_one({"_id": ctx.author.id})["Bank"] < amount:
                embed = discord.Embed(title="Error!", description=f"Sorry {ctx.author.mention} You can't withdraw because you don't have that much money in the bank.")
                return await ctx.send(embed=embed)
            collection.update_one({"_id": ctx.author.id}, {"$set": {"Bank": remove_coins}})
            collection.update_one({"_id": ctx.author.id}, {"$set": {"coins": total_coins}})
            embed = discord.Embed(title="Withdraw", description=f"{ctx.author.mention} you have just withdrawn `{amount}` coins.", color=0x2F3136)
            await ctx.send(embed=embed)

    @deposit.error
    async def deposit_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/deposit <amount>`")


    @withdraw.error
    async def withdraw_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/withdraw <amount>`")

## Bank end ##

## Owner section ##

    @commands.command(help="Sorry Buddy only owner.")
    @commands.is_owner()
    async def givecoin(self, ctx, users: discord.Member, *, coin):
        query = {"_id": users.id}
        user = collection.find(query)
        for result in user:
            user_coin = result["coins"]
            total_coins = user_coins + coin
            collection.update_one({"_id": users.id}, {"$set": {"coins": total_coins}})
            embed1 = discord.Embed(
                title="Success!"
                ).add_field(
                name=f"Complete", 
                value=f"{ctx.author.mention} I Have Added `{coin}` Coins To {users.mention}'s Balance"
                )
            await ctx.send(embed=embed1)

    @commands.command(help="Only owner buddy.")
    @commands.is_owner()
    async def removecoin(self, ctx, users: discord.Member, *, coin):
        query = {"_id": users.id}
        user = collection.find(query)
        for result in user:
            user_coin = result["coins"]
            collection.update_one({"_id": users.id}, {"$set": {"coins":coins}})
            embed1 = discord.Embed(
                title="Success"
                ).add_field(
                name=f"Complete",
                value=f"{ctx.author.mention} I Have Removed `{coin}` Coins From {users.mention}'s Balance"
                )
            await ctx.send(embed=embed1)

## end of owner section

## Shootout start ##

    @commands.command(help="World shootout", aliases=["shoot", "worldshoot"])
    @commands.cooldown(rate=1, per=15, type=commands.BucketType.member)
    async def shootout(self, ctx):
    	await self._shootout_game(ctx)

    @shootout.error
    async def shootout_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            a = error.retry_after
            a = round(a)
            await ctx.send(f"Sorry {ctx.author.mention} This command in on cooldown, Try again in {a} seconds.")

## shootout end ##

## Fishing start ##

    @commands.command(help="Fish for things in the lake", aliases=["fish", "worldfishing"])
    @commands.cooldown(rate=1, per=120, type=commands.BucketType.member)
    async def fishing(self, ctx):
    	await self._fishing_world(ctx)

    @fishing.error
    async def fishing_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            a = error.retry_after
            a = round(a)
            await ctx.send(f"Sorry {ctx.author.mention} This command in on cooldown, Try again in {a} seconds.")

## Fishing end ##

## define section

    async def _fishing_world(self, ctx: commands.Context):
    	fishing_idle = "https://im-a-dev.xyz/1kKJXQSr.png"
    	caught_fish = "https://im-a-dev.xyz/ImWqkaSy.png"
    	caught_cookies = "https://im-a-dev.xyz/sqPSfhJJ.png"
    	caught_coins = "https://im-a-dev.xyz/syTQUdrV.png"

    	randomize = [fishing_idle, caught_fish, caught_cookies, caught_coins]
    	random_choice = random.choice(randomize)

    	if random_choice == "https://im-a-dev.xyz/1kKJXQSr.png":
    		embed = discord.Embed(
    			title="Fishing",
    			description="There are no fish in the lake right now, come again soon!",
    			color=0x2F3136
    			)
    		embed.set_image(url="https://im-a-dev.xyz/1kKJXQSr.png")
    		return await ctx.send(embed=embed)

    	if random_choice == "https://im-a-dev.xyz/ImWqkaSy.png":
    		query = {"_id": ctx.author.id}
    		user = collection.find(query)
    		for result in user:
    			user_fish = result["Fish"]
    			new_amount = user_fish + int(1)
    			collection.update_one({"_id": ctx.author.id}, {"$set": {"Fish": new_amount}})
    			embed = discord.Embed(
    				title="Fishing",
    				description=f"Great, looks like you have caught a fish! you now have a total of `{new_amount}` Fish!",
    				color=0x2F3136
    				)
    			embed.set_image(url="https://im-a-dev.xyz/ImWqkaSy.png")
    			return await ctx.send(embed=embed)

    	if random_choice == "https://im-a-dev.xyz/sqPSfhJJ.png":
    		query = {"_id": ctx.author.id}
    		user = collection.find(query)
    		for result in user:
    			user_cookie = result["cookie"]
    			box_cookies = user_cookie + int(5)
    			collection.update_one({"_id": ctx.author.id}, {"$set": {"cookie": box_cookies}})
    			embed = discord.Embed(
    				title="Fishing",
    				description=f"Wow, you caught a box of cookies while fishing?! you now have a total of `{box_cookies}` Cookies!",
    				color=0x2F3136
    				)
    			embed.set_image(url="https://im-a-dev.xyz/sqPSfhJJ.png")
    			return await ctx.send(embed=embed)

    	if random_choice == "https://im-a-dev.xyz/syTQUdrV.png":
    		query = {"_id": ctx.author.id}
    		user = collection.find(query)
    		for result in user:
    			user_coin = result["coins"]
    			random_coins = random.randint(1, 50)
    			bagof_coins = user_coin + random_coins
    			collection.update_one({"_id": ctx.author.id}, {"$set": {"coins": bagof_coins}})
    			embed = discord.Embed(
    				title="Fishing",
    				description=f"Wow, you caught a bag of coins while fishing?!\nCoins in the bag: `{random_coins}`\nyou now have a total of `{bagof_coins}` Coins!",
    				color=0x2F3136
    				)
    			embed.set_image(url="https://im-a-dev.xyz/syTQUdrV.png")
    			return await ctx.send(embed=embed)

    async def _shootout_game(self, ctx: commands.Context):
    	shooter_world = "https://im-a-dev.xyz/QqoZ2M6m.png"
    	normal_world = "https://im-a-dev.xyz/BvdekLII.png"
    	nothing_world = "https://im-a-dev.xyz/MfSnYYAa.png"

    	all_worlds = [shooter_world, normal_world, nothing_world]

    	random_choice = random.choice(all_worlds)

    	embed = discord.Embed(title="Shootout", description="Is World a shooter?", color=0x2F3136)
    	embed.set_image(url=random_choice)
    	embed.set_footer(text="|✅ - shooter|❎ - innocent|🚫 - nothing")
    	message = await ctx.send(embed=embed)

    	await message.add_reaction('✅')
    	await message.add_reaction('❎')
    	await message.add_reaction('🚫')

    	emoji = ''

    	while True:
    		if emoji == '✅':
    			if random_choice == "https://im-a-dev.xyz/QqoZ2M6m.png":
    				query = {"_id": ctx.author.id}
    				user = collection.find(query)
    				for result in user:
    					user_coin = result["coins"]
    					amount_won = user_coin + 250
    					collection.update_one({"_id": ctx.author.id}, {"$set": {"coins": amount_won}})
    					await message.delete()
    					return await ctx.send(f"Hey {ctx.author.mention} you caught World in the act! and have earned a total of `250` coins. Well done!")
    			else:
    				await message.delete()
    				return await ctx.send(f"Sorry {ctx.author.mention} you chose the wrong one! try again next time.")
    		if emoji == '❎':
    			if random_choice == "https://im-a-dev.xyz/BvdekLII.png":
    				query = {"_id": ctx.author.id}
    				user = collection.find(query)
    				for result in user:
    					user_coin = result["coins"]
    					amount_won = user_coin + 100
    					collection.update_one({"_id": ctx.author.id}, {"$set": {"coins": amount_won}})
    					await message.delete()
    					return await ctx.send(f"Hey {ctx.author.mention} you have found innocent World! and have earned a total of `100` coins. Well done!")
    			else:
    				await message.delete()
    				return await ctx.send(f"Sorry {ctx.author.mention} you chose the wrong one! try again next time.")
    		if emoji == '🚫':
    			if random_choice == "https://im-a-dev.xyz/MfSnYYAa.png":
    				await message.delete()
    				return await ctx.send(f"Hey {ctx.author.mention} you found nothing...")
    			else:
    				await message.delete()
    				return await ctx.send(f"Sorry {ctx.author.mention} you chose the wrong one! try again next time.")
    		try:
    			res = await self.bot.wait_for('reaction_add', check=lambda r, u: u.id == ctx.author.id and r.message.id == message.id, timeout=4)
    			if res==None:
    				break
    			if str(res[1])!='Luffy#0728':
    				emoji=str(res[0].emoji)
    		except TimeoutError:
    			await message.delete()
    			return await ctx.send(f"Sorry {ctx.author.mention} you werent fast enough and World got away...")

    	await message.clear_reactions()



    async def _create_account(self, user_id: int) -> None:
        """Create a World account."""
        now = datetime.now()
        _created_at = str(now.strftime("%m/%d/%Y at %H:%M:%S"))
        collection.insert_one({
            "_id": user_id,
            "coins": 100,
            "cookie": 0,
            "choc": 0,
            "poop": 0,
            "beans": 0,
            "pizza": 0,
            "waffles": 0,
            "Fish": 0,
            "apple": 0,
            "afk": "No status set, run w/status to set a status",
            "Reputation": 0,
            "LastUsed": "Isnotset",
            "TargetMember": 0,
            "BadgeSlot1": "Doesn't Have Noob",
            "BadgeSlot2": "Doesn't Have Beginner",
            "BadgeSlot3": "Doesn't Have Leader",
            "AccountCreated": _created_at,
            "Premium": "No",
            "Developer": "No",
            "Bank": 0,
            "Wallet": 0,
            "Tickets": 0,
            "TicketReason": "No reason",
            "WorldFriends": 0,
            "IsBlacklisted": "No",
            "CurrentJob": "No job",
            "LastWithdraw": "No date",
            "LastTransfer": "No date",
            "MarriedTo": "Nobody",
            "MarriedDate": "No date",
        })

    async def _has_account(self, user_id: int) -> None:
        """Returns True if the user_id has an account. Otherwise False."""
        return bool(collection.find_one(
            {"_id": user_id}
        ))

## end of define section

def setup(bot):
    bot.add_cog(EconomyFunCog(bot))
