from os import environ
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
cluster = MongoClient(environ["MONGODB_URL"])

class Devs:
    def __init__(self):
        pass

    async def GetUser(userid: int, options):
    	UserCollection = cluster["Coins"]["UserCoins" if options == "UserCollection" else "UserPointsCollection"]
        return UserCollection.find_one({"_id": userid})

    async def GetGuild(guildid: int):
    	return cluster["Logging"]["Guilds"].find_one({"_id": guildid})

    async def UpdateDocument(_id: int, item: str, updateditem, collection):
    	if collection == "UserCoins":
    		Collection = cluster["Coins"]["UserCoins"]
    	elif collection == "UserPoints":
    		Collection = cluster["Coins"]["Points/others"]
    	elif collection == "Guild":
    		Collection = cluster["Logging"]["Guilds"]
        Collection.update_one({"_id": _id}, {"$set": {item: updateditem}})
        return "Succesfully updated the document"