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
    filters = {}
    try:
        seconds = int(args)
    except ValueError:
        return "You must provide a integer value"
    filters.update({'time': seconds})
    return filters

class VoiceRecorder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sink = discord.Sink

    @commands.command(help="Record your voice in a Discord VoiceChannel")
    @commands.cooldown(1, 30, BucketType.user)
    async def record(self, ctx, seconds: int):
        if not ctx.author.voice:
            return await ctx.send("You are not in a voice channel, Please connect to one and then run the command.")
        if seconds >=60:
            return await ctx.send("Sorry, `60` Seconds is max.")
        self.vc = await ctx.author.voice.channel.connect()
        self.vc.start_recording(self.sink(encoding='wav', filters=args_to_filters(seconds), output_path="recordings"), on_stopped, ctx.channel)
        fm = await ctx.send(f"The recording has started!")
        await sleep(seconds + 1)
        #self.sink.format_audio(self) # This was for DSR, But having troubles with it :z
        ssrc = self.vc.rssrc(ctx.author) # Get ID and File name
        await self.vc.disconnect() # Disconnect because we no longer need to be inside of the voice channel
        await fm.edit(content="Here is the recording i have took!")
        await ctx.send(file=File(f"recordings/{ssrc[ctx.author.id]}.wav"))
        remove(f"recordings/{ssrc[ctx.author.id]}.wav") # Save space :P
        #receive = dsr.listen(f"recordings/{ssrc[ctx.author.id]}.wav") # Pass the File to DSR.
        #await ctx.send("Checking file...", delete_after=seconds) # Just wait for dsr to check
        #await sleep(seconds)
        #await ctx.send(receive) # Send what DSR recognized.
        
    
    @record.error
    async def record_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"Try again in {error.retry_after:.2f}s.")
        elif isinstance(error, commands.BadArgument):
            return await ctx.send("Try `w/record 10`, This will record your voice in the vc for 10 seconds.")

def setup(bot):
    bot.add_cog(VoiceRecorder(bot))