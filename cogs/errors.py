from discord.ext import commands
from discord import Embed

class WorldError(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        error = getattr(error, 'original', error)
        if isinstance(error, commands.CommandOnCooldown):
            return await ctx.send(f"Sorry {ctx.author.mention} but `{ctx.command.name}` is on cooldown. Please retry in `{round(error.retry_after):.0f} seconds.`")
            
        if hasattr(ctx.command, 'on_error'):
            return
            
        channel = self.bot.get_channel(824027831407214615)

        if ctx.cog:
            if ctx.cog._get_overridden_method(ctx.cog.cog_command_error) is not None:
                return

        embed = Embed(
            title="New error",
            description=f"Name: {ctx.author}, ID: {ctx.author.id}",
            color=self.bot.color
            ).add_field(
                name="info:",
                value=f"CMD: `{ctx.command.name}`"
            )
        await channel.send(embed=embed)
        await channel.send(f"```\n{ctx.author} - {error}\n```")


        if isinstance(error, commands.CommandNotFound): # We don't want this dumb error lol
            return

        if isinstance(error, commands.BadArgument):
            return await ctx.send(f"Sorry {ctx.author.mention} you used this command the wrong way. Please do `w/help {ctx.command.name}`")
        elif isinstance(error, commands.MissingPermissions):
            return await ctx.send(f"Sorry {ctx.author.mention} but you don't have the permissons to invoke this command.")
        elif isinstance(error, commands.BotMissingPermissions):
            return await ctx.send(f"Sorry {ctx.author.mention}, World is missing the permissons to do this. Please give World the correct permissons")
        elif isinstance(error, commands.ChannelNotFound):
            return await ctx.send(f"Sorry {ctx.author.mention} but that channel was not found! Maybe make it visible for me!")
        elif isinstance(error, commands.MemberNotFound):
            return await ctx.send(f"Sorry {ctx.author.mention} but that Member was not found!")
        elif isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send(f"Sorry {ctx.author.mention} You missed a required argument, Please do `w/help {ctx.command.name}`")

def setup(bot):
    bot.add_cog(WorldError(bot))