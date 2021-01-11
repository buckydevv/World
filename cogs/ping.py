import discord
from asyncio import sleep as _sleep
from time import time
from discord.ext import commands

class PingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = 0x2F3136

    @commands.command()
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.member)
    async def ping(self, ctx):
        """Returns the bots Latency/Ping in a embed."""
        testing = discord.Embed(title = 'Testing Latency... <a:loading1:772860591190048768>', color=self.color)
        start = time()
        msg = await ctx.send(embed=testing)
        end = time()
        await _sleep(2)

        finished = discord.Embed(title = f'<a:loading:772860569127878676> Pong!', description=f"Latency: `{round(self.bot.latency * 1000)}ms`\nResponse time: `{(end-start)*1000:,.0f}ms`", color=self.color)
        await msg.edit(embed=finished)

    @ping.error
    async def ping_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            a = round(error.retry_after)
            await ctx.send(f"Sorry {ctx.author.mention} This command in on cooldown, Try again in {a} seconds.")


def setup(bot):
    bot.add_cog(PingCog(bot))
