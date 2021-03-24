from discord.ext.commands.cooldowns import BucketType
from discord.ext import commands
import discord
from os import remove
from asyncio import sleep
#from dsr.recognize import dsr
from discord import File

def on_stopped(sink, *args):
    pass

def args_to_filters(args):
    try:
        seconds = int(args)
    except ValueError:
        return "You must provide a integer value"
    return {'time': seconds}

class VoiceRecorder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.encoding = "wav" # This is the format of the file we turn the pcm into.
        self.output_path = "recordings" # The directory to save the .pcm and .wav files.
        self.maxrecint = 60 # This is for how long the bot can record inside of the VoiceChannel.
        self.sink = discord.Sink # Sink class, This is not in the official discord.py package.

    @commands.command(help="Record your voice in a Discord VoiceChannel")
    @commands.cooldown(1, 30, BucketType.user)
    async def record(self, ctx, seconds: int):
        if not ctx.author.voice:
            return await ctx.send("You are not in a voice channel, Please connect to one and then run the command.")
        elif seconds > 60:
            return await ctx.send(f"Sorry, {self.maxrecint} Seconds is max.")
        
        self.vc = await ctx.author.voice.channel.connect() # Connect to the author's VoiceChannel.
        self.vc.start_recording(self.sink(encoding=self.encoding, filters=args_to_filters(seconds), output_path=self.output_path), on_stopped, ctx.channel) # Start the recording state.

        fm = await ctx.send("The recording has started!") # The bot starts recording when the message is sent.
        ssrc = self.vc.rssrc(ctx.author) # This returns the author's ID and the name of the generated file. (pcm in this case as it has not been turned into .wav yet)
        #self.sink.format_audio(self) # Trying to format audio(Need this because dsr can't read becuase of frames or something)
        await sleep(seconds + 1) # After this is when it get turned into a .wav file.
        await self.vc.disconnect() # Disconnect from the VoiceChannel after the recording state has finished(We can check this with `if self.vc.recoding`.)

        await fm.edit(content="Here is the recording i have took!") # Send a pre-message
        await ctx.send(file=File(f"recordings/{ssrc[ctx.author.id]}.wav")) # Semd the actual file from the directory

        remove(f"recordings/{ssrc[ctx.author.id]}.wav") # Remove the file with `os.remove` as this will save lots of space.

        #try:
           # receive = dsr.listen(f"recordings/{ssrc[ctx.author.id]}.wav") # This will listen to the .wav file and recognize it, Then it will return text of what was said.
            #await ctx.send("Checking file...", delete_after=seconds) # Just a pre-message
           # await sleep(seconds) # `seconds` is the argument that the user passed in the command. (How long the file will be... But in some cases the file extends or shortens depends on the bot's ping i think. So in the future i could just check the actual file length and set it to a variable.)
           # await ctx.send(receive) # Send what was recognized.
        #except Exception as e:
            #await ctx.send(e)

def setup(bot):
    bot.add_cog(VoiceRecorder(bot))