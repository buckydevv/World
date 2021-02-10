from os import environ
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
collection = MongoClient(environ["MONGODB_URL"])["Coins"]["UserCoins"]

class Premium:
    def __init__(self):
        pass

    def has_premium(user: int):
    	"""Check if the given user has World Premium."""
    	result = collection.find_one({"_id": user})
    	return bool(result and result["Premium"] == "Yes")

    def give_premium(user_id: int):
        """Give World Premium to given user."""
        collection.update_one({"_id": user_id}, {"$set": {"Premium": "Yes"}})

    def remove_premium(user_id: int):
        """Remove World Premium from the given user."""
        collection.update_one({"_id": user_id}, {"$set": {"Premium": "No"}})