from discord.ext import commands
from discord import Embed, Color
from .wealth import Wealth

def require_account():
    async def predicate(ctx):
        if not Wealth.collection.find_one({"_id": ctx.author.id}):
            Wealth._create_account(ctx.author.id)
        return True
    return commands.check(predicate)