import psutil
from asyncio import sleep as _sleep
from json import dumps, loads, load
from typing import Optional
from time import time
from framework import Paginator
from textwrap import dedent
from discord import Embed, Member, Role, CategoryChannel, __version__
from discord.ext import commands
from aiohttp import ClientSession

class InfoCog(commands.Cog):
    """Contains commands that provide useful information."""

    def __init__(self, bot: commands.Bot) -> None:
        """Sets up the cog."""
        self.bot = bot
        self.init_time = time()
        self.session = ClientSession()
        self.color = 0x2F3136

    @commands.command(name="userinfo", aliases=("ui", "user"))
    async def userinfo(self, ctx: commands.Context, member: Optional[Member]) -> None:
        """
        Returns information about a member.
        If the `member` parameter is not specified, the info will be from the author.
        """
        user = member or ctx.author
        await ctx.send(embed=Embed(
            title=f"Information about {user} {f'({user.nick})' if user.nick else ''}",
            color=self.color
        ).add_field(
            name="General information",
            value=dedent(f"""
                Name: `{user.name}`
                ID: `{user.id}`
                Created at: `{user.created_at.strftime('%m/%d/%Y')}`
                Bot: `{user.bot}`
                Status: `{user.status}`
                Activity: `{user.activity}`
            """),
            inline=False
        ).add_field(
            name="Server related information",
            value=dedent(f"""
                Nick: `{user.nick if user.nick else 'None'}`
                Joined at: `{user.joined_at.strftime('%m/%d/%Y')}`
                Join position: `{sorted(ctx.guild.members, key=lambda m: m.joined_at).index(user) + 1}`
                Booster since: `{user.premium_since}`
                System user: `{user.system}`
            """),
            inline=False
        ).set_thumbnail(url=user.avatar_url))

    @userinfo.error
    async def userinfo_error(self, ctx: commands.Context, error: commands.errors.CommandInvokeError) -> None:
        """Handles errors while running the userinfo command."""
        if isinstance(error, commands.errors.BadArgument):
            await ctx.send(f"Sorry {ctx.author.mention} That member doesn't exist.")

    @commands.command(name="serverinfo", aliases=("server", "guild"))
    async def serverinfo(self, ctx: commands.Context) -> None:
        """Shows information about the server."""
        await ctx.send(embed=Embed(
            title=f"Information about {ctx.guild.name}",
            color=self.color
        ).add_field(name="**Name**", value=ctx.guild.name
        ).add_field(name="**Owner**", value=f"{ctx.guild.owner}"
        ).add_field(name="**Region**", value=f"{ctx.guild.region}"
        ).add_field(name="**Boosts**", value=f"{ctx.guild.premium_subscription_count}"
        ).add_field(name="**Boost Tier**", value=f"{ctx.guild.premium_tier}"
        ).add_field(name="**Locale**", value=f"{ctx.guild.preferred_locale}"
        ).add_field(name="**Members**", value=f"{len(ctx.guild.members)}"
        ).add_field(name="**Roles**", value=f"{len(ctx.guild.roles)}"
        ).add_field(name="**Channels**", value=f"{len(ctx.guild.channels)}"
        ).add_field(name="**Emojis**", value=f"{len(ctx.guild.emojis)}"
        ).add_field(name="**2FA**", value=f"{ctx.guild.mfa_level}"
        ).add_field(name="**Emoji limit**", value=f"{ctx.guild.emoji_limit}"
        ).add_field(name="**Verify Level**", value=f"{ctx.guild.verification_level}"
        ).add_field(name="**File Size limit**", value=f"{ctx.guild.filesize_limit}"
        ).add_field(name="**Birate Limit**", value=f"{ctx.guild.bitrate_limit}"
        ).set_thumbnail(url=ctx.guild.icon_url))
    
    @commands.command(aliases=["ri"])
    async def roleinfo(self, ctx, role: Role):
        await ctx.send(embed=Embed(
            title="Role Information",
            color=self.color
            ).add_field(
            name=f"{role.name} - Info",
            value=f"{role.mention}\nUsers: `{len(role.members)}`\nColor: `{role.color}`\nMentionable: `{role.mentionable}`\nDisplayed: `{role.hoist}`"
        ))

    @roleinfo.error
    async def roleinfo_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/roleinfo <role>`")

    @commands.command(aliases=["ci", "catinfo"])
    async def categoryinfo(self, ctx, *, category: CategoryChannel):
        await ctx.send(embed=Embed(
            title="Category Information",
            color=self.color
            ).add_field(
            name=f"{category.name} - Info",
            value=f"Type: `{category.type}`\nText channels: `{len(category.text_channels)}`\nVoice channels: `{len(category.voice_channels)}`\nNsfw: `{category.is_nsfw()}`"
        ))

    @categoryinfo.error
    async def categoryinfo_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/categoryinfo <category>`")

    @commands.command(name="botinfo", aliases=("bot", "about"))
    async def botinfo(self, ctx: commands.Context) -> None:
        """Shows info about World."""
        req = await self.session.get("https://api.statcord.com/v3/700292147311542282")
        if req.status != 200:
            return await ctx.send(f"Sorry {ctx.author.mention} a error has occured and will be fixed soon!")
        r = await req.json()
        p = dumps(r)
        y = loads(p)
        with open('prefixes.json', 'r') as f: # wow nice
            prefixes = load(f)
        guild_prefix = "w/, world" if (str(ctx.guild.id) in prefixes) else prefixes[str(ctx.guild.id)]
        start = time()
        message = await ctx.send(embed=Embed(title="Bot information", description="Loading... <a:loading1:772860591190048768>", color=self.color))
        end = time()
        await _sleep(1)
        await message.edit(embed=Embed(
            title="World's info!",
            color=self.color,
            description=dedent(f"""
                > <:Worldhappy:768145777985454131> Bot Information
                Version: `discord.py {__version__}`
                CPU Load: `{psutil.cpu_percent()}%`
                Cores: `{psutil.cpu_count()}`
                Memory: `{psutil.virtual_memory().percent}%`
                Servers: `{len(self.bot.guilds)}`
                Users: `{len(set(self.bot.get_all_members()))}`
                > <:Worldsmile:768145778493227058> Guild info
                Prefix: `{guild_prefix}`
                Latency: `{round(self.bot.latency * 1000)}ms`
                Response Time: `{(end-start)*1000:,.0f}ms`
                > <:Worldsipjuice:768201555811631134> Command info
                Total commands: `{len(self.bot.commands)}`
                Commands used today: `{y['data'][0]['commands']}`
                Popular commands: `w/{y['data'][0]['popular'][0]['name']}`, `w/{y['data'][0]['popular'][1]['name']}`, `w/{y['data'][0]['popular'][2]['name']}`,\n`w/{y['data'][0]['popular'][3]['name']}`, `w/{y['data'][0]['popular'][4]['name']}`
            """)
        ))

    @commands.command(name="vote")
    async def vote(self, ctx: commands.Context) -> None:
        """Sends a link where you can vote for World."""
        await ctx.send(embed=Embed(
            title="Vote for World!",
            description="You can vote for World [Here](https://top.gg/bot/700292147311542282/vote)",
            color=self.color
        ))

    @commands.command(name="suggest")
    async def suggest(self, ctx: commands.Context, *, suggestion: str) -> None:
        """
        Suggest something for World.
        **WARNING:** Bad usage of this command may lead from a bot ban.
        """
        await ctx.send(
            embed=Embed(
                title="Done!",
                description=f"I have sent the following to World developers: `{suggestion}`",
                color=self.color
            ).set_footer(
                text=f"WARNING: Bad usage of this command may lead to a bot ban."
            )
        )
        suggestion_channel = await self.bot.fetch_channel(763110868791459860)
        suggestion_embed.set_thumbnail(url=ctx.author.avatar_url)
        await suggestion_channel.send(embed=Embed(
            title=f"Suggestion from {ctx.author}",
            description=suggestion,
            color=self.color
        ).add_field(name="Information about the suggester",
            value=dedent(f"""
                Name: {ctx.author}
                ID: {ctx.author.id}
            """),
            inline=False
        ))

    @suggest.error
    async def suggest_error(self, ctx: commands.Context, error: commands.errors.CommandInvokeError) -> None:
        """Handles errors while running suggest command."""
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send(f"Hey {ctx.author.mention} You missed the `suggestion` parameter.")

    @commands.command(name="uptime")
    async def uptime(self, ctx: commands.Context) -> None:
        """Returns the bot's uptime."""
        seconds = time() - self.init_time
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        await ctx.send(embed=Embed(
            title="Uptime",
            description=f"`{days:.2f} days {hours:.2f} hours {minutes:.2f} minutes {seconds:.2f} seconds`",
            color=self.color
        ))

    @commands.command(name="invite")
    async def invite(self, ctx: commands.Context) -> None:
        """Gives a World invite link to the user."""
        await ctx.send(embed=Embed(
            title="Invite world",
            description=f"[Invite - Admin perms](https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=8&scope=bot)\n[Invite - No perms](https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=0&scope=bot)\n[Support server](https://discord.gg/AyWjtRncHA)",
            color=self.color
        ))

    @commands.command(help="How to get World emotes!", aliases=["worldemotes", "worldemote", "emojis", "emoji"])
    async def emotes(self, ctx, allemote: Optional[str]) -> None:
        allemotes = ("--all", "all", "allemotes")
        if not allemote:
            return await ctx.send(embed=Embed(
                title="World emotes",
                description="`Support server:` [<:Worldhappy:768145777985454131> Join](https://discord.gg/gQSHvKCV)\n`World Emotes1:` [<:Worldhappy:768145777985454131> Join](https://discord.gg/TEfM7hEBpz)",
                color=self.color
            ).set_footer(text="To see all emotes run `w/emotes --all`"))

        if allemote in allemotes:
            server1 = self.bot.get_guild(738392767637487713)
            world1 = [f"`{emoji.name}` - {emoji}" for emoji in server1.emojis]
            server2 = self.bot.get_guild(774294150748831814)
            world2 = [f"`{emoji.name}` - {emoji}" for emoji in server2.emojis]

            paginator = Paginator(ctx, [
                Embed(title="`Page 1` - World Emotes", description = "\n".join(world1[:18]), color=self.color),
                Embed(title="`Page 2` - World Emotes", description="\n".join(world1[19:34]), color=self.color),
                Embed(title="`Page 3` - World Emotes", description="\n".join(world1[35:51]), color=self.color),
                Embed(title="`Page 4` - World Emotes", description="\n".join(world2[:25]), color=self.color),
            ])
            return await paginator.execute()
        
def setup(bot: commands.Bot) -> None:
    """Adds the cog into the bot."""
    bot.add_cog(InfoCog(bot))
