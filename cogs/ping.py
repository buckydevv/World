import discord
from discord.ext import commands
import asyncio


class PingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Show bots latency.")
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.member)
    async def ping(self, ctx):
        ping3 = discord.Embed(title = 'Testing Latency... <a:load:724296877356482640>', color =0x13d1f2)
        ping2 = discord.Embed(title = 'Connection Recived <a:load:724296877356482640>', color =0xe30ec3)
        ppo = discord.Embed(title = f'<a:green:724295655954317404> Pong! {round(self.bot.latency * 1000)}ms', color = 0xf05f0c)

        pinging = await ctx.send(embed = ping3)
        await asyncio.sleep(2)
        await pinging.edit(embed = ping2)
        await asyncio.sleep(2)
        await pinging.edit(embed = ppo)

    @ping.error
    async def ping_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            a = error.retry_after
            a = round(a)
            await ctx.send(f"Sorry {ctx.author.mention} This command in on cooldown, Try again in {a} seconds.")


def setup(bot):
    bot.add_cog(PingCog(bot))
