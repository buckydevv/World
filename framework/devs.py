import discord
import pymongo
import datetime
import os

from os import environ, listdir
from discord import Spotify

from discord.ext import commands
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

cluster = MongoClient(os.environ["MONGODB_URL"])

class Devs:
    def __init__(self):
        self.color = 0x2F3136

    async def GetUser(userid: int, options):
    	if options == "UserCollection":
    		UserCollection = cluster["Coins"]["UserCoins"]
    		for result in UserCollection.find({"_id": userid}):
    			return result
    	elif options == "UserPointsCollection":
    		UserPointsCollection = cluster["Coins"]["Points/others"]
    		for result in UserPointsCollection.find({"_id": userid}):
    			return result

    async def GetGuild(guildid: int):
    	GuildCollection = cluster["Logging"]["Guilds"]
    	for result in GuildCollection.find({"_id": guildid}):
    		return result

    async def UpdateDocument(_id: int, item: str, updateditem, collection):
    	if collection == "UserCoins":
    		UserCollection = cluster["Coins"]["UserCoins"]
    		UserCollection.update_one({"_id": _id}, {"$set": {item: updateditem}})
    		return "Succesfully updated the document"
    	elif collection == "UserPoints":
    		UserPointsCollection = cluster["Coins"]["Points/others"]
    		UserPointsCollection.update_one({"_id": _id}, {"$set": {item: updateditem}})
    		return "Succesfully updated the document"
    	elif collection == "Guild":
    		GuildCollection = cluster["Logging"]["Guilds"]
    		GuildCollection.update_one({"_id": _id}, {"$set": {item: updateditem}})
    		return "Succesfully updated the document"