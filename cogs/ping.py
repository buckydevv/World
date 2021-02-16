from discord import Embed
from time import time
from discord.ext import commands

class PingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Show bots latency.")
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.member)
    async def ping(self, ctx):
        return await ctx.send(title = f'<a:loading:772860569127878676> Pong!', description=f"Latency: `{round(self.bot.latency * 1000)}ms`\nResponse time: `{(time() - ctx.message.created_at.timestamp())*1000:,.0f}ms`", color=self.bot.color))

    @ping.error
    async def ping_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            a = round(error.retry_after)
            await ctx.send(f"Sorry {ctx.author.mention} This command in on cooldown, Try again in {a} seconds.")


def setup(bot):
    bot.add_cog(PingCog(bot))