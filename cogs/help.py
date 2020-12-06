import discord
import typing
import textwrap
from typing import Optional
from discord.ext.commands import Cog
from discord import Embed
from discord.ext.commands import command
from discord.utils import get
from discord.ext import commands

world_pfp = ("https://im-a-dev.xyz/EL35H6QC.png")


def syntax(command):
  cmd_and_aliases = " | ".join([str(command), *command.aliases])
  params = []

  for key, value in command.params.items():
    if key not in ("self", "ctx"):
      params.append(f"[{key}]" if "NoneType" in str(value) else f"<{key}>")

  params = " ".join(params)

  return f"**Usage:** `w/{cmd_and_aliases} {params}`"


class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = 0x2F3136

    async def cmd_help(self, ctx, command):
      embed = Embed(title=f"{command} - Help",
            description=syntax(command),
            color=self.color)
      embed.add_field(name="Command info", value=command.help)
      await ctx.send(embed=embed)


    @command(name="help", help="Shows this message.")
    async def show_help(self, ctx, cmd: Optional[str]):
      """Shows this message."""
      if cmd is None:
        embed = discord.Embed(color=self.color)
        embed.set_author(name='World - Help', icon_url=world_pfp)
        embed.add_field(name="Shows multiple categories.", value="w/categories", inline=True)
        embed.add_field(name="Invite", value="[Invite World](https://discord.com/oauth2/authorize?client_id=700292147311542282&permissions=8&scope=bot)", inline=True)
        embed.add_field(name="Vote", value="[Vote For World](https://top.gg/bot/700292147311542282/vote)", inline=True)
        embed.set_image(url="https://im-a-dev.xyz/Yr0rRrcP.png")
        embed.set_footer(text="Use \"w/help <command>\" For more info")
        await ctx.send(embed=embed)

      else:
        if (command := get(self.bot.commands, name=cmd)):
          await self.cmd_help(ctx, command)

        else:
          await ctx.send(f"Sorry {ctx.author.mention} thats not a valid command.")


    @commands.command(help="Shows categories")
    async def categories(self, ctx):
      em = discord.Embed(color=self.color)
      em.add_field(name="‎‎World", value=f"New\n`w/new`\nFun\n`w/fun`\nOther\n`w/other`")
      em.add_field(name=f"Categories", value=f"Logging\n`w/logs`\nEconomy\n`w/economy`\nModeration\n`w/mod`")
      await ctx.send(embed=em)


    @commands.command(help="Shows other category.")
    async def other(self, ctx):
      em = discord.Embed(
        title="Other commands", 
        color=self.color,
        ).add_field(
        name="<:shufflelogo:765652804387471430> | Random Commands",
        value="`w/urban` | `w/advice` | `w/userinfo` | `w/serverinfo` | `w/roleinfo` | `w/categoryinfo` | `w/activity` | `w/snipe` | `w/editsnipe`",
        inline=False
        ).add_field(
        name="<:Worldhappy:768145777985454131> | World commands",
        value="`w/botinfo` | `w/invite` | `w/vote` | `w/uptime` | `w/emotes`",
        inline=False
        )
      await ctx.send(embed=em)



    @commands.command(help="Shows moderation category.")
    async def mod(self, ctx):
      em = discord.Embed(
        title="Moderation commands", 
        color=self.color,
        ).add_field(
        name="<:memberlogo:765649915031846912> | Member Commands",
        value="`w/ban` | `w/kick` | `w/unban` | `w/mute` | `w/unmute`"
        ).add_field(
        name="<:channellogo:765650652797468682> | Channel Commands",
        value="`w/slowmode` | `w/lock` | `w/unlock` | `w/nuke` | `w/purge`",
        inline=False
        )
      await ctx.send(embed=em)
      
    @commands.command(help="Shows logging category.")
    async def logs(self, ctx):
      em = discord.Embed(
        title="Logging commands", 
        color=self.color,
        ).add_field(
        name="<:discordlogo:765648661039677481> | Guild Commands",
        value="`w/logging create` | `w/logging shutdown`",
        inline=False
        ).add_field(
        name=":question: | Logging options",
        value="`w/logging bans` | `w/logging unban` | `w/logging welcomes` | `w/logging goodbye` | `w/logging edited` | `w/logging deleted`",
        inline=False
        )
      await ctx.send(embed=em)


    @commands.command(hlep="Shows Fun category.")
    async def fun(self, ctx):
      embed = discord.Embed(
        title="Fun commands", 
        color=self.color,
        ).add_field(
        name="<:Worldcool:768201555492864030> | Normal fun",
        value="`w/gay` | `w/askali` | `w/pp` | `w/8ball` | `w/f` | `w/joke` | `w/emojify` | `w/akinator` | `w/kill` | `w/fast`"
        ).add_field(
        name=":frame_photo: | Image fun",
        value="`w/fakequote` | `w/tweet` | `w/topgg` | `w/tweet` | `w/blur` | `w/avatar` | `w/qr` | `w/flip` | `w/wide`",
        inline=False
        )
      await ctx.send(embed=embed)


    @commands.command(help="Shows economy category.")
    async def economy(self, ctx):
      em = discord.Embed(
        title="Economy commands", 
        color=self.color,
        ).add_field(
        name="<:account:765642079920980009> | Account Commands",
        value="`w/create` | `w/delete` | `w/balance` | `w/inventory` | `w/transfer` | `w/profile` | \n`w/mybadges` | `w/mystatus` `w/repcount`"
        ).add_field(
        name=":shopping_bags: | Market Commands",
        value="`w/shop` | `w/buy` | `w/sell` | `w/beg` | `w/badgeshop` | `w/buybadge` | `w/deposit` | `w/withdraw`",
        inline=False
        ).add_field(
        name=":thumbsup: | Fun commands",
        value="`w/daily` | `w/weekly` | `w/gamble` | `w/rep` | `w/repinfo` | `w/marry` | `w/divorce` | `w/rob` | `w/shootout` | `w/fish`",
        inline=False
        )
      await ctx.send(embed=em)
   

    @commands.command(help="Shows new commands.")
    async def new(self, ctx):
      em = discord.Embed(
        title="New commands!", 
        color=self.color,
        description="`w/emotes` | `w/rob` | `w/fish` | `w/shootout` | `w/duck` | `w/flip` | `w/blur`\n\nTo see patches Join the support server! `w/invite`"
        )
      await ctx.send(embed=em)


def setup(bot):
    bot.add_cog(HelpCog(bot))
