import discord
import inspect
import traceback
import datetime
import asyncio
from discord.ext import commands
TOKEN = '||Think Ima Give You My Token!?||'


class OwnerCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True, help="Load a python file.")
    @commands.is_owner()
    async def load(self, ctx, module):
        """Loads a module."""
        try:
            self.bot.load_extension(module)
        except Exception as e:
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            embed = discord.Embed(title='load!', description=f"I Have loaded `{module}`", colour=ctx.author.colour)
            await ctx.send(content=None, embed=embed)  

    @commands.command(hidden=True, help="Unload a python file.")
    @commands.is_owner()
    async def unload(self, ctx, module):
        """Unloads a module."""
        try:
            self.bot.unload_extension(module)
        except Exception as e:
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            embed = discord.Embed(title='Unload!', description=f"I Have Unloaded `{module}`", colour=ctx.author.colour)
            await ctx.send(content=None, embed=embed)

    @commands.command(name='reload', hidden=True, help="Reload python file.")
    @commands.is_owner()
    async def _reload(self, ctx, module):
        """Reloads a module."""
        try:
            self.bot.unload_extension(module)
            self.bot.load_extension(module)
        except Exception as e:
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            embed = discord.Embed(title='Reload!', description=f"I Have Reloaded `{module}`", colour=ctx.author.colour)
            await ctx.send(content=None, embed=embed)

    @commands.command(hidden=True, help="Set patches")
    @commands.is_owner()
    async def update(self, ctx, *, desc):
    	channel = self.bot.get_channel(765632402680447006)
    	msg = await channel.fetch_message(765675535325069323)
    	embed = discord.Embed(
    		title="Latest update",
    		description=desc,
    		color=0x2F3136,
    		timestamp=datetime.datetime.utcnow()
    		)
    	await msg.edit(embed=embed)
    	await ctx.send(f"Hey {ctx.author.mention} i have updated the message in <#765632402680447006>")

    @commands.command(name="eval")
    @commands.is_owner()
    async def eval_(self, ctx: commands.Context, *, code: str):
        import traceback
        code = code.strip("`")
        if code.startswith(("py\n", "python\n")):
            code = "\n".join(code.split("\n")[1:])

        try:
            exec(
                "async def __function():\n"
                + "".join(f"\n    {line}" for line in code.split("\n")),
                locals()
            )

            await locals()["__function"]()
        except Exception:
            res = discord.Embed(title="Error!", description=f"```{traceback.format_exc()}```", color=discord.Color.red())
            res.set_footer(text=f"Invoker: {ctx.author}", icon_url=ctx.author.avatar_url_as(format="png"))
            await ctx.send(embed=res)
    @eval_.error
    async def eval__error(self, ctx, error):
        embed = discord.Embed(title="Error!", description=f"```{error}```", color=discord.Color.red())
        embed.set_footer(text=f"Invoker: {ctx.author}", icon_url=ctx.author.avatar_url_as(format="png"))
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def selfpurge(self, ctx, amount: int):
    	def world(m):
    		return m.author == self.bot.user
    	await ctx.message.channel.purge(limit=amount, check=world)
    	embed = discord.Embed(title="Purged", description=f"{ctx.author.mention} i have successfully purged `{amount}` of messages in <#{ctx.message.channel.id}>", color=ctx.author.color)
    	yes = await ctx.send(embed=embed)
    	await asyncio.sleep(3)
    	await yes.delete()
    	await ctx.message.delete()



def setup(bot):
    bot.add_cog(OwnerCog(bot))
