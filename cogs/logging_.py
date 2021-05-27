from os import environ
from PIL import Image, ImageFont
from twemoji_parser import TwemojiParser
from discord import TextChannel
from pymongo import MongoClient
from discord.ext import commands
from discord import Embed, Message
from datetime import datetime
from framework import Guild, Misc

__import__("dotenv").load_dotenv()

class LoggingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.collection = MongoClient(environ["MONGODB_URL"])["Logging"]["Guilds"]

    @commands.group(name="logging")
    async def logging(self, ctx):
        if not ctx.invoked_subcommand:
            return await ctx.send(f"Sorry {ctx.author.mention} please type `w/logging <command>`")

    @logging.command(name="create")
    @commands.has_permissions(administrator=True)
    async def create(self, ctx):
        try:
            Guild._create_guild_account(ctx.guild.id)
            return await ctx.send(embed=Embed(title="Logging", description=f"I have succsesfully setup logging for `{ctx.guild.name}`.", color=self.bot.color))
        except:
            return await ctx.send(embed=Embed(title="Logging", description=f"Sorry {ctx.author.mention} your guild already has a logging system setup!", color=self.bot.color))

    @logging.command(name="shutdown", aliases=["delete"])
    @commands.has_permissions(administrator=True)
    async def shutdown(self, ctx):
        if not self.collection.find_one({'_id': ctx.guild.id}):
            return await ctx.send(embed=Embed(title="Shutdown", description=f"Hey {ctx.author.mention} your guild was not found.\nTry using: `w/logging create`", color=self.bot.color))

        self.collection.remove({"_id": ctx.guild.id})
        await ctx.send(embed=Embed(title="Shutdown", description=f"Hey {ctx.author.mention} i have succsesfully removed your guild's account.", color=self.bot.color))

    @logging.command(name="bans", aliases=["discordbans", "banlog"])
    @commands.has_permissions(administrator=True)
    async def bans(self, ctx, channel: TextChannel):
        result = self.collection.find_one({'_id': ctx.guild.id}) or Guild._create_guild_account(ctx.guild.id)
        if result["Bans"] == channel.id:
            return await ctx.send(embed=Embed(title="Logging", description=f"Sorry {ctx.author.mention} <#{channel.id}> has already been set as your `Ban Log`.", color=self.bot.color))
        self.collection.update_one({"_id": ctx.guild.id}, {"$set": {"Bans": channel.id}})
        return await ctx.send(embed=Embed(title="Logging", description=f"{ctx.author.mention} I have succsesfully updated your `Ban Log` to the channel: <#{channel.id}>", color=self.bot.color))

    @logging.command(name="unban", aliases=["discordunban", "unbanlog", "unbanslog", "unbans"])
    @commands.has_permissions(administrator=True)
    async def unban(self, ctx, channel: TextChannel):
        result = self.collection.find_one({'_id': ctx.guild.id}) or Guild._create_guild_account(ctx.guild.id)
        if result["Unbanned"] == channel.id:
            return await ctx.send(embed=Embed(title="Logging", description=f"Sorry {ctx.author.mention} <#{channel.id}> has already been set as your `Unban Log`.", color=self.bot.color))
        self.collection.update_one({"_id": ctx.guild.id}, {"$set": {"Unbanned": channel.id}})
        await ctx.send(embed=Embed(title="Logging", description=f"{ctx.author.mention} I have succsesfully updated your `Unban Log` to the channel: <#{channel.id}>", color=self.bot.color))

    @logging.command(name="deleted", aliases=["discorddeleted", "delmsg"])
    @commands.has_permissions(administrator=True)
    async def deleted(self, ctx, channel: TextChannel):
        result = self.collection.find_one({'_id': ctx.guild.id}) or Guild._create_guild_account(ctx.guild.id)
        if result["DeletedMessage"] == channel.id:
            return await ctx.send(embed=Embed(title="Logging", description=f"Sorry {ctx.author.mention} <#{channel.id}> has already been set as your `Deleted messages Log`.", color=self.bot.color))
        self.collection.update_one({"_id": ctx.guild.id}, {"$set": {"DeletedMessage": channel.id}})
        return await ctx.send(embed=Embed(title="Logging", description=f"{ctx.author.mention} I have succsesfully updated your `Deleted messages Log` to the channel: <#{channel.id}>", color=self.bot.color))

    @logging.command(name="edited", aliases=["discordedited", "editmsg"])
    @commands.has_permissions(administrator=True)
    async def edited(self, ctx, channel: TextChannel):
        result = self.collection.find_one({'_id': ctx.guild.id}) or Guild._create_guild_account(ctx.guild.id)
        if result["EditedMessage"] == channel.id:
            return await ctx.send(embed=Embed(title="Logging", description=f"Sorry {ctx.author.mention} <#{channel.id}> has already been set as your `Edited messages Log`.", color=self.bot.color))
        self.collection.update_one({"_id": ctx.guild.id}, {"$set": {"EditedMessage": channel.id}})
        await ctx.send(embed=Embed(title="Logging", description=f"{ctx.author.mention} I have succsesfully updated your `Edited messages Log` to the channel: <#{channel.id}>", color=self.bot.color))

    @logging.command(name="welcomes", aliases=["joiner", "joins", "join", "welcomemessages", "welcomemsg", "welcome"])
    @commands.has_permissions(administrator=True)
    async def welcomes(self, ctx, channel: TextChannel):
        result = self.collection.find_one({'_id': ctx.guild.id}) or Guild._create_guild_account(ctx.guild.id)
        if result["JoinedServer"] == channel.id:
            return await ctx.send(embed=Embed(title="Logging", description=f"Sorry {ctx.author.mention} <#{channel.id}> has already been set as your `Welcome messages Log`.", color=self.bot.color))
        self.collection.update_one({"_id": ctx.guild.id}, {"$set": {"JoinedServer": channel.id}})
        await ctx.send(embed=Embed(title="Logging", description=f"{ctx.author.mention} I have succsesfully updated your `Welcome messsages Log` to the channel: <#{channel.id}>", color=self.bot.color))

    @logging.command(name="goodbye", aliases=["memberleave", "bye", "leftserver", "leaving", "goodbyes"])
    @commands.has_permissions(administrator=True)
    async def goodbye(self, ctx, channel: TextChannel):
        result = self.collection.find_one({'_id': ctx.guild.id}) or Guild._create_guild_account(ctx.guild.id)
        if result["LeftServer"] == channel.id:
            return await ctx.send(embed=Embed(title="Logging", description=f"Sorry {ctx.author.mention} <#{channel.id}> has already been set as your `Goodbye messages Log`.", color=self.bot.color))
        self.collection.update_one({"_id": ctx.guild.id}, {"$set": {"LeftServer": channel.id}})
        return await ctx.send(embed=Embed(title="Logging", description=f"{ctx.author.mention} I have succsesfully updated your `Goodbye messsages Log` to the channel: <#{channel.id}>", color=self.bot.color))

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        result = self.collection.find_one({"_id": guild.id})
        if (not result) or (not result["Bans"]):
            return
        ban1 = await guild.fetch_ban(user)
        await self.bot.get_channel(result["Bans"]).send(embed=Embed(title="Ban Log", description=f"A user from this guild has been banned.\nName: `{user.name}`\nID: `{user.id}`\nReason: `{ban1.reason}`", timestamp=datetime.utcnow()))

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        result = self.collection.find_one({"_id": guild.id})
        if (not result) or (not result["Unbanned"]):
            return
        await self.bot.get_channel(result["Unbanned"]).send(embed=Embed(title="Unban Log", description=f"A user from this guild has been unbanned.\nName: `{user.name}`\nID: `{user.id}`", timestamp=datetime.utcnow()))

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        result = self.collection.find_one({"_id": message.guild.id})
        if (not result) or (not result["DeletedMessage"]):
            return
        await self.bot.get_channel(result["DeletedMessage"]).send(embed=Embed(title="Deleted message Log", description=f"A message was just deleted.\nContent: {message.content}\nUser: `{message.author}`\nChannel: `{message.channel}`", timestamp=datetime.utcnow()))

    @commands.Cog.listener()
    async def on_message_edit(self, before: Message, after: Message):
        result = self.collection.find_one({"_id": after.guild.id})
        if (not result) or (not result["EditedMessage"]) or after.attachments or (before.content == after.content):
            return
        await self.bot.get_channel(result["EditedMessage"]).send(embed=Embed(title="Edited message Log", description=f"A message was just edited.\nUser: `{after.author}`\nChannel: `{after.channel}`", timestamp=datetime.utcnow()).add_field(name="Before content:", value=before.content).add_field(name="After content:", value=after.content))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        result = self.collection.find_one({"_id": member.guild.id})
        if (not result) or (not result["JoinedServer"]):
            return

        font = ImageFont.truetype("fonts/Arial-bold.ttf", 60, encoding="unic")
        fontsmall = ImageFont.truetype("fonts/Arial-bold.ttf", 45, encoding="unic")

        check_length = member.name if len(member.name) <= 14 else f'{member.name[:11]}...'

        mainimage = Image.open("images/Welcome.png")

        parser = TwemojiParser(mainimage)
        await parser.draw_text((275, 230), f"Welcome {check_length}", font=font, fill='black')
        await parser.draw_text((279, 300), f"We now have {member.guild.member_count:,} members!", font=fontsmall, fill='black')
        await parser.close()

        CONVERT = await Misc.circle_pfp(member, 200, 200)

        mainimage.paste(CONVERT, (50, 195), CONVERT)
        await self.bot.get_channel(result["JoinedServer"]).send(file=Misc.save_image(mainimage))

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        result = self.collection.find_one({"_id": member.guild.id})
        if (not result) or (not result["LeftServer"]):
            return

        font = ImageFont.truetype("fonts/Arial-bold.ttf", 60, encoding="unic")
        fontsmall = ImageFont.truetype("fonts/Arial-bold.ttf", 45, encoding="unic")

        check_length = member.name if len(member.name) <= 14 else f'{member.name[:11]}...'

        mainimage = Image.open("images/Welcome.png")

        parser = TwemojiParser(mainimage)
        await parser.draw_text((275, 230), f"Goodbye {check_length}", font=font, fill='black')
        await parser.draw_text((279, 300), f"We loved having you here!", font=fontsmall, fill='black')
        await parser.close()

        CONVERT = await Misc.circle_pfp(member, 200, 200)
        mainimage.paste(CONVERT, (50, 195), CONVERT)
        await self.bot.get_channel(result["LeftServer"]).send(file=Misc.save_image(mainimage))

def setup(bot):
    bot.add_cog(LoggingCog(bot))