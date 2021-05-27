from discord.ext import commands
from statcord import Client
from os import environ
__import__("dotenv").load_dotenv()

class StatcordPost(commands.Cog):
    def __init__(self, bot):
        self.api = Client(bot, environ["STATCORD_SECRET"])
        self.api.start_loop()

    @commands.Cog.listener()
    async def on_command(self,ctx):
        self.api.command_run(ctx)

def setup(bot):
    bot.add_cog(StatcordPost(bot))