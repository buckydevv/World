import discord
import pymongo
import datetime
import os

from os import environ, listdir
from discord import Spotify

from discord.ext import commands
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime

load_dotenv()

cluster = MongoClient(os.environ["MONGODB_URL"])

db = cluster["Coins"]
collection = db["UserCoins"]

class Wealth:
    def __init__(self):
        self.color = 0x2F3136

    def _has_account(user_id: int) -> None:
        """Returns True if the user_id has an account. Otherwise False."""
        return bool(collection.find_one(
            {"_id": user_id}
            ))

    def _create_account(user_id: int) -> None:
        """Create a World account."""
        now = datetime.now()
        _created_at = str(now.strftime("%m/%d/%Y at %H:%M:%S"))
        collection.insert_one({
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
        for result in collection.find_one({"_id": user_id}):
            u_bank = result["Bank"]
            u_coins = result["coins"]

            remove_coins = u_coins - coins
            total_coins = u_bank + coins

            collection.update_one({"_id": user_id}, {"$set": {"Bank": total_coins}})
            collection.update_one({"_id": user_id}, {"$set": {"coins": remove_coins}})

    def fetch_user(user_id: int, item: str):
        for result in collection.find({"_id": user_id}):
            fetched = result[item]
            return fetched


    def mass_fetch(user_id: int):
        for result in collection.find({"_id": user_id}):
            return result

    def fishing_ran():
        fishing_idle = "https://im-a-dev.xyz/1kKJXQSr.png"
        caught_fish = "https://im-a-dev.xyz/ImWqkaSy.png"
        caught_cookies = "https://im-a-dev.xyz/sqPSfhJJ.png"
        caught_coins = "https://im-a-dev.xyz/syTQUdrV.png"

        randomize = [fishing_idle, caught_fish, caught_cookies, caught_coins]
        random_choice = random.choice(randomize)

        return random_choice

    def shootout_ran():
        shooter_world = "https://im-a-dev.xyz/QqoZ2M6m.png"
        normal_world = "https://im-a-dev.xyz/BvdekLII.png"
        nothing_world = "https://im-a-dev.xyz/MfSnYYAa.png"

        all_worlds = [shooter_world, normal_world, nothing_world]

        random_choice = random.choice(all_worlds)

        return random_choice

    def extract_props(doc, props):
        i = 0
        while i < len(props):
            if (thing := doc.get(props[i])):
                yield thing
            i += 1