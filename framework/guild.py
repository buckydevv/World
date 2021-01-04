from os import environ
from discord.ext import commands
from pymongo import MongoClient

__import__("dotenv").load_dotenv()
class Guild:
    def __init__(self):
        self.color = 0x2F3136
        self.collection = MongoClient(environ["MONGODB_URL"])["Logging"]["Guilds"]

    def _create_guild_account(self, guild_id: int) -> None:
        """Create a World guild account."""
        self.collection.insert_one({
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

    def _has_guild_account(self, guild_id: int) -> None:
        """If True, will return guild id. If False, will return nothing."""
        return bool(self.collection.find_one(
            {"_id": guild_id}
        ))