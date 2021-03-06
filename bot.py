#import os, struct
from os import environ, listdir
from json import load, dump
from discord import Activity, Embed, Intents
from discord.ext import commands
from rich import print
from rich.console import Console
from rich.table import Table
console = Console()

__import__("dotenv").load_dotenv()

# -------
# prefix area

defaultprefixes = ["World ", "w/", "world "]
ownerprefix = ["w/", "world ", "World "]

async def get_prefix(world, message):
    if await world.is_owner(message.author):
        return commands.when_mentioned_or(*ownerprefix)(world, message)
    prefixes = load(open('prefixes.json', 'r'))
    if not str(message.guild.id) in prefixes:
        return commands.when_mentioned_or(*defaultprefixes)(world, message)
    return commands.when_mentioned_or(prefixes[str(message.guild.id)])(world, message)

# -------
# Main bot area

world = commands.Bot(
    command_prefix=get_prefix,
    description="Discord Bot Made For All",
    case_insensitive=True,
    intents=Intents.all()
)
setattr(world, "color", 0x2F3136)
world.remove_command("help")

# -------


# -------
# Command area 

@world.command(help="Change the prefix for your discord guild")
@commands.has_permissions(administrator=True)
async def changeprefix(ctx, prefix):
    if len(prefix) > 7:
        return await ctx.send(f"Sorry {ctx.author.mention} a limit of `7` letters please.")
    with open('prefixes.json', 'r') as f:
        prefixes = load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as f:
        dump(prefixes, f, indent=4)
    await ctx.send(embed=Embed(
        title="Custom prefix",
        description=f"Prefix for {ctx.guild} is now `{prefix}`.\nTry using the help command: `{prefix}help`"
    ))


@world.command()
async def enablenoprefix(ctx):
    if await world.is_owner(ctx.author):
        ownerprefix.append("")
        await ctx.send(f"Hey {ctx.author.mention} i have enabled `No Prefix mode`.")

@world.command()
async def disablenoprefix(ctx):
    if await world.is_owner(ctx.author):
        ownerprefix.remove("")
        await ctx.send(f"Hey {ctx.author.mention} i have disabled `No Prefix mode`.")

@changeprefix.error
async def changeprefix_error(ctx, error):
   if isinstance(error, commands.errors.CheckFailure):
       await ctx.send(f"Sorry {ctx.author.mention} you don't have permissions to change the prefix!")

# -------

# -------
# Cogs area
for cog in filter(lambda x: x.endswith(".py"), listdir("cogs/")):
    world.load_extension(f"cogs.{cog[:-3]}")
    print(f"[bold cyan]INFO  [/bold cyan][yellow]COG:[/yellow] [purple]{cog}[/purple] [yellow]is loaded.[/yellow]")

# -------
# Blacklist area
with open("blacklisted.json") as f:
    blacklisted_people = load(f)

# -------
# Message received area
@world.event
async def on_message(message):
    """
    Dispatched every time a message is sent.
    Checks if the message wasn't send by a bot, the message wasn't send
    on DMs and the user isn't blacklisted.
    """
    if message.author.bot or (str(message.author.id) in blacklisted_people):
        return
    elif not message.guild:
        return await message.channel.send((
            "You can't use commands on DMs, invite the bot your server: "
            f"<https://discord.com/oauth2/authorize?client_id={world.user.id}&permissions=8&scope=bot>"
        ))
    
    await world.process_commands(message)


# -------
# Event area
@world.event
async def on_ready():
    """Dispatched when the bot has successfully connected into Discord."""
    await world.change_presence(status="dnd", activity=Activity(type=2, name="w/help"))
    table = Table()
    table.add_column("[bold white]Bot info[/bold white]", justify="left", style="bold blue", no_wrap=True)
    table.add_row(f"[bold cyan]Name:[/bold cyan] {world.user.name}")
    table.add_row(f"[bold cyan]Latency:[/bold cyan] {float(world.latency*1000):.0f}ms")
    table.add_row(f"[bold cyan]Guilds:[/bold cyan] {len(world.guilds)}")
    console.print(table)

@world.event
async def on_guild_remove(guild):
    prefixes = load(open('prefixes.json', 'r'))
    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as f:
        dump(prefixes, f, indent=4)

#bitness = struct.calcsize('P') * 8
#target = 'x64' if bitness > 32 else 'x86'
#filename = os.path.join(os.path.dirname(os.path.abspath(discord.__file__)), 'bin', f'libopus-0.{target}.dll')
#discord.opus.load_opus(filename)
# ^ This is for my project dsr: https://github.com/shuanaongithub/dsr, So just ignore.

world.run(environ["TOKEN"])
