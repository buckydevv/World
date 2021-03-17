from random import randint, seed
from textwrap import dedent
from dataclasses import dataclass
from os import environ
from typing import Literal, Union
from discord import Embed, Member
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from datetime import datetime
from framework import require_account, Wealth
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
    Bank: int
    beans: int
    pizza: int
    waffles: int
    Fish: int
    LastTransfer: str
    #Premium: str -> Being added soon
    #Wallet: int -> Being added soon
    #Tickets: int -> Being added soon
    #TicketReason: str -> Being added soon
    #WorldFriends: int -> Being added soon
    #IsBlacklisted: str -> Being added soon
    #CurrentJob: str -> Being added soon


class Item(type):
    """Base class for a World item."""
    pass

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

class Beans(metaclass=Item):
    """Represents a World item."""

    name = "beans"
    price = 10

class Pizza(metaclass=Item):
    """Represents a World item."""

    name = "pizza"
    price = 15

class Waffles(metaclass=Item):
    """Represents a World item."""

    name = "waffles"
    price = 20

class Fish(metaclass=Item):
    """Represents a World item."""

    name = "Fish"
    price = 30


class ItemConverter(commands.Converter):
    """Converts a string into a World item."""
    def __init__(self, *args, **kwargs):
        self.items = {
            Cookie: ("cookie", "cookies"),
            Choc: ("chocbar", "choc", "chocbars", "chocs"),
            Poop: ("poop", "poops"),
            Apple: ("apple", "apples"),
            Beans: ("beans", "bean"),
            Pizza: ("pizza", "pizzas"),
            Waffles: ("waffle", "waffles"),
            Fish: ("fish", "fishes")
        }

    async def convert(self, ctx: commands.Context, argument: str) -> Item:
        """Converts a string into a World item."""
        argument = argument.lower()
        for key in self.items.keys():
            if argument in self.items[key]:
                return key

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

    def __init__(self, color):
        """Sets up the cog."""
        self.color = color

    @commands.command(name="shop", aliases=("items", ))
    async def shop(self, ctx: commands.Context):
        """Returns all items you can buy or sell."""
        await ctx.send(embed=Embed(
            title="Shop",
            description=dedent("""
                - Cookies
                `1 coin per cookie.`
                - Chocbars
                `4 coins per choc.`
                - Poops
                `6 coins per poop.`
                - Apples
                `10 coins per apple.`
                - Beans
                `10 coins per bean.`
                - Waffles
                `15 coins per waffle.`
                - Pizzas
                `20 coins per pizza.`
                - Fish
                `30 coins per Fish.`
            """),
            color=self.color
        ))

    @commands.command(name="inventory", aliases=("inv", ))
    @require_account()
    async def inventory(self, ctx: commands.Context):
        """Returns the current items from the user inventory."""

        author = self._get_user(ctx.author.id)
        await ctx.send(embed=Embed(title=f"{ctx.author}'s inventory", color=self.color
        ).add_field(name="Coins", value=f":moneybag: {author.coins:,}"
        ).add_field(name="Apples", value=f":apple: {author.apple}"
        ).add_field(name="Cookies", value=f":cookie: {author.cookie}"
        ).add_field(name="Chocolate bars", value=f":chocolate_bar: {author.choc}"
        ).add_field(name="Poops", value=f":poop: {author.poop}"
        ).add_field(name="Beans", value=f"<:beanworld:774371828629635132> {author.beans}"
        ).add_field(name="Pizza", value=f":pizza: {author.pizza}"
        ).add_field(name="Waffles", value=f":waffle: {author.waffles}"
        ).add_field(name="Fish", value=f":fish: {author.Fish}"
        ).set_thumbnail(url=ctx.author.avatar_url))

    @commands.command(name="balance", aliases=("bal", ))
    @require_account()
    async def balance(self, ctx: commands.Context, member: Member=None):
        """Returns the current balance of the user."""
        user = member or ctx.author
        data = self._get_user(user.id)
        await ctx.send(embed=Embed(
            title=f"{user}'s balance",
            color=self.color,
            description=f"Coins: `{data.coins:,.0f}`\nBank: `{data.Bank:,.0f}`"
        ))

    @commands.command(name="buy")
    @require_account()
    async def buy(self, ctx: commands.Context, item: ItemConverter, amount: UnsignedIntegerConverter):
        """
        Buys items.
        Run `w/shop` for a list of items.
        """
        user = self._get_user(ctx.author.id)
        await self._buy(item, amount, user)
        await ctx.send(embed=Embed(
            title="You successfully bought",
            color=self.color,
            description=f"{ctx.author.mention} bought `{amount} {item.name}{'s' if amount > 1 else ''}`\n\nTo see your inventory run the command `w/inventory`"
        ))

    @buy.error
    async def buy_error(self, ctx: commands.Context, error: commands.errors.CommandInvokeError):
        """Handles errors when buying something."""
        error = getattr(error, "original", error)
        if isinstance(error, NotEnoughCoins) or isinstance(error, commands.errors.BadArgument):
            await ctx.send(error)
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} You missed the `item` or `amount` arguments.")

    @commands.command(name="sell")
    @commands.cooldown(1, 60, BucketType.member)
    @require_account()
    async def sell(self, ctx: commands.Context, item: ItemConverter, amount: UnsignedIntegerConverter):
        """
        Sells items.
        Run `w/shop` for a list of items.
        """
        user = self._get_user(ctx.author.id)
        coins_earned = await self._sell(item, amount, user)
        if not coins_earned:
            return await ctx.send(embed=Embed(title="Sorry", color=self.color, description=f"Sorry {ctx.author.mention} your items couldn't be sold because you got robbed. Good luck the next time!"))
        return await ctx.send(embed=Embed(title="Congrats!", color=self.color, description=f"Hey {ctx.author.mention} You sold your items successfully! You earned `{coins_earned:.0f}` coins."))

    @commands.command(name="rob")
    @commands.cooldown(1, 1800, BucketType.member)
    @require_account()
    async def rob(self, ctx: commands.Context, user: Member):
        """Rob a user!"""
        if user.id == ctx.author.id:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send(f"Sorry {ctx.author.mention} you can't rob yourself silly <:Worldkek:768145777926078474>")
        elif user.bot:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send(f"Sorry {ctx.author.mention} you can't rob a bot silly <:Worldkek:768145777926078474>")
        
        target = self._get_user(user.id)
        if not target.coins:
            return await ctx.send(f"Sorry {ctx.author.mention} That user has no coins, try again next time!")
        robbed_amount = randint(1, round(target.coins))
        Wealth.collection.update_one({"_id": user.id}, {"$inc": {"coins": -robbed_amount}})
        Wealth.collection.update_one({"_id": ctx.author.id}, {"$inc": {"coins": robbed_amount}})

        await ctx.send(embed=Embed(
            title="Rob",
            description=f"{ctx.author.mention} you haved robbed `{robbed_amount}` coins from {user.mention}",
            color=self.color
        ))

    @rob.error
    async def rob_error(self, ctx: commands.Context, error: commands.errors.CommandInvokeError):
        """Handles errors when running the rob command."""
        error = getattr(error, "original", error)
        if isinstance(error, NotEnoughCoins):
            await ctx.send(error)
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Invalid argument please type `world rob <@user>`")
        elif isinstance(error, commands.errors.BadArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Member not found, or invalid coin amount.")
        elif isinstance(error, commands.errors.CommandOnCooldown):
            await ctx.send(f"Sorry {ctx.author.mention} You're on cooldown. Try again in {error.retry_after:,} seconds.")
        elif isinstance(error, UserNotFound):
            await ctx.send(f"Sorry {ctx.author.mention} Your target does not have a World account.")

    @sell.error
    async def sell_error(self, ctx: commands.Context, error: commands.errors.CommandInvokeError):
        """Handles errors when buying something."""
        error = getattr(error, "original", error)
        if isinstance(error, NotEnoughItems) or isinstance(error, commands.errors.BadArgument):
            return await ctx.send(error)
        elif isinstance(error, commands.errors.CommandOnCooldown):
            return await ctx.send(f"Sorry {ctx.author.mention} You're on cooldown. Try again in {error.retry_after:,} seconds.")
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            return await ctx.send(f"Sorry {ctx.author.mention} You missed the `item` or `amount` arguments.")

    @commands.command(name="delete")
    async def delete(self, ctx: commands.Context):
        """Deletes the economy account associated to the user."""
        if not Wealth.collection.find_one({"_id": ctx.author.id}):
            return await ctx.send(embed=Embed(title="Uh oh!", color=self.color, description=f"Hey {ctx.author.mention} You dont have a World account, Run the following command `w/create`"))
        Wealth.collection.delete_one({"_id": ctx.author.id})
        return await ctx.send(embed=Embed(title="Goodbye", color=self.color, description=f"Hey {ctx.author.mention} I have successfully removed your World account."))

    @commands.command(name="leaderboard", aliases=("lb", ))
    @commands.cooldown(1, 10, BucketType.member) # better have cooldown
    async def leaderboard(self, ctx: commands.Context):
        """Fetches the global leaderboard."""
        await ctx.trigger_typing()
        data = list(Wealth.collection.find())
        
        if 'server' in ctx.message.content.lower():
            _map = map(lambda x: x.id, ctx.guild.members)
            data = list(filter(lambda x: x.get('_id', 0) in _map, data))
        
        sorted_bal = sorted(map(lambda x: x.get('coins', 0), data))[::-1][:10]
        ids = []
        description = ""
        
        for i, bal in enumerate(sorted_bal):
            _data = list(filter(lambda x: x.get('coins', 0) == bal and x["_id"] not in ids, data))[0]
            ids.append(_data["_id"])
            user = ctx.bot.get_user(_data["_id"])
            description += f"{i + 1}. **{user.name if user else '`Unknown`'}** {_data['coins']:,.0f} :moneybag:" + "\n"
        
        return await ctx.send(embed=Embed(title="World Leaderboard", color=self.color, description=description))

    @leaderboard.error
    async def leaderboard_error(self, ctx: commands.Context, error: commands.errors.CommandInvokeError):
        """Handles errors when running the rob command."""
        error = getattr(error, "original", error)
        if isinstance(error, commands.errors.CommandOnCooldown):
            await ctx.send(f"Sorry {ctx.author.mention} You're on cooldown. Try again in {error.retry_after:,} seconds.")

    @commands.command(name="create")
    async def create(self, ctx: commands.Context):
        """Creates a World account."""
        if not Wealth.collection.find_one({"_id": ctx.author.id}):
            return await ctx.send(embed=Embed(title="Uh oh!", color=self.color, description=f"Hey {ctx.author.mention} You already have a World account."))
        Wealth._create_account(ctx.author.id)
        return await ctx.send(embed=Embed(title="Welcome!", color=self.color, description=f"Hey {ctx.author.mention} I have successfully made your World account."))

    @commands.command(name="status")
    @require_account()
    async def status(self, ctx: commands.Context, *, status: str):
        """Sets a custom status for the user."""
        Wealth.collection.update_one(
            {
                "_id": ctx.author.id
            },
            {
                "$set": {
                    "afk": status[:80]
                }
            }
        )
        await ctx.send(embed=Embed(title="Status", color=self.color, description=f"Hey {ctx.author.mention} I have set your current status to `{status[:80]}`."))

    @status.error
    async def status_error(self, ctx: commands.Context, error: commands.errors.CommandInvokeError):
        """Handles errors when running the status command."""
        if isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} You missed the `status` argument.")

    @commands.command(name="gamble")
    @require_account()
    async def gamble(self, ctx: commands.Context, amount: UnsignedIntegerConverter):
        """
        Gambles your amount money.
        If you win, you get your money back but doubled, Otherwise, you lose it.
        The winning percentage is 15%.
        """

        user = self._get_user(ctx.author.id)
        if user.coins < amount:
            raise NotEnoughCoins(f"Sorry {ctx.author.mention} The amount of money to gamble is larger than your current balance.")

        Wealth.collection.update_one(
            {
                "_id": ctx.author.id
            },
            {
                "$inc": {
                    "coins": -amount
                }
            }
        )

        # Get percentage
        seed(datetime.now().timestamp())
        percentage = randint(0, 100)
        if percentage <= 75:
            return await ctx.send(embed=Embed(title="You lost.", color=self.color, description=f"Hey {ctx.author.mention} You have lost {amount} coin{'s' if amount > 1 else ''}.\nYou had a {percentage}% chance of winning."))

        user = self._get_user(ctx.author.id)
        Wealth.collection.update_one(
            {
                "_id": user._id
            },
            {
                "$inc": {
                    "coins": amount * 2
                }
            }
        )
        await ctx.send(embed=Embed(title="Congrats!", color=self.color, description=f"Hey {ctx.author.mention} You have won `{amount}` coins."))

    @commands.command(name="roulette")
    @require_account()
    async def roulette(self, ctx: commands.Context, amount: UnsignedIntegerConverter, choice: UnsignedIntegerConverter):
        """
        Roulette.
        If you win, you get triple the money, Otherwise, if you loose
        Then the money that you rouletted will be removed.
        """
        if choice > 100:
            return await ctx.send(f"Sorry {ctx.author.mention} you can only pick a number between 1 and 100.")
        user = self._get_user(ctx.author.id)
        if user.coins < amount:
            raise NotEnoughCoins(f"Sorry {ctx.author.mention} The amount of money to roulette is larger than your current balance.")

        Wealth.collection.update_one(
            {
                "_id": ctx.author.id
            },
            {
                "$inc": {
                    "coins": -amount
                }
            }
        )

        seed(datetime.now().timestamp())
        percentage = randint(1, 100)
        if percentage is not choice:
            return await ctx.send(embed=Embed(title="Roulette", color=self.color, description=f"Hey {ctx.author.mention} You have lost {amount} coin{'s' if amount > 1 else ''}.\nYou chose `{choice}`\nWorld chose: `{percentage}`"))

        user = self._get_user(ctx.author.id)
        Wealth.collection.update_one(
            {
                "_id": user._id
            },
            {
                "$inc": {
                    "coins": amount * 3
                }
            }
        )
        await ctx.send(embed=Embed(title="Roulette!", color=self.color, description=f"Hey {ctx.author.mention} You have won `{amount * 3}` coins.\nYou chose `{choice}`\nWorld chose `{percentage}`"))

    @commands.command(name="beg")
    @commands.cooldown(1, 45, BucketType.member)
    @require_account()
    async def beg(self, ctx: commands.Context):
        """User can beg for coins, and World will generate a random number between 10 and 300."""
        seed(datetime.now().timestamp())
        amount_of_coins = randint(0, 300)
        user = self._get_user(ctx.author.id)
        Wealth.collection.update_one(
            {
                "_id": ctx.author.id
            },
            {
                "$inc": {
                    "coins": amount_of_coins
                }
            }
        )
        await ctx.send(embed=Embed(
            title="You have begged.",
            color=self.color,
            description=f"Amount given from World: `{amount_of_coins}` Coins\nCurrent balance: `{user.coins + amount_of_coins:,}` Coins"
        ))

    @roulette.error
    async def roulette_error(self, ctx: commands.Context, error: commands.errors.CommandInvokeError):
        """Handles errors when running the gamble command."""
        error = getattr(error, "original", error)
        if isinstance(error, NotEnoughCoins):
            await ctx.send(error)
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} You ran that command wrong, here's how you should run it: `w/roulette <amount> <choice>`")

    @beg.error
    async def beg_error(self, ctx: commands.Context, error: commands.errors.CommandInvokeError):
        """Handles errors when running the beg command."""
        if isinstance(error, commands.errors.CommandOnCooldown):
            await ctx.send(f"Sorry {ctx.author.mention} Try again in {error.retry_after:,} seconds.")

    @gamble.error
    async def gamble_error(self, ctx: commands.Context, error: commands.errors.CommandInvokeError):
        """Handles errors when running the gamble command."""
        error = getattr(error, "original", error)
        if isinstance(error, NotEnoughCoins):
            await ctx.send(error)
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} You missed the `amount` argument.")

    @commands.command(name="daily")
    @commands.cooldown(1, 86400, BucketType.member)
    @require_account()
    async def daily(self, ctx: commands.Context):
        """Gives to the user a daily account of money."""
        Wealth.collection.update_one(
            {
                "_id": ctx.author.id
            },
            {
                "$inc": {
                    "coins": 200
                }
            }
        )
        await ctx.send(embed=Embed(title="Daily", color=self.color, description=f"Hey {ctx.author.mention} You successfully received your daily amount of `200` coins."))

    @daily.error
    async def daily_error(self, ctx: commands.Context, error: commands.errors.CommandInvokeError):
        """Handles errors when running the daily command."""
        if isinstance(error, commands.errors.CommandOnCooldown):
            await ctx.send(f"Sorry {ctx.author.mention} Try again in {error.retry_after / 3600:,} hours.")

    @commands.command(name="weekly")
    @commands.cooldown(1, 604800, BucketType.member)
    @require_account()
    async def weekly(self, ctx: commands.Context):
        """Gives to the user a weekly account of money."""
        Wealth.collection.update_one(
            {
                "_id": ctx.author._id
            },
            {
                "$inc": {
                    "coins": 800
                }
            }
        )
        await ctx.send(embed=Embed(title="Weekly", color=self.color, description=f"Hey {ctx.author.mention} You successfully received your weekly amount of `800` coins."))

    @weekly.error
    async def weekly_error(self, ctx: commands.Context, error: commands.errors.CommandInvokeError):
        """Handles errors when running the weekly command."""
        if isinstance(error, commands.errors.CommandOnCooldown):
            await ctx.send(f"Sorry {ctx.author.mention} Try again in {error.retry_after / 86400:,} days.")

    @commands.command(name="transfer")
    @require_account()
    async def transfer(self, ctx: commands.Context, target: Member, amount: UnsignedIntegerConverter):
        """
        Transfers an amount of money to the target specified.
        The target is a member from your Discord server.
        """
        if target.id == ctx.author.id:
            return await ctx.send(f"Sorry {ctx.author.mention} but you can\'t transfer money to yourself dummy!")
        elif target.bot:
            return await ctx.send(f"Sorry {ctx.author.mention} but you can\'t transfer money to a bot dummy!")
        now = datetime.now()
        user = self._get_user(ctx.author.id)
        if amount > user.coins:
            raise NotEnoughCoins(f"Sorry {ctx.author.mention} You don't have enough coins to perform this operation.")

        Wealth.collection.update_one(
            {
                "_id": user._id
            },
            {
                "$set": {
                    "coins": user.coins - amount,
                    "LastTransfer": now.strftime("%m/%d/%Y at %H:%M:%S")
                }
            }
        )
        Wealth.collection.update_one(
            {
                "_id": target.id
            },
            {
                "$inc": {
                    "coins": amount
                }
            }
        )
        await ctx.send(embed=Embed(
            title="Transfer",
            color=self.color,
            description=f"Hey {ctx.author.mention} You have successfully transfered `{amount}` coin{'s' if amount > 1 else ''} to {target.mention}.\nYour Last Transfer: `{user.LastTransfer}`"
        ))

    @transfer.error
    async def tranfer_error(self, ctx: commands.Context, error: commands.errors.CommandInvokeError):
        """Handles errors when running the tranfer command."""
        error = getattr(error, "original", error)
        if isinstance(error, NotEnoughCoins):
            return await ctx.send(error)
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            return await ctx.send(f"Sorry {ctx.author.mention} Invalid argument please type `world transfer <@user? <amount>")
        elif isinstance(error, commands.errors.BadArgument):
            return await ctx.send(f"Sorry {ctx.author.mention} Member not found, or invalid coin amount.")
        elif isinstance(error, UserNotFound):
            return await ctx.send(f"Sorry {ctx.author.mention} Your target does not have a World account.")

    def _get_user(self, user_id: int) -> User:
        """
        Gets a user from the Coins collection.
        Returns a `User` object.
        Raises `UserNotFound` if the user was not found.
        """
        user_data = Wealth.collection.find_one(
            {"_id": user_id}
        )
        if not user_data:
            raise UserNotFound(f"User with ID {user_id} is not found on the Coins collection")

        return User(
            user_id, user_data["coins"], user_data["cookie"], user_data["choc"],
            user_data["poop"], user_data["apple"], user_data["afk"], user_data["Bank"],
            user_data["beans"], user_data["pizza"], user_data["waffles"], user_data["Fish"],
            user_data["LastTransfer"]
        )

    def _buy(self, item: Item, amount: int, user: User):
        """
        The core of the `buy` command.
        This performs the buy operation. This will check if the user has enough coins,
        substract the coins from the user account, and add the specified item into the
        user inventory.
        """
        if (user.coins - (item.price * amount)) < 0:
            raise NotEnoughCoins(f"Sorry <@{user._id}> You don't have enough coins to buy this item.")

        Wealth.collection.update_one(
            {
                "_id": user._id
            },
            {
                "$inc": {
                    "coins": -(item.price * amount),
                    item.name: amount
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

        Wealth.collection.update_one(
            {
                "_id": user._id
            },
            {
                "$inc": {
                    item.name: -amount
                }
            }
        )

        # Get the chance
        seed(datetime.now().timestamp())
        chance = randint(0, 100)
        if chance >= 75:
            return False

        coins_earned = (item.price * amount / 100 * 15) + item.price * amount

        Wealth.collection.update_one(
            {
                "_id": user._id
            },
            {
                "$inc": {
                    "coins": coins_earned
                }
            }
        )

        return coins_earned

def setup(bot):
    bot.add_cog(EconomyCog(bot.color))
