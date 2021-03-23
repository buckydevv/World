from os import environ
from pymongo import MongoClient
collection = MongoClient(environ["MONGODB_URL"])["Logging"]["Guilds"]

__import__("dotenv").load_dotenv()

class Guild:
    def _create_guild_account(guild_id: int):
        """Create a World guild account."""
        obj = {
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
        }
        
        collection.insert_one(obj)
        return obj