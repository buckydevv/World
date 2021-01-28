from os import environ
from discord.ext import commands
from pymongo import MongoClient

__import__("dotenv").load_dotenv()
class Guild:
    collection = MongoClient(environ["MONGODB_URL"])["Logging"]["Guilds"]

    def _create_guild_account(guild_id: int):
        """Create a World guild account."""
        collection.insert_one({
            "_id": guild_id,
            "Bans": 0,
            "Kicks": 0,
            "Mutes": 0,
            "Unmute": 0,
            "Slowmode": 0,
            "DeletedMessage": 0,
            "EditedMessage": 0,
            "JoinedServer": 0,
            "LeftServer": 0,
            "Unbanned": 0,
        })