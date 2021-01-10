from os import environ
from discord.ext import commands
from pymongo import MongoClient
from datetime import datetime
from random import choice
__import__("dotenv").load_dotenv()

class Wealth:
    collection = MongoClient(environ["MONGODB_URL"])["Coins"]["UserCoins"]

    def _has_account(user_id: int) -> None:
        """Returns True if the user_id has an account. Otherwise False."""
        return bool(Wealth.collection.find_one(
            {"_id": user_id}
        ))

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
        result = Wealth.collection.find_one({"_id": user_id})
        if not result:
            return
        Wealth.collection.update_one({"_id": user_id}, {"$inc": {"Bank": coins}})
        Wealth.collection.update_one({"_id": user_id}, {"$inc": {"coins": -coins}})

    def fetch_user(user_id: int, item: str):
        """Fetch a single prop from the given user's id"""
        result = Wealth.collection.find_one({"_id": user_id})
        if not result:
            return
        return result.get(item)

    def mass_fetch(user_id: int):
        """Fetch multiple props from one document."""
        return Wealth.collection.find_one({"_id": user_id})

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

    def extract_props(doc, props):
        """Extract props from the given document."""
        i = 0
        while i < len(props):
            if (thing := doc.get(props[i])):
                yield thing
            i += 1


    def give_coins(user_id: int, amount: int) -> None:
        """Update a users Coins."""
        Wealth.collection.update_one({"_id": user_id}, {"$inc": {"coins": amount}}) # Increment the number to the document.