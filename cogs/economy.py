import os
import random
import textwrap
from dataclasses import dataclass
from datetime import datetime
from os import environ
from typing import Literal, Union

import aiohttp

from discord import Embed, Member
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType

from dotenv import load_dotenv

import motor.motor_asyncio


@dataclass
class User:
    """Represents a World Economy user."""

    _id: int
    coins: int
    cookie: int
    choc: int
    poop: int
    apple: int
    afk: str


class Item(type):
    """Base class for a World item."""


class Cookie(metaclass=Item):
    """Represents a World cookie."""

    name = "cookie"
    price = 1


class Choc(metaclass=Item):
    """Represents a World chocolatebar."""

    name = "choc"
    price = 4


class Poop(metaclass=Item):
    """Represents a World poop."""

    name = "poop"
    price = 6


class Apple(metaclass=Item):
    """Represents a World item."""

    name = "apple"
    price = 10


class ItemConverter(commands.Converter):
    """Converts a string into a World item."""

    async def convert(self, ctx: commands.Context, argument: str) -> Item:
        """Converts a string into a World item."""
        if argument.lower() in ("cookie", "cookies"):
            return Cookie
        elif argument.lower() in ("chocbar", "choc", "chocbars", "chocs"):
            return Choc
        elif argument.lower() in ("poop", "poops"):
            return Poop
        elif argument.lower() in ("apple", "apples"):
            return Apple
        else:
            raise commands.errors.BadArgument("Invalid item provided.")


class UnsignedIntegerConverter(commands.Converter):
    """Converts a string into an unsigned integer."""

    async def convert(self, ctx: commands.Context, argument: str) -> int:
        """Converts a string into an unsigned integer."""
        try:
            if (number := int(argument)) <= 0:
                raise commands.errors.BadArgument("No signed integers or 0!")
        except ValueError:
            raise commands.errors.BadArgument("This is not a number.")

        return number


class EconomyError(Exception):
    """Base exception for economy-related (the cog) errors."""


class NotEnoughCoins(EconomyError):
    """Exception raised when the user doesn't have enough coins."""


class NotEnoughItems(EconomyError):
    """Exception raised when the user doesn't have enough items to perform the operation."""


class UserNotFound(EconomyError):
    """Exception raised when the user is not found."""


