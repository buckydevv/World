import textwrap
import discord
from time import time
from typing import Optional

from discord import Embed, Member
from discord import __version__ as discord_version
from discord.ext import commands


init_time = time()


class InfoCog(commands.Cog):
    """Contains commands that provide useful information."""

    def __init__(self, bot: commands.Bot) -> None:
        """Sets up the cog."""
        self.bot = bot

    @commands.command(name="userinfo", aliases=("ui", "user"))
    async def userinfo(self, ctx: commands.Context, member: Optional[Member]) -> None:
        """
        Returns information about a member.

        If the `member` parameter is not specified, the info will be from the author.
        """
        user: Member
        if member:
            user = member
        else:
            user = ctx.author
        user_information = Embed(
            title=f"Information about {user} {f'({user.nick})' if user.nick else ''}",
            color=0x2F3136
        )
        user_information.add_field(
            name="General information",
            value=textwrap.dedent(f"""
                Name: `{user.name}`
                ID: `{user.id}`
                Created at: `{user.created_at}`
                Bot: `{user.bot}`
                Status: `{user.status}`
                Activity: `{user.activity}`
            """),
            inline=False
        )
        user_information.add_field(
            name="Server related information",
            value=textwrap.dedent(f"""
                Nick: `{user.nick if user.nick else 'None'}`
                Joined at: `{user.joined_at}`
                Join position: `{sorted(ctx.guild.members, key=lambda m: m.joined_at).index(user) + 1}`
                Booster since: `{user.premium_since}`
                System user: `{user.system}`
            """),
            inline=False
        )
        user_information.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=user_information)

    @userinfo.error
    async def userinfo_error(self, ctx: commands.Context, error: commands.errors.CommandInvokeError) -> None:
        """Handles errors while running the userinfo command."""
        if isinstance(error, commands.errors.BadArgument):
            await ctx.send(f"Sorry {ctx.author.mention} That member doesn't exist.")

    @commands.command(name="serverinfo", aliases=("server",))
    async def serverinfo(self, ctx: commands.Context) -> None:
        """Shows information about the server."""
        server_information = Embed(
            title=f"Information about {ctx.guild.name}",
            color=0x2F3136
        )
        server_information.add_field(name="**Name**", value=f"{ctx.guild}", inline=True)
        server_information.add_field(name="**Owner**", value=f"{ctx.guild.owner}", inline=True)
        server_information.add_field(name="**Region**", value=f"{ctx.guild.region}", inline=True)
        server_information.add_field(name="**Boosts**", value=f"{ctx.guild.premium_subscription_count}", inline=True)
        server_information.add_field(name="**Boost Tier**", value=f"{ctx.guild.premium_tier}", inline=True)
        server_information.add_field(name="**Locale**", value=f"{ctx.guild.preferred_locale}", inline=True)
        server_information.add_field(name="**Members**", value=f"{len(ctx.guild.members)}", inline=True)
        server_information.add_field(name="**Roles**", value=f"{len(ctx.guild.roles)}", inline=True)
        server_information.add_field(name="**Channels**", value=f"{len(ctx.guild.channels)}", inline=True)
        server_information.add_field(name="**Emojis**", value=f"{len(ctx.guild.emojis)}", inline=True)
        server_information.add_field(name="**2FA**", value=f"{ctx.guild.mfa_level}")
        server_information.add_field(name="**Emoji limit**", value=f"{ctx.guild.emoji_limit}", inline=True)
        server_information.add_field(name="**Verify Level**", value=f"{ctx.guild.verification_level}")
        server_information.add_field(name="**File Size limit**", value=f"{ctx.guild.filesize_limit}", inline=True)
        server_information.add_field(name="**Birate Limit**", value=f"{ctx.guild.bitrate_limit}", inline=True)
        server_information.set_thumbnail(url=ctx.guild.icon_url)
        server_information.set_footer(text=f"World ServerInfo | {ctx.guild}'s Info", icon_url=ctx.guild.icon_url)
        await ctx.send(embed=server_information)
    
    @commands.command(aliases=["ri"], help="Role information")
    async def roleinfo(self, ctx, role: discord.Role):
        embed = Embed(
            title="Role Information",
            color=0x2F3136
            ).add_field(
            name=f"{role.name} - Info",
            value=f"{role.mention}\nUsers: `{len(role.members)}`\nColor: `{role.color}`\nMentionable: `{role.mentionable}`\nDisplayed: `{role.hoist}`"
            )
        await ctx.send(embed=embed)

    @roleinfo.error
    async def roleinfo_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/roleinfo <role>`")

    @commands.command(aliases=["ci", "catinfo"], help="Category information")
    async def categoryinfo(self, ctx, *, category: discord.CategoryChannel):
        embed = Embed(
            title="Category Information",
            color=0x2F3136
            ).add_field(
            name=f"{category.name} - Info",
            value=f"Type: `{category.type}`\nText channels: `{len(category.text_channels)}`\nVoice channels: `{len(category.voice_channels)}`\nNsfw: `{category.is_nsfw()}`"
            )
        await ctx.send(embed=embed)

    @categoryinfo.error
    async def categoryinfo_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/categoryinfo <category>`")

    @commands.command(name="AAmount of servers world is in.")
    async def servers(self, ctx: commands.Context) -> None:
        """Returns the number of guilds where World's connected."""
        await ctx.send(embed=Embed(
            description=f"Connected on {len(self.bot.guilds)} servers",
            color=0x2F3136
        ))

    @commands.command(name="botinfo", aliases=("bot", "about"))
    async def botinfo(self, ctx: commands.Context) -> None:
        """Shows info about World."""
        world_information = Embed(
            title="World's info!",
            color=0x2F3136
        )
        world_information.add_field(
            name=":robot: | Stats",
            value=textwrap.dedent(f"""
                Version: discord.py {discord_version}
                Servers: {len(self.bot.guilds)}
                Users: {len(set(self.bot.get_all_members()))}
            """),
            inline=False
        )
        world_information.add_field(
            name=":computer: | Owners and developers",
            value=textwrap.dedent("""
                Owner: `seañ#1718`
                Developers: `Atie#5173` | `fxcilities#4728`
            """),
            inline=False
        )
        await ctx.send(embed=world_information)

    @commands.command(name="vote")
    async def vote(self, ctx: commands.Context) -> None:
        """Sends a link where you can vote for World."""
        vote_embed = Embed(
            title="Vote for World!",
            description="You can vote for World [Here](https://top.gg/bot/700292147311542282/vote)",
            color=0x2F3136
        )
        await ctx.send(embed=vote_embed)

    @commands.command(name="suggest")
    async def suggest(self, ctx: commands.Context, *, suggestion: str) -> None:
        """
        Suggest something for World.

        **WARNING:** Bad usage of this command may lead from a bot ban.
        """
        await ctx.send(
            embed=Embed(
                title="Done!",
                color=0x2F3136
            ).set_footer(
                text=f"I have sent the following to World developers: `{suggestion}`\n\nWARNING: Bad usage of this command may lead to a bot ban."
            )
        )
        suggestion_channel = await self.bot.fetch_channel(763110868791459860)
        suggestion_embed = Embed(
            title=f"Suggestion from {ctx.author}",
            description=suggestion,
            color=0x2F3136
        )
        suggestion_embed.add_field(
            name="Information about the suggester",
            value=textwrap.dedent(f"""
                Name: {ctx.author}
                ID: {ctx.author.id}
            """),
            inline=False
        )
        suggestion_embed.set_thumbnail(url=ctx.author.avatar_url)
        await suggestion_channel.send(embed=suggestion_embed)

    @suggest.error
    async def suggest_error(self, ctx: commands.Context, error: commands.errors.CommandInvokeError) -> None:
        """Handles errors while running suggest command."""
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send(f"Hey {ctx.author.mention} You missed the `suggestion` parameter.")

    @commands.command(name="uptime")
    async def uptime(self, ctx: commands.Context) -> None:
        """Returns the bot's uptime."""
        seconds = time() - init_time
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        uptime_embed = Embed(
            title="Uptime",
            description=f"`{days:.2f} days {hours:.2f} hours {minutes:.2f} minutes {seconds:.2f} seconds`",
            color=0x2F3136
        )
        await ctx.send(embed=uptime_embed)

    # Important: do not add `inv` alias because it's already registered by `inventory` command
    # (cogs/economy.py)
    @commands.command(name="invite")
    async def invite(self, ctx: commands.Context) -> None:
        """Gives a World invite link to the user."""
        embed = Embed(
            title="Invite world",
            description=f"[Invite - Admin perms](https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=8&scope=bot)\n[Invite - No perms](https://discord.com/api/oauth2/authorize?client_id={self.bot.user.id}&permissions=0&scope=bot)\n[Support server](https://discord.gg/AyWjtRncHA)",
            color=0x2F3136
            )
        await ctx.send(embed=embed)


def setup(bot: commands.Bot) -> None:
    """Adds the cog into the bot."""
    bot.add_cog(InfoCog(bot))
