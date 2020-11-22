import textwrap
import json
import discord

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
from discord.ext.commands import has_permissions

load_dotenv()

# -------
# prefix area

defaultprefixes = ["World ", "w/", "world "]

ownerprefix = ["w/", "world ", "World "]

async def get_prefix(world, message):
	if await world.is_owner(message.author):
		return commands.when_mentioned_or(*ownerprefix)(world, message)
	with open('prefixes.json', 'r') as f:
		prefixes = json.load(f)
		if not str(message.guild.id) in prefixes:
			return commands.when_mentioned_or(*defaultprefixes)(world, message)
	return commands.when_mentioned_or(prefixes[str(message.guild.id)])(world, message)

# -------
# Main bot area

world = commands.Bot(
    command_prefix=(get_prefix),
    description="Discord Bot Made For All",
    case_insensitive=True,
    intents=Intents.all()
)
world.remove_command("help")

# -------


# -------
# Command area 

@world.command(help="Change the prefix for your discord guild")
@has_permissions(administrator=True)
async def changeprefix(ctx, prefix):
	if len(prefix) >7:
		return await ctx.send(f"Sorry {ctx.author.mention} a limit of `7` letters please.")
	with open('prefixes.json', 'r') as f:
		prefixes = json.load(f)

	prefixes[str(ctx.guild.id)] = prefix

	with open('prefixes.json', 'w') as f:
		json.dump(prefixes, f, indent=4)

	embed = Embed(
		title="Custom prefix",
		description=f"Prefix for {ctx.guild} is now `{prefix}`.\nTry using the help command: `{prefix}help`"
		)
	await ctx.send(embed=embed)


@world.command()
async def enablenoprefix(ctx):
	if await world.is_owner(ctx.author):
		ownerprefix.append("")
		await ctx.send(f"Hey {ctx.author.mention} i have enabled `No Prefix mode`.")
	else:
		return

@world.command()
async def disablenoprefix(ctx):
	if await world.is_owner(ctx.author):
		ownerprefix.remove("")
		await ctx.send(f"Hey {ctx.author.mention} i have disabled `No Prefix mode`.")
	else:
		return

@changeprefix.error
async def changeprefix_error(ctx, error):
   if isinstance(error, discord.ext.commands.errors.CheckFailure):
       await ctx.send(f"Sorry {ctx.author.mention} you don't have permissions to change the prefix!")

# -------

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
        return await message.channel.send((
            "You can't use commands on DMs, invite the bot your server: "
            f"<https://discord.com/oauth2/authorize?client_id={world.user.id}&permissions=8&scope=bot>"
        ))

    if str(message.author.id) in blacklisted_people:
        return
    
    await world.process_commands(message)


# -------
# Event area
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

@world.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

world.run(environ["TOKEN"], bot=True, reconnect=True)
