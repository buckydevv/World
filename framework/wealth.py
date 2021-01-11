from os import environ
from discord.ext import commands
from pymongo import MongoClient
from datetime import datetime
from random import choice
__import__("dotenv").load_dotenv()

class Wealth:
    collection = MongoClient(environ["MONGODB_URL"])["Coins"]["UserCoins"]

    def _create_account(user_id: int) -> None:
        """Create a World account."""
        now = datetime.now()
        _created_at = now.strftime("%m/%d/%Y at %H:%M:%S")
        Wealth.collection.insert_one({
            "_id": user_id,
            "coins": 100,
            "cookie": 0,
            "choc": 0,
            "poop": 0,
            "beans": 0,
            "pizza": 0,
            "waffles": 0,
            "Fish": 0,
            "apple": 0,
            "afk": "No status set, run w/status to set a status",
            "Reputation": 0,
            "LastUsed": "Isnotset",
            "TargetMember": 0,
            "BadgeSlot1": "Doesn't Have Noob",
            "BadgeSlot2": "Doesn't Have Beginner",
            "BadgeSlot3": "Doesn't Have Leader",
            "AccountCreated": _created_at,
            "Premium": "No",
            "Developer": "No",
            "Bank": 0,
            "Wallet": 0,
            "Tickets": 0,
            "TicketReason": "No reason",
            "WorldFriends": 0,
            "IsBlacklisted": "No",
            "CurrentJob": "No job",
            "LastWithdraw": "No date",
            "LastTransfer": "No date",
            "MarriedTo": "Nobody",
            "MarriedDate": "No date",
        })

    def _deposit_coins(user_id: int, coins: int):
        """Deposit coins into the users bank prop"""
        if not Wealth.collection.find_one({"_id": user_id}):
            return
        Wealth.collection.update_one({"_id": user_id}, {"$inc": {
            "Bank": coins,
            "coins": -coins
        }})

    def fishing_ran():
        """Pick a random photo for the `Fishing` command."""
        return choice([
            "https://im-a-dev.xyz/1kKJXQSr.png",
            "https://im-a-dev.xyz/ImWqkaSy.png",
            "https://im-a-dev.xyz/sqPSfhJJ.png",
            "https://im-a-dev.xyz/syTQUdrV.png"
        ])

    def shootout_ran():
        """Pick a random photo for the `Shootout` command."""
        return choice([
            "https://im-a-dev.xyz/QqoZ2M6m.png",
            "https://im-a-dev.xyz/BvdekLII.png",
            "https://im-a-dev.xyz/MfSnYYAa.png"
        ])