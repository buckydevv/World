import discord

from os import environ
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
from io import BytesIO
from typing import Optional
from twemoji_parser import TwemojiParser
from discord import TextChannel
from pymongo import MongoClient
from discord.ext import commands
from urllib.parse import urlparse, quote
from discord.ext.commands import has_permissions, MissingPermissions
from dotenv import load_dotenv
from discord import Embed
from datetime import datetime

load_dotenv()

cluster = MongoClient(environ["MONGODB_URL"])

class LoggingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = 0x2F3136
        self.collection = cluster["Logging"]["Guilds"]

    @commands.group(name="logging")
    async def logging(self, ctx):
        if ctx.invoked_subcommand is None:
            return await ctx.send(f"Sorry {ctx.author.mention} please type `w/logging <command>`")

    @logging.command(name="create")
    @commands.has_permissions(administrator=True)
    async def create(self, ctx):
        try:
            await self._create_guild_account(ctx.guild.id)

            embed = Embed(title="Logging", description=f"I have succsesfully setup logging for `{ctx.guild.name}`.", color=self.color)
            await ctx.send(embed=embed)
        except:
            embed = Embed(title="Logging", description=f"Sorry {ctx.author.mention} your guild already has a logging system setup!", color=self.color)
            return await ctx.send(embed=embed)

    @create.error
    async def create_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(f'Sorry {ctx.author.mention} you don\'t have the permissions to do this!')

    @logging.command(name="shutdown", aliases=["delete"])
    @commands.has_permissions(administrator=True)
    async def shutdown(self, ctx):
        if not (await self._has_guild_account(ctx.guild.id)):
            embed = Embed(title="Shutdown", description=f"Hey {ctx.author.mention} your guild was not found.\nTry using: `w/logging create`", color=self.color)
            return await ctx.send(embed=embed)

        self.collection.remove({"_id": ctx.guild.id})
        embed = Embed(title="Shutdown", description=f"Hey {ctx.author.mention} i have succsesfully removed your guild's account.", color=self.color)
        await ctx.send(embed=embed)

    @shutdown.error
    async def shutdown_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(f'Sorry {ctx.author.mention} you don\'t have the permissions to do this!')

    @logging.command(name="bans", aliases=["discordbans", "banlog"])
    @commands.has_permissions(administrator=True)
    async def bans(self, ctx, channel: TextChannel):
        if not (await self._has_guild_account(ctx.guild.id)):
            await self._create_guild_account(ctx.guild.id)
        query = {"_id": ctx.guild.id}
        res = self.collection.find(query)
        for result in res:
            if self.collection.find_one({"_id": ctx.guild.id})["Bans"] == channel.id:
                embed = discord.Embed(title="Logging", description=f"Sorry {ctx.author.mention} <#{channel.id}> has already been set as your `Ban Log`.", color=self.color)
                return await ctx.send(embed=embed)
            ban = result["Bans"]
            banresult = int(channel.id)
            self.collection.update_one({"_id": ctx.guild.id}, {"$set": {"Bans": banresult}})
            embed = Embed(title="Logging", description=f"{ctx.author.mention} I have succsesfully updated your `Ban Log` to the channel: <#{channel.id}>", color=self.color)
            await ctx.send(embed=embed)

    @bans.error
    async def bans_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/logging bans <channel>`")
        elif isinstance(error, commands.CheckFailure):
            await ctx.send(f'Sorry {ctx.author.mention} you don\'t have the permissions to do this!')

    @logging.command(name="unban", aliases=["discordunban", "unbanlog", "unbanslog", "unbans"])
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, channel: TextChannel):
    	if not (await self._has_guild_account(ctx.guild.id)):
    		await self._create_guild_account(ctx.guild.id)
    	query = {"_id": ctx.guild.id}
    	res = self.collection.find(query)
    	for result in res:
            if self.collection.find_one({"_id": ctx.guild.id})["Unbanned"] == channel.id:
                embed = discord.Embed(title="Logging", description=f"Sorry {ctx.author.mention} <#{channel.id}> has already been set as your `Unban Log`.", color=self.color)
                return await ctx.send(embed=embed)
            unban = result["Unbanned"]
            unbanresult = int(channel.id)
            self.collection.update_one({"_id": ctx.guild.id}, {"$set": {"Unbanned": unbanresult}})
            embed = Embed(title="Logging", description=f"{ctx.author.mention} I have succsesfully updated your `Unban Log` to the channel: <#{channel.id}>", color=self.color)
            await ctx.send(embed=embed)

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/logging unban <channel>`")
        elif isinstance(error, commands.CheckFailure):
            await ctx.send(f'Sorry {ctx.author.mention} you don\'t have the permissions to do this!')

    @logging.command(name="deleted", aliases=["discorddeleted", "delmsg"])
    @commands.has_permissions(administrator=True)
    async def deleted(self, ctx, channel: TextChannel):
    	if not (await self._has_guild_account(ctx.guild.id)):
    		await self._create_guild_account(ctx.guild.id)
    	query = {"_id": ctx.guild.id}
    	res = self.collection.find(query)
    	for result in res:
            if self.collection.find_one({"_id": ctx.guild.id})["DeletedMessage"] == channel.id:
                embed = discord.Embed(title="Logging", description=f"Sorry {ctx.author.mention} <#{channel.id}> has already been set as your `Deleted messages Log`.", color=self.color)
                return await ctx.send(embed=embed)
            delete = result["DeletedMessage"]
            delresult = int(channel.id)
            self.collection.update_one({"_id": ctx.guild.id}, {"$set": {"DeletedMessage": delresult}})
            embed = Embed(title="Logging", description=f"{ctx.author.mention} I have succsesfully updated your `Deleted messages Log` to the channel: <#{channel.id}>", color=self.color)
            await ctx.send(embed=embed)

    @deleted.error
    async def deleted_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/logging deleted <channel>`")
        elif isinstance(error, commands.CheckFailure):
            await ctx.send(f'Sorry {ctx.author.mention} you don\'t have the permissions to do this!')

    @logging.command(name="edited", aliases=["discordedited", "editmsg"])
    @commands.has_permissions(administrator=True)
    async def edited(self, ctx, channel: TextChannel):
    	if not (await self._has_guild_account(ctx.guild.id)):
    		await self._create_guild_account(ctx.guild.id)
    	query = {"_id": ctx.guild.id}
    	res = self.collection.find(query)
    	for result in res:
            if self.collection.find_one({"_id": ctx.guild.id})["EditedMessage"] == channel.id:
                embed = discord.Embed(title="Logging", description=f"Sorry {ctx.author.mention} <#{channel.id}> has already been set as your `Edited messages Log`.", color=self.color)
                return await ctx.send(embed=embed)
            edit = result["EditedMessage"]
            editresult = int(channel.id)
            self.collection.update_one({"_id": ctx.guild.id}, {"$set": {"EditedMessage": editresult}})
            embed = Embed(title="Logging", description=f"{ctx.author.mention} I have succsesfully updated your `Edited messages Log` to the channel: <#{channel.id}>", color=self.color)
            await ctx.send(embed=embed)

    @edited.error
    async def edited_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/logging edited <channel>`")
        elif isinstance(error, commands.CheckFailure):
            await ctx.send(f'Sorry {ctx.author.mention} you don\'t have the permissions to do this!')

    @logging.command(name="welcomes", aliases=["joiner", "joins", "join", "welcomemessages", "welcomemsg", "welcome"])
    @commands.has_permissions(administrator=True)
    async def welcomes(self, ctx, channel: TextChannel):
    	if not (await self._has_guild_account(ctx.guild.id)):
    		await self._create_guild_account(ctx.guild.id)
    	query = {"_id": ctx.guild.id}
    	res = self.collection.find(query)
    	for result in res:
            if self.collection.find_one({"_id": ctx.guild.id})["JoinedServer"] == channel.id:
                embed = discord.Embed(title="Logging", description=f"Sorry {ctx.author.mention} <#{channel.id}> has already been set as your `Welcome messages Log`.", color=self.color)
                return await ctx.send(embed=embed)
            join = result["JoinedServer"]
            joinresult = int(channel.id)
            self.collection.update_one({"_id": ctx.guild.id}, {"$set": {"JoinedServer": joinresult}})
            embed = Embed(title="Logging", description=f"{ctx.author.mention} I have succsesfully updated your `Welcome messsages Log` to the channel: <#{channel.id}>", color=self.color)
            await ctx.send(embed=embed)

    @welcomes.error
    async def welcomes_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/logging welcomes <channel>`")
        elif isinstance(error, commands.CheckFailure):
            await ctx.send(f'Sorry {ctx.author.mention} you don\'t have the permissions to do this!')

    @logging.command(name="goodbye", aliases=["memberleave", "bye", "leftserver", "leaving", "goodbyes"])
    @commands.has_permissions(administrator=True)
    async def goodbye(self, ctx, channel: TextChannel):
    	if not (await self._has_guild_account(ctx.guild.id)):
    		await self._create_guild_account(ctx.guild.id)
    	query = {"_id": ctx.guild.id}
    	res = self.collection.find(query)
    	for result in res:
            if self.collection.find_one({"_id": ctx.guild.id})["LeftServer"] == channel.id:
                embed = discord.Embed(title="Logging", description=f"Sorry {ctx.author.mention} <#{channel.id}> has already been set as your `Goodbye messages Log`.", color=self.color)
                return await ctx.send(embed=embed)
            leave = result["LeftServer"]
            leaveresult = int(channel.id)
            self.collection.update_one({"_id": ctx.guild.id}, {"$set": {"LeftServer": leaveresult}})
            embed = Embed(title="Logging", description=f"{ctx.author.mention} I have succsesfully updated your `Goodbye messsages Log` to the channel: <#{channel.id}>", color=self.color)
            await ctx.send(embed=embed)

    @goodbye.error
    async def goodbye_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/logging goodbye <channel>`")
        elif isinstance(error, commands.CheckFailure):
            await ctx.send(f'Sorry {ctx.author.mention} you don\'t have the permissions to do this!')

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        query = {"_id": guild.id}
        memberban = self.collection.find(query)
        post = {"Bans": 0}
        for result in memberban:
        	ban = result["Bans"]
        	if self.collection.find_one({"_id": guild.id})["Bans"] == 0:
        		return
        	else:
        		ban1 = await guild.fetch_ban(user)
        		print(ban1)
        		reason = ban1.reason
        		embed = discord.Embed(title="Ban Log", description=f"A user from this guild has been banned.\nName: `{user.name}`\nID: `{user.id}`\nReason: `{reason}`", timestamp=datetime.utcnow())
        		channel = self.bot.get_channel(ban)
        		await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        query = {"_id": guild.id}
        memberunban = self.collection.find(query)
        post = {"Unbanned": 0}
        for result in memberunban:
            unban = result["Unbanned"]
            if self.collection.find_one({"_id": guild.id})["Unbanned"] == 0:
                return
            else:
                embed = discord.Embed(title="Unban Log", description=f"A user from this guild has been unbanned.\nName: `{user.name}`\nID: `{user.id}`", timestamp=datetime.utcnow())
                channel = self.bot.get_channel(unban)
                await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        query = {"_id": message.guild.id}
        messagedelete = self.collection.find(query)
        post = {"DeletedMessage": 0}
        for result in messagedelete:
            deletedm = result["DeletedMessage"]
            if self.collection.find_one({"_id": message.guild.id})["DeletedMessage"] == 0:
                return
            else:
                embed = discord.Embed(title="Deleted message Log", description=f"A message was just deleted.\nContent: {message.content}\nUser: `{message.author}`\nChannel: `{message.channel}`", timestamp=datetime.utcnow())
                channel = self.bot.get_channel(deletedm)
                await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        query = {"_id": after.guild.id}
        editmessage = self.collection.find(query)
        post = {"EditedMessage": 0}
        for result in editmessage:
            editedm = result["EditedMessage"]
            if self.collection.find_one({"_id": after.guild.id})["EditedMessage"] == 0:
                return
            else:
                if before.content == after.content:
                    return
                beforec = (before.content)
                afterc = (after.content)
                for attachment in after.attachments:
                    return
                embed = discord.Embed(title="Edited message Log", description=f"A message was just edited.\nUser: `{after.author}`\nChannel: `{after.channel}`", timestamp=datetime.utcnow())
                embed.add_field(name="Before content:", value=beforec)
                embed.add_field(name="After content:", value=afterc)
                channel = self.bot.get_channel(editedm)
                await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        query = {"_id": member.guild.id}
        member_joined = self.collection.find(query)
        post = {"JoinedServer": 0}
        for result in member_joined:
            joined = result["JoinedServer"]
            if self.collection.find_one({"_id": member.guild.id})["JoinedServer"] == 0:
                return
            else:
            	picture = member.avatar_url_as(format='png')
            	buf_avatar = BytesIO()

            	await picture.save(buf_avatar)
            	buf_avatar.seek(0)

            	font = ImageFont.truetype("fonts/Arial-bold.ttf", 60, encoding="unic")
            	fontsmall = ImageFont.truetype("fonts/Arial-bold.ttf", 45, encoding="unic")

            	check_length = member.name if len(member.name) <= 14 else f'{member.name[0:11]}...'

            	mainimage = Image.open("images/Welcome.png")

            	parser = TwemojiParser(mainimage)
            	await parser.draw_text((275, 230), f"Welcome {check_length}", fill='black', font=font)
            	await parser.draw_text((279, 300), f"We now have {len(member.guild.members)} members!", fill='black', font=fontsmall)
                await parser.close()

            	user_picture = Image.open(buf_avatar)

            	resize = user_picture.resize((200, 200));
            	size_bigger = (resize.size[0] * 3, resize.size[1] * 3)
            	maskimage = Image.new('L', size_bigger, 0)
            	draw = ImageDraw.Draw(maskimage)
            	draw.ellipse((0, 0) + size_bigger, fill=255)
            	maskimage = maskimage.resize(resize.size, Image.ANTIALIAS)
            	resize.putalpha(maskimage)

            	output = ImageOps.fit(resize, maskimage.size, centering=(0.5, 0.5))
            	output.putalpha(maskimage)
            	mainimage.paste(resize, (50, 195), resize)

            	buffer = BytesIO()
            	mainimage.save(buffer, format='PNG')
            	buffer.seek(0)

            	file = discord.File(buffer, "WelcomeImg.png")
            	channel = self.bot.get_channel(joined)
            	await channel.send(file=file)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        query = {"_id": member.guild.id}
        member_joined = self.collection.find(query)
        post = {"LeftServer": 0}
        for result in member_joined:
            joined = result["LeftServer"]
            if self.collection.find_one({"_id": member.guild.id})["LeftServer"] == 0:
                return
            else:
            	picture = member.avatar_url_as(format='png')
            	buf_avatar = BytesIO()

            	await picture.save(buf_avatar)
            	buf_avatar.seek(0)

            	font = ImageFont.truetype("fonts/Arial-bold.ttf", 60, encoding="unic")
            	fontsmall = ImageFont.truetype("fonts/Arial-bold.ttf", 45, encoding="unic")

            	check_length = member.name if len(member.name) <= 14 else f'{member.name[0:11]}...'

            	mainimage = Image.open("images/Welcome.png")

            	parser = TwemojiParser(mainimage)
            	await parser.draw_text((275, 230), f"Goodbye {check_length}", fill='black', font=font)
            	await parser.draw_text((279, 300), f"We loved having you here!", fill='black', font=fontsmall)
                await parser.close()

            	user_picture = Image.open(buf_avatar)

            	resize = user_picture.resize((200, 200));
            	size_bigger = (resize.size[0] * 3, resize.size[1] * 3)
            	maskimage = Image.new('L', size_bigger, 0)
            	draw = ImageDraw.Draw(maskimage)
            	draw.ellipse((0, 0) + size_bigger, fill=255)
            	maskimage = maskimage.resize(resize.size, Image.ANTIALIAS)
            	resize.putalpha(maskimage)

            	output = ImageOps.fit(resize, maskimage.size, centering=(0.5, 0.5))
            	output.putalpha(maskimage)
            	mainimage.paste(resize, (50, 195), resize)

            	buffer = BytesIO()
            	mainimage.save(buffer, format='PNG')
            	buffer.seek(0)

            	file = discord.File(buffer, "Goodbye.png")
            	channel = self.bot.get_channel(joined)
            	await channel.send(file=file)

    async def _create_guild_account(self, guild_id: int) -> None:
        """Create a World guild account."""
        self.collection.insert_one({
            "_id": guild_id,
            "Bans": 0,
            "Kicks": 0,
            "Mutes": 0,
            "Unmute": 0,
            "Slowmode": 0,
            "DeletedMessage": 0,
            "EditedMessage": 0,
            "JoinedServer": 0,
            "LeftServer": 0,
            "Unbanned": 0,
        })

    async def _has_guild_account(self, guild_id: int) -> None:
        """If True, will return guild id. If False, will return nothing."""
        return bool(collection.find_one(
            {"_id": guild_id}
        ))



def setup(bot):
    bot.add_cog(LoggingCog(bot))
