import discord
import pymongo
import os

from os import environ, listdir

from discord.ext import commands
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

cluster = MongoClient(os.environ["MONGODB_URL"])

db = cluster["Coins"]
collection = db["UserCoins"]

class Premium:
    def __init__(self):
        self.color = 0x2F3136

    def has_premium(user: int):
    	"""Check if the given user has World Premium."""
    	for result in collection.find({"_id": user}):
    		if result["Premium"] == "Yes":
    			return True
    		elif result["Premium"] != "Yes":
    			return False


    def give_premium(user_id: int) -> None:
        """Give World Premium to given user."""
        result = collection.find_one(
            {"_id": user_id}
            )

        collection.update_one({"_id": user_id}, {"$set": {"Premium": "Yes"}})


    def remove_premium(user_id: int) -> None:
        """Remove World Premium from the given user."""
        result = collection.find_one(
            {"_id": user_id}
            )

        collection.update_one({"_id": user_id}, {"$set": {"Premium": "No"}})