class EconomyCog(commands.Cog):
    """Cog for World's economy system."""

    def __init__(self) -> None:
        """Sets up the cog."""
        self._connect_to_database()

    @commands.command(name="shop", aliases=("items",))
    async def shop(self, ctx: commands.Context) -> None:
        """Returns all items you can buy or sell."""
        shop_embed = Embed(
            title="Shop",
            description=textwrap.dedent("""
                - Cookies
                `1 coin per cookie.`
                - Chocbars
                `4 coins per choc.`
                - Poops
                `6 coins per poop.`
                - Apples
                `10 coins per apple.`
            """),
            color=0x2F3136
        )
        await ctx.send(embed=shop_embed)

    @commands.command(name="inventory", aliases=("inv",))
    async def inventory(self, ctx: commands.Context) -> None:
        """Returns the current items from the user inventory."""
        if not (await self._has_account(ctx.author.id)):
            await self._create_account(ctx.author.id)

        author = await self._get_user(ctx.author.id)
        inventory_embed = Embed(
            title=f"{ctx.author}'s inventory",
            color=0x2F3136
        )
        inventory_embed.add_field(
            name="Coins",
            value=f":moneybag: {author.coins:.2f}"
        )
        inventory_embed.add_field(
            name="Apples",
            value=f":apple: {author.apple}"
        )
        inventory_embed.add_field(
            name="Cookies",
            value=f":cookie: {author.cookie}"
        )
        inventory_embed.add_field(
            name="Chocolate bars",
            value=f":chocolate_bar: {author.choc}"
        )
        inventory_embed.add_field(
            name="Poops",
            value=f":poop: {author.poop}"
        )
        inventory_embed.add_field(
            name="Status",
            value=author.afk
        )
        inventory_embed.set_thumbnail(url=ctx.author.avatar_url)
        await ctx.send(embed=inventory_embed)

    @commands.command(name="profile", aliases=("account",))
    async def profile(self, ctx: commands.Context, user: Member=None) -> None:
        """Returns the profile of the users items, status and coins."""
        user = user or ctx.author
        if not (await self._has_account(user.id)):
            await self._create_account(user.id)

        stat = await self._get_user(user.id)
        status_embed = Embed(
        	title=f"{user}'s Profile",
        	color=0x2F3136
        	).add_field(
        	name="<:memberlogo:765649915031846912> | Account",
        	value=f"Account Type: `World Account`\nCoins: `{stat.coins:.2f}`\nStatus: `{stat.afk}`"
        	).set_thumbnail(
        	url=user.avatar_url
        	)
        await ctx.send(embed=status_embed)

    @profile.error
    async def profile_error(self, ctx: commands.Context, error: commands.errors.CommandInvokeError) -> None:
        """Handles errors when showing users profile something."""
        error = getattr(error, "original", error)
        if isinstance(error, NotEnoughCoins):
            await ctx.send(error)
        elif isinstance(error, commands.errors.BadArgument):
            await ctx.send(error)
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please mention a valid user.")

    @commands.command(name="balance", aliases=("bal",))
    async def balance(self, ctx: commands.Context) -> None:
        """Returns the current balance of the user."""
        if not (await self._has_account(ctx.author.id)):
            await self._create_account(ctx.author.id)

        author = await self._get_user(ctx.author.id)
        bal_embed = Embed(
            title=f"{ctx.author}'s balance",
            color=0x2F3136,
            description=f"`{author.coins:.2f}` Coins"
        )
        await ctx.send(embed=bal_embed)

    @commands.command(name="buy")
    async def buy(self, ctx: commands.Context, item: ItemConverter, amount: UnsignedIntegerConverter) -> None:
        """
        Buys items.

        Run `w/shop` for a list of items.
        """
        if not (await self._has_account(ctx.author.id)):
            await self._create_account(ctx.author.id)

        user = await self._get_user(ctx.author.id)
        await self._buy(item, amount, user)
        buy_embed = Embed(
            title="You successfully bought",
            color=0x2F3136,
            description=f"{ctx.author.mention} bought `{amount} {item.name}{'s' if amount > 1 else ''}`\n\nTo see your inventory run the command `w/inventory`"
        )
        await ctx.send(embed=buy_embed)

    @buy.error
    async def buy_error(self, ctx: commands.Context, error: commands.errors.CommandInvokeError) -> None:
        """Handles errors when buying something."""
        error = getattr(error, "original", error)
        if isinstance(error, NotEnoughCoins):
            await ctx.send(error)
        elif isinstance(error, commands.errors.BadArgument):
            await ctx.send(error)
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} You missed the `item` or `amount` arguments.")

    @commands.command(name="sell")
    @commands.cooldown(1, 60, BucketType.member)
    async def sell(self, ctx: commands.Context, item: ItemConverter, amount: UnsignedIntegerConverter) -> None:
        """
        Sells items.

        Run `w/shop` for a list of items.
        """
        if not (await self._has_account(ctx.author.id)):
            await self._create_account(ctx.author.id)

        user = await self._get_user(ctx.author.id)
        coins_earned = await self._sell(item, amount, user)
        if not coins_earned:
            robbed_embed = Embed(title="Sorry", color=0x2F3136, description=f"Sorry {ctx.author.mention} your items couldn't be sold because you got robbed. Good luck the next time!")
            await ctx.send(embed=robbed_embed)
        else:
            sold_embed = Embed(title="Congrats!", color=0x2F3136, description=f"Hey {ctx.author.mention} You sold your items successfully! You earned **{coins_earned}** coins.")
            await ctx.send(embed=sold_embed)

    @sell.error
    async def sell_error(self, ctx: commands.Context, error: commands.errors.CommandInvokeError) -> None:
        """Handles errors when buying something."""
        error = getattr(error, "original", error)
        if isinstance(error, NotEnoughItems):
            await ctx.send(error)
        elif isinstance(error, commands.errors.BadArgument):
            await ctx.send(error)
        elif isinstance(error, commands.errors.CommandOnCooldown):
            await ctx.send(f"Sorry {ctx.author.mention} You're on cooldown. Try again in {error.retry_after:.2f} seconds.")
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} You missed the `item` or `amount` arguments.")

    @commands.command(name="delete")
    async def delete(self, ctx: commands.Context) -> None:
        """Deletes the economy account associated to the user."""
        if not (await self._has_account(ctx.author.id)):
            no_account_embed = Embed(title="Uh oh!", color=0x2F3136, description=f"Hey {ctx.author.mention} You dont have a World account, Run the following command `w/create`")
            await ctx.send(embed=no_account_embed)
        else:
            await self._database_collection.delete_one({"_id": ctx.author.id})
            delete_account_embed = Embed(title="Goodbye", color=0x2F3136, description=f"Hey {ctx.author.mention} I have successfully removed your World account.")
            await ctx.send(embed=delete_account_embed)

    @commands.command(name="create")
    async def create(self, ctx: commands.Context) -> None:
        """Creates a World account."""
        if (await self._has_account(ctx.author.id)):
            has_account_embed = Embed(title="Uh oh!", color=0x2F3136, description=f"Hey {ctx.author.mention} You already have a World account.")
            await ctx.send(embed=has_account_embed)
        else:
            await self._create_account(ctx.author.id)
            create_account_embed = Embed(title="Welcome!", color=0x2F3136, description=f"Hey {ctx.author.mention} I have successfully made your World account.")
            await ctx.send(embed=create_account_embed)

    @commands.command(name="status")
    async def status(self, ctx: commands.Context, *, status: str) -> None:
        """Sets a custom status for the user."""
        if not (await self._has_account(ctx.author.id)):
            await self._create_account(ctx.author.id)

        if len(status) > 80:
            await ctx.send(f"Hey {ctx.author.mention} Your status message is too big. Try to keep it smaller than 80 chars.")
            return

        await self._database_collection.update_one(
            {
                "_id": ctx.author.id
            },
            {
                "$set": {
                    "afk": status
                }
            }
        )
        status_embed = Embed(title="Status", color=0x2F3136, description=f"Hey {ctx.author.mention} I have set your current status to `{status}`.")
        await ctx.send(embed=status_embed)

    @status.error
    async def status_error(self, ctx: commands.Context, error: commands.errors.CommandInvokeError) -> None:
        """Handles errors when running the status command."""
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} You missed the `status` argument.")

    @commands.command(name="gamble")
    async def gamble(self, ctx: commands.Context, amount: UnsignedIntegerConverter) -> None:
        """
        Gambles your amount money.

        If you win, you get your money back but doubled, Otherwise, you lose it.
        The winning percentage is 15%.
        """
        if not (await self._has_account(ctx.author.id)):
            await self._create_account(ctx.author.id)

        user = await self._get_user(ctx.author.id)
        if user.coins < amount:
            raise NotEnoughCoins(f"Sorry {ctx.author.mention} The amount of money to gamble is larger than your current balance.")

        await self._database_collection.update_one(
            {
                "_id": ctx.author.id
            },
            {
                "$set": {
                    "coins": user.coins - amount
                }
            }
        )

        # Get percentage
        random.seed(datetime.now().timestamp())
        percentage = random.randint(0, 100)
        if percentage <= 85:
            lost_embed = Embed(title="You lost.", color=0x2F3136, description=f"Hey {ctx.author.mention} You have lost {amount} coin{'s' if amount > 1 else ''}.")
            await ctx.send(embed=lost_embed)
            return

        user = await self._get_user(ctx.author.id)
        await self._database_collection.update_one(
            {
                "_id": user._id
            },
            {
                "$set": {
                    "coins": user.coins + (amount * 2)
                }
            }
        )
        win_embed = Embed(title="Congrats!", color=0x2F3136, description=f"Hey {ctx.author.mention} You have won `{amount}` coins.")
        await ctx.send(embed=win_embed)

    @commands.command(name="roulette")
    async def roulette(self, ctx: commands.Context, amount: UnsignedIntegerConverter, choice: UnsignedIntegerConverter) -> None:
        """
        Roulette.

        If you win, you get triple the money, Otherwise, if you loose
        Then the money that you rouletted will be removed.
        """
        if choice > 100:
        	return await ctx.send(f"Sorry {ctx.author.mention} you can only pick a number between 1 and 100.")

        if not (await self._has_account(ctx.author.id)):
            await self._create_account(ctx.author.id)

        user = await self._get_user(ctx.author.id)
        if user.coins < amount:
            raise NotEnoughCoins(f"Sorry {ctx.author.mention} The amount of money to roulette is larger than your current balance.")

        await self._database_collection.update_one(
            {
                "_id": ctx.author.id
            },
            {
                "$set": {
                    "coins": user.coins - amount
                }
            }
        )

        random.seed(datetime.now().timestamp())
        percentage = random.randint(1, 100)
        if percentage is not choice:
            embed_lost = Embed(title="Roulette", color=0x2F3136, description=f"Hey {ctx.author.mention} You have lost {amount} coin{'s' if amount > 1 else ''}.\nYou chose `{choice}`\nWorld chose: `{percentage}`")
            await ctx.send(embed=embed_lost)
            return

        user = await self._get_user(ctx.author.id)
        await self._database_collection.update_one(
            {
                "_id": user._id
            },
            {
                "$set": {
                    "coins": user.coins + (amount * 3)
                }
            }
        )
        embed_win = Embed(title="Roulette!", color=0x2F3136, description=f"Hey {ctx.author.mention} You have won `{amount * 3}` coins.\nYou chose `{choice}`\nWorld chose `{percentage}`")
        await ctx.send(embed=embed_win)

    @commands.command(name="beg")
    @commands.cooldown(1, 45, BucketType.member)
    async def beg(self, ctx: commands.Context) -> None:
        """User can beg for coins, and World will generate a random number between 10 and 300."""
        if not (await self._has_account(ctx.author.id)):
            await self._create_account(ctx.author.id)

        random.seed(datetime.now().timestamp())
        amount_of_coins = random.randint(0, 300)
        user = await self._get_user(ctx.author.id)
        await self._database_collection.update_one(
            {
                "_id": user._id
            },
            {
                "$set": {
                    "coins": user.coins + amount_of_coins
                }
            }
        )
        beg_embed = Embed(
            title="You have begged.",
            color=0x2F3136,
            description=f"Amount given from World: `{amount_of_coins}` Coins\nCurrent balance: `{user.coins + amount_of_coins:.2f}` Coins"
        )
        await ctx.send(embed=beg_embed)

    @roulette.error
    async def roulette_error(self, ctx: commands.Context, error: commands.errors.CommandInvokeError) -> None:
        """Handles errors when running the gamble command."""
        error = getattr(error, "original", error)
        if isinstance(error, NotEnoughCoins):
            await ctx.send(error)
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} You ran that command wrong, here's how you should run it: `w/roulette <amount> <choice>`")

    @beg.error
    async def beg_error(self, ctx: commands.Context, error: commands.errors.CommandInvokeError) -> None:
        """Handles errors when running the beg command."""
        if isinstance(error, commands.errors.CommandOnCooldown):
            await ctx.send(f"Sorry {ctx.author.mention} Try again in {error.retry_after:.2f} seconds.")

    @gamble.error
    async def gamble_error(self, ctx: commands.Context, error: commands.errors.CommandInvokeError) -> None:
        """Handles errors when running the gamble command."""
        error = getattr(error, "original", error)
        if isinstance(error, NotEnoughCoins):
            await ctx.send(error)
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} You missed the `amount` argument.")

    @commands.command(name="daily")
    @commands.cooldown(1, 86400, BucketType.member)
    async def daily(self, ctx: commands.Context) -> None:
        """Gives to the user a daily account of money."""
        if not (await self._has_account(ctx.author.id)):
            await self._create_account(ctx.author.id)

        user = await self._get_user(ctx.author.id)
        await self._database_collection.update_one(
            {
                "_id": user._id
            },
            {
                "$set": {
                    "coins": user.coins + 200
                }
            }
        )
        daily_embed = Embed(title="Daily", color=0x2F3136, description=f"Hey {ctx.author.mention} You successfully received your daily amount of `200` coins.")
        await ctx.send(embed=daily_embed)

    @daily.error
    async def daily_error(self, ctx: commands.Context, error: commands.errors.CommandInvokeError) -> None:
        """Handles errors when running the daily command."""
        if isinstance(error, commands.errors.CommandOnCooldown):
            await ctx.send(f"Sorry {ctx.author.mention} Try again in {error.retry_after / 3600:.2f} hours.")

    @commands.command(name="weekly")
    @commands.cooldown(1, 604800, BucketType.member)
    async def weekly(self, ctx: commands.Context) -> None:
        """Gives to the user a weekly account of money."""
        if not (await self._has_account(ctx.author.id)):
            await self._create_account(ctx.author.id)

        user = await self._get_user(ctx.author.id)
        await self._database_collection.update_one(
            {
                "_id": user._id
            },
            {
                "$set": {
                    "coins": user.coins + 800
                }
            }
        )
        weekly_embed = Embed(title="Weekly", color=0x2F3136, description=f"Hey {ctx.author.mention} You successfully received your weekly amount of `800` coins.")
        await ctx.send(embed=weekly_embed)

    @weekly.error
    async def weekly_error(self, ctx: commands.Context, error: commands.errors.CommandInvokeError) -> None:
        """Handles errors when running the weekly command."""
        if isinstance(error, commands.errors.CommandOnCooldown):
            await ctx.send(f"Sorry {ctx.author.mention} Try again in {error.retry_after / 86400:.2f} days.")

    @commands.command(name="transfer")
    async def transfer(self, ctx: commands.Context, target: Member, amount: UnsignedIntegerConverter) -> None:
        """
        Transfers an amount of money to the target specified.

        The target is a member from your Discord server.
        """
        if not (await self._has_account(ctx.author.id)):
            await self._create_account(ctx.author.id)

        user = await self._get_user(ctx.author.id)
        target_user_object = await self._get_user(target.id)

        if amount > user.coins:
            raise NotEnoughCoins(f"Sorry {ctx.author.mention} You don't have enough coins to perform this operation.")

        await self._database_collection.update_one(
            {
                "_id": user._id
            },
            {
                "$set": {
                    "coins": user.coins - amount
                }
            }
        )
        await self._database_collection.update_one(
            {
                "_id": target_user_object._id
            },
            {
                "$set": {
                    "coins": target_user_object.coins + amount
                }
            }
        )
        daily_embed = Embed(
            title="Transfer",
            color=0x2F3136,
            description=f"Hey {ctx.author.mention} You have successfully transfered `{amount}` coin{'s' if amount > 1 else ''} to {target.mention}."
        )
        await ctx.send(embed=daily_embed)

    @transfer.error
    async def tranfer_error(self, ctx: commands.Context, error: commands.errors.CommandInvokeError) -> None:
        """Handles errors when running the tranfer command."""
        error = getattr(error, "original", error)
        if isinstance(error, NotEnoughCoins):
            await ctx.send(error)
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} You forgot to mention the member.")
        elif isinstance(error, commands.errors.BadArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Member not found, or invalid coin amount.")
        elif isinstance(error, UserNotFound):
            await ctx.send(f"Sorry {ctx.author.mention} Your target does not have a World account.")

    def _connect_to_database(self) -> None:
        """
        Connects into the MongoDB database.
        The URL is specified on the `MONGODB_URL` key in the `.env` file
        in the root directory of this folder.
        This doesn't return anything, in fact, this just sets `self._database_collection`.
        """
        load_dotenv()
        self._database_collection = motor.motor_asyncio.AsyncIOMotorClient(
            os.environ["MONGODB_URL"]
        )["Coins"]["UserCoins"]

    async def _get_user(self, user_id: int) -> User:
        """
        Gets a user from the Coins collection.
        Returns a `User` object.
        Raises `UserNotFound` if the user was not found.
        """
        user_data = await self._database_collection.find_one(
            {"_id": user_id}
        )
        if not user_data:
            raise UserNotFound(f"User with ID {user_id} is not found on the Coins collection")

        user_object = User(
            user_id, user_data["coins"], user_data["cookie"], user_data["choc"],
            user_data["poop"], user_data["apple"], user_data["afk"]
        )
        return user_object

    async def _buy(self, item: Item, amount: int, user: User) -> None:
        """
        The core of the `buy` command.

        This performs the buy operation. This will check if the user has enough coins,
        substract the coins from the user account, and add the specified item into the
        user inventory.
        """
        if user.coins - (item.price * amount) < 0:
            raise NotEnoughCoins(f"Sorry <@{user._id}> You don't have enough coins to buy this item.")

        await self._database_collection.update_one(
            {
                "_id": user._id
            },
            {
                "$set": {
                    "coins": user.coins - (item.price * amount),
                    item.name: getattr(user, item.name) + amount
                }
            }
        )

    async def _sell(self, item: Item, amount: int, user: User) -> Union[Literal[False], int]:
        """
        The core of the `sell` command.

        You have a 75% chance to sell the items successfully, and a 25% chance to loose it.
        Returns False if the user was robbed, or the coins amount (int) if the items were sold
        successfully.
        """
        if getattr(user, item.name) < amount:
            raise NotEnoughItems(f"Sorry <@{user._id}> You don't have enough items to perform this operation.")

        await self._database_collection.update_one(
            {
                "_id": user._id
            },
            {
                "$set": {
                    item.name: getattr(user, item.name) - amount
                }
            }
        )

        # Get the chance
        random.seed(datetime.now().timestamp())
        chance = random.randint(0, 100)
        if chance >= 75:
            return False

        coins_earned = (item.price * amount / 100 * 15) + item.price * amount

        await self._database_collection.update_one(
            {
                "_id": user._id
            },
            {
                "$set": {
                    "coins": user.coins + coins_earned
                }
            }
        )

        return coins_earned

    async def _create_account(self, user_id: int) -> None:
        """Creates a record, setting the record's author as user_id."""
        await self._database_collection.insert_one({
            "_id": user_id,
            "coins": 100,
            "cookie": 0,
            "choc": 0,
            "poop": 0,
            "apple": 0,
            "afk": "No status set, run w/status to set a status"
        })

    async def _has_account(self, user_id: int) -> None:
        """Returns True if the user_id has an account. Otherwise False."""
        return bool(await self._database_collection.find_one(
            {"_id": user_id}
        ))


def setup(bot: commands.Bot) -> None:
    """Adds the EconomyBot into the bot."""
    bot.add_cog(EconomyCog())
