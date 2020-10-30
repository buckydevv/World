import discord
import pymongo
import os
import datetime

from discord.ext.commands import command
from discord.ext import commands
from discord.ext.commands import Cog
from pymongo import MongoClient
from datetime import datetime

now = datetime.now()

cluster = MongoClient(os.environ["MONGODB_URL"])
    		
db = cluster["EconomyFun"]
collection = db["Reputation"]


class EconomyFunCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Add reputation points to a user.", aliases=["rep"])
    @commands.cooldown(rate=1, per=1800, type=commands.BucketType.member)
    async def reputation(self, ctx, user: discord.Member):
    	if user.id == ctx.author.id:
    		return await ctx.send(f"Sorry {ctx.author.mention} You cant give yourself a reputation point.")
    	if not collection.find_one({"_id": user.id}):
    		rep_account = {
    		"_id": user.id,
    		"Reputation": 0,
    		"LastUsed": "Isnotset",
    		"TargetMember": 0,
    		}
    		collection.insert_one(rep_account)
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



def setup(bot):
    bot.add_cog(EconomyFunCog(bot))
