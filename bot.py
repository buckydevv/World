import textwrap
import json

from os import environ, listdir

from discord import (
    Activity,
    ActivityType,
    Embed,
    HTTPException,
    Intents,
    Message,
    Status
)
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

# -------
# Main bot area
world = commands.Bot(
    command_prefix=("w/", "world ", "World "),
    description="Discord Bot Made For All",
    case_insensitive=True,
    intents=Intents.all()
)
world.remove_command("help")


# -------
# Cogs area
cogs = [
    f[:-3] for f in listdir("cogs/")
    if f.endswith(".py")
]

for cog in cogs:
    world.load_extension(f"cogs.{cog}")


# -------
# Blacklist area
with open("blacklisted.json") as f:
    blacklisted_people = json.load(f)


# -------
# Message received area
@world.event
async def on_message(message: Message) -> None:
    """
    Dispatched every time a message is sent.

    Checks if the message wasn't send by a bot, the message wasn't send
    on DMs and the user isn't blacklisted.
    """
    if message.author.bot:
        return
    if not message.guild:
        await message.channel.send((
            "You can't use commands on DMs, invite the bot your server: "
            f"<https://discord.com/oauth2/authorize?client_id={world.user.id}&permissions=8&scope=bot>"
        ))
        return

    if message.author.id in blacklisted_people:
        return
    
    await world.process_commands(message)


# -------
# On ready area
@world.event
async def on_ready() -> None:
    """Dispatched when the bot has successfully connected into Discord."""
    await world.change_presence(
        status=Status.dnd,
        activity=Activity(
            type=ActivityType.listening,
            name="w/help"
        )
    )
    print("Bot connected successfully into Discord!")


# -------
# Error handler area
@world.event
async def on_command_error(ctx: commands.Context, error: commands.errors.CommandInvokeError) -> None:
    """Dispatched when an exception was raised."""
    error = getattr(error, "original", error)
    if environ["DEBUG"] == "1":
        error_msg = textwrap.dedent(f"""
            ------------------
            Error
            
            Cog: {ctx.cog.__class__.__name__}
            Command: {ctx.command}
            Invoker: {ctx.author} ({ctx.author.id})
            Location: {ctx.message.jump_url}
            Input: `{ctx.message.content}`
            
            {error.__class__.__name__}: {error}
            ------------------
        """)
        print(error_msg)

        error_embed = Embed(
            title=":x: Error",
            description=error_msg.strip().strip("-"),
            color=0xff0000
        )
        try:
            error_channel = await world.fetch_channel(763111707379761162)
        except HTTPException:
            return
        await error_channel.send(embed=error_embed)
    else:
        print(f"{error.__class__.__name__}: {error}")


world.run(environ["TOKEN"], bot=True, reconnect=True)