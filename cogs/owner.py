import discord
from discord import Embed
from datetime import datetime
from asyncio import sleep as _sleep
from traceback import format_exc
from discord.ext import commands
TOKEN = '||Think Ima Give You My Token!?||'

class OwnerCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    @commands.is_owner()
    async def load(self, ctx, module):
        """Loads a module."""
        try:
            self.bot.load_extension(module)
        except Exception as e:
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.send(embed=Embed(title='load!', description=f"I Have loaded `{module}`", colour=ctx.author.colour))  

    @commands.command(hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, module):
        """Unloads a module."""
        try:
            self.bot.unload_extension(module)
        except Exception as e:
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.send(content=None, embed=Embed(title='Unload!', description=f"I Have Unloaded `{module}`", colour=ctx.author.colour))

    @commands.command(name='reload', hidden=True)
    @commands.is_owner()
    async def _reload(self, ctx, module):
        """Reloads a module."""
        try:
            self.bot.unload_extension(module)
            self.bot.load_extension(module)
        except Exception as e:
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.send(content=None, embed=Embed(title='Reload!', description=f"I Have Reloaded `{module}`", colour=ctx.author.colour))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def update(self, ctx, *, desc):
    	channel = self.bot.get_channel(765632402680447006)
    	msg = await channel.fetch_message(765675535325069323)
    	await msg.edit(embed=Embed(
    		title="Latest update",
    		description=desc,
    		color=0x2F3136,
    		timestamp=datetime.utcnow()
        ))
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
            await ctx.send(embed=Embed(title="Error!", description=f"```{format_exc()}```", color=discord.Color.red()).set_footer(text=f"Invoker: {ctx.author}", icon_url=ctx.author.avatar_url_as(format="png")))
    
    @eval_.error
    async def eval__error(self, ctx, error):
        await ctx.send(embed=Embed(title="Error!", description=f"```{error}```", color=discord.Color.red()).set_footer(text=f"Invoker: {ctx.author}", icon_url=ctx.author.avatar_url_as(format="png")))

    @commands.command()
    @commands.is_owner()
    async def selfpurge(self, ctx, amount: int):
    	def world(m):
    		return self.bot.user.id == m.author.id
    	await ctx.message.channel.purge(limit=amount, check=world, bulk=False)
    	await ctx.send(embed=Embed(title="Purged", description=f"{ctx.author.mention} i have successfully purged `{amount}` of messages in <#{ctx.message.channel.id}>", color=ctx.author.color), delete_after=3)
    	await _sleep(3)
    	await ctx.message.delete()

    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
    	message = await ctx.send(embed=Embed(
    		title="Shutdown World",
    		description="Would you like to shutdown World?",
        ))

    	await message.add_reaction('✅')
    	await message.add_reaction('❎')

    	emoji = ''

    	while True:
    		if emoji=='✅':
    			await message.edit(embed=Embed(
                    title="Shutting Down",
                    description="I Have shut myself down."
                ))
    			await self.bot.close()
    		if emoji=='❎':
    			await message.edit(embed=Embed(
                    title="Shudown Failed",
                    description="You Chose not to shutdown World."
                ))
    			break

    		res = await self.bot.wait_for('reaction_add', check=lambda r, u: u.id == ctx.author.id and r.message.id == message.id, timeout=15)
    		if not res:
    			break
    		if res.id != 700292147311542282:
    			emoji = str(res[0].emoji)
    			await message.remove_reaction(res[0].emoji,res[1])

    	await message.clear_reactions()


def setup(bot):
    bot.add_cog(OwnerCog(bot))
