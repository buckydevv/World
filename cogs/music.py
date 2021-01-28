import wavelink
import asyncio
import re
import itertools
import async_timeout
from discord.ext import commands
from typing import Union
from discord import Embed, Member, VoiceChannel, VoiceState
from datetime import timedelta
from asyncio import TimeoutError

URL_REG = re.compile(r'https?://(?:www\.)?.+')

class Track(wavelink.Track):
    """Wavelink Track object with a requester attribute."""

    __slots__ = ('requester', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args)

        self.requester = kwargs.get('requester')


class Player(wavelink.Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.color = 0x2F3136
        self.context: commands.Context = kwargs.get('context', None)
        if self.context:
            self.dj: Member = self.context.author

        self.queue = asyncio.Queue()
        self.controller = None

        self.waiting = False

    async def invoke_next(self) -> None:
        if self.is_playing or self.waiting:
            return
        try:
            self.waiting = True
            with async_timeout.timeout(120):
                track = await self.queue.get()
        except TimeoutError:
            return await self.disconnect()
        await self.play(track)
        self.waiting = False


class Music(commands.Cog, wavelink.WavelinkMixin):
    def __init__(self, bot):
        self.bot = bot
        self.color = 0x2F3136
        if not hasattr(bot, 'wavelink'):
            self.bot.wavelink = wavelink.Client(bot=self.bot)

        self.bot.loop.create_task(self.start_nodes())

    async def start_nodes(self):
        await self.bot.wait_until_ready() # Wait until bot is ready to make a connection!
        node = await self.bot.wavelink.initiate_node(host='127.0.0.1',port=2333, rest_uri='http://127.0.0.1:2333', password='Worldbot77', identifier='WaveWorld', region='us_central')
        node.set_hook(self.on_event_hook)

    async def start_nodes(self) -> None:
        """Connect and intiate wavelink nodes."""
        await self.bot.wait_until_ready()

        if self.bot.wavelink.nodes:
            previous = self.bot.wavelink.nodes.copy()

            for node in previous.values():
                await node.destroy()

        nodes = {'MAIN': {'host': '127.0.0.1',
                          'port': 2333,
                          'rest_uri': 'http://127.0.0.1:2333',
                          'password': 'Worldbot77',
                          'identifier': 'MAIN',
                          'region': 'us_central'
                          }}

        for n in nodes.values():
            await self.bot.wavelink.initiate_node(**n)
        
    @wavelink.WavelinkMixin.listener(event="on_node_ready")
    async def node_ready_event(self, node: wavelink.node.Node):
        print(f"Node {node} is ready!")


    @wavelink.WavelinkMixin.listener('on_track_stuck')
    @wavelink.WavelinkMixin.listener('on_track_end')
    @wavelink.WavelinkMixin.listener('on_track_exception')
    async def on_player_stop(self, node: wavelink.Node, payload):
        await payload.player.invoke_next()


    @commands.Cog.listener()
    async def on_voice_state_update(self, member: Member, before: VoiceState, after: VoiceState):
        if member.bot:
            return

        player: Player = self.bot.wavelink.get_player(member.guild.id, cls=Player)

        if not player.channel_id or not player.context:
            player.node.players.pop(member.guild.id)
            return

        channel = self.bot.get_channel(int(player.channel_id))

        if member == player.dj and after.channel is None:
            for m in channel.members:
                if m.bot:
                    continue
                else:
                    player.dj = m
                    return

        elif after.channel == channel and player.dj not in channel.members:
            player.dj = member

    def is_privileged(self, ctx: commands.Context):
        """Check whether the user is an Admin or DJ."""
        player: Player = self.bot.wavelink.get_player(guild_id=ctx.guild.id, cls=Player, context=ctx)

        return player.dj == ctx.author or ctx.author.guild_permissions.ban_members

    @commands.command()
    async def connect(self, ctx: commands.Context, *, channel: VoiceChannel = None):
        """Connect the bot to a voice channel."""
        player: Player = self.bot.wavelink.get_player(guild_id=ctx.guild.id, cls=Player, context=ctx)
        await player.set_volume(45)

        if player.is_connected:
            return

        channel = getattr(ctx.author.voice, 'channel', channel)
        if channel is None:
            return await ctx.send(f"Sorry {ctx.author.mention} you are not connected to a voice channel!")

        await player.connect(channel.id)

    @commands.command()
    async def play(self, ctx, *, query: str):
        """Search for a song and either play it or add it to the queue."""
        query = query.strip('<>')
        if not URL_REG.match(query):
            query = f'ytsearch:{query}'

        tracks = await self.bot.wavelink.get_tracks(query)
        channel = getattr(ctx.author.voice, 'channel', VoiceChannel)
        player: Player = self.bot.wavelink.get_player(guild_id=ctx.guild.id, cls=Player, context=ctx)
        await player.set_volume(45)

        if not ctx.author.voice:
            return await ctx.send(f"Sorry {ctx.author.mention} Please connect to the channel in order to play a song.")

        if not tracks:
            return await ctx.send(f"Sorry {ctx.author.mention} That track was not found!")

        if not player.is_connected:
            await ctx.invoke(self.connect)

        if isinstance(tracks, wavelink.TrackPlaylist):
            for track in tracks.tracks:
                track = Track(track.id, track.info, requester=ctx.author)
                await player.queue.put(track)
            embed = Embed(title="World music", description=f"Added the playlist `{tracks.data['playlistInfo']['name']}` to the queue, With `{len(tracks.tracks)}` songs added to the queue.", color=self.color).set_thumbnail(url=track.thumb)
            await ctx.send(embed=embed)
        else:
            track = Track(tracks[0].id, tracks[0].info, requester=ctx.author)
            embed = Embed(title="World music", description=f"Added {track.title} to the queue!", color=self.color).set_thumbnail(url=track.thumb)
            await ctx.send(embed=embed)
            await player.queue.put(track)

        if not player.is_playing:
            await player.invoke_next()

    @commands.command()
    async def pause(self, ctx):
        """Pause the current playing song."""
        player: Player = self.bot.wavelink.get_player(guild_id=ctx.guild.id, cls=Player, context=ctx)
        if not player.is_playing:
            return await ctx.send(f"Sorry {ctx.author.mention} There is not a song currently playing.")
        
        if not self.is_privileged:
            return await ctx.send(f"Sorry {ctx.author.mention} you are not a Admin or DJ.")
        
        await player.set_pause(True)
        await ctx.send(f"Paused the song: {player.current}")


    @commands.command(aliases=["resume"])
    async def unpause(self, ctx):
        """Resume the song that was playing."""
        player: Player = self.bot.wavelink.get_player(guild_id=ctx.guild.id, cls=Player, context=ctx)
        if not player.paused:
            return await ctx.send(f"Sorry {ctx.author.mention} The song currently playing is not paused!")
    
        if not self.is_privileged:
            return await ctx.send(f"Sorry {ctx.author.mention} you are not a Admin or DJ.")

        await player.set_pause(False)
        await ctx.send(f"Unpaused the song: {player.current}")



    @commands.command(aliases=["s"])
    async def skip(self, ctx):
        """Skip the song that is currently playing!"""
        player: Player = self.bot.wavelink.get_player(guild_id=ctx.guild.id, cls=Player, context=ctx)
        
        if not player.is_playing:
            return await ctx.send(f"Sorry {ctx.author.mention} i am not currently playing a song!")

        if not self.is_privileged:
            return await ctx.send(f"Sorry {ctx.author.mention} you are not a Admin or DJ.")
        
        await player.stop()
        await ctx.send(f"Hey {ctx.author.mention}, The song has been skipped")

    @commands.command(aliases=["vol"])
    async def volume(self, ctx, *, vol: int):
        """Change the volume of the sound coming out from World."""
        player: Player = self.bot.wavelink.get_player(guild_id=ctx.guild.id, cls=Player, context=ctx)

        if vol > 100:
            return await ctx.send(f"Sorry {ctx.author.mention} `100%` is the max volume.")

        vol = max(min(vol, 100), 0)
        player.volume = vol

        if not self.is_privileged:
            return await ctx.send(f"Sorry {ctx.author.mention} you are not a Admin or DJ.")
        
        await player.set_volume(vol)
        await ctx.send(f"Hey {ctx.author.mention} Volume has been set to `{vol}%`")

    @commands.command(aliases=['np', 'current'])
    async def nowplaying(self, ctx):
        """Show the current song playing within the voice channel."""
        player: Player = self.bot.wavelink.get_player(guild_id=ctx.guild.id, cls=Player, context=ctx)

        if not player.current:
            return await ctx.send(f"Sorry {ctx.author.mention} there is not a song currently playing!")

        embed = Embed(title="Playing", description=f"Now playing: `{player.current}` | Filter: {player.eq}", color=self.color).set_thumbnail(url=player.current.thumb)
        await ctx.send(embed=embed)


    @commands.command(aliases=['q'])
    async def queue(self, ctx):
        """Return the next upcoming 5 songs."""
        player: Player = self.bot.wavelink.get_player(guild_id=ctx.guild.id, cls=Player, context=ctx)

        if not player.current or not player.queue._queue:
            return await ctx.send("There are no songs currently in the queue.")

        upcoming = list(itertools.islice(player.queue._queue, 0, 10))

        fqueue = ''.join(f'```css\n{str(song)} | {timedelta(milliseconds=song.duration)}\n```' for song in upcoming)
        embed = Embed(title=f'Upcoming songs: {len(upcoming)}', description=fqueue, color=self.color)
        await ctx.send(embed=embed)


    @commands.command(aliases=['disconnect', 'dc', "leave"])
    async def stop(self, ctx):
        """Remove World from the voice channel."""
        player: Player = self.bot.wavelink.get_player(guild_id=ctx.guild.id, cls=Player, context=ctx)
        
        if not self.is_privileged:
            return await ctx.send(f"Sorry {ctx.author.mention} you are not a Admin or DJ.")

        player: Player = self.bot.wavelink.get_player(guild_id=ctx.guild.id, cls=Player, context=ctx)
        try:
            await player.destroy() # Send a destroy node
        except Exception:
            return await ctx.send(f"Sorry {ctx.author.mention} i am currently not in a voice channel.")

    @commands.command(aliases=['swap', "givedj", "sdj"])
    async def swapdj(self, ctx: commands.Context, *, member: Member = None):
        """Give DJ position to another person in the Voice chat."""
        player: Player = self.bot.wavelink.get_player(guild_id=ctx.guild.id, cls=Player, context=ctx)

        if not player.is_connected:
            return

        if member.bot:
            return await ctx.send(f"Sorry {ctx.author.mention} but that's a bot, Please give DJ to a human!")

        if not self.is_privileged(ctx):
            return await ctx.send(f"Sorry {ctx.author.mention} but only admins or the DJ may use this command.")

        members = self.bot.get_channel(int(player.channel_id)).members

        if member and member not in members:
            return await ctx.send(f"{member} isn't in the voice chat! They cannot be DJ.")
        if member and member == player.dj:
            return await ctx.send(f"I can't change the DJ to someone who is already the DJ...")
        if len(members) <= 2:
            return await ctx.send(f"Sorry {ctx.author.mention} There are no other members in this VC to swap DJ with.")
        if member:
            player.dj = member
            return await ctx.send(f"{member.mention} is now the DJ.")
        for m in members:
            if m == player.dj or m.bot:
                continue
            else:
                player.dj = m
                return await ctx.send(f"{member.mention} is now the DJ.")
                
    @commands.group(name="filter")
    async def filter(self, ctx):
        if not ctx.invoked_subcommand:
            return await ctx.send(f"Sorry {ctx.author.mention} please type `w/filter <FILTER>`")

    @filter.command()
    async def boost(self, ctx):
        player: Player = self.bot.wavelink.get_player(guild_id=ctx.guild.id, cls=Player, context=ctx)

        if not player.is_connected:
            return await ctx.send(f"Sorry {ctx.author.mention} I am not connected to a voice channel!.")

        if not self.is_privileged(ctx):
            return await ctx.send(f"Sorry {ctx.author.mention} you are not a Admin or DJ.")
        
        boostEQ = {'boost': wavelink.Equalizer.boost()}
        eq = boostEQ.get('boost', None)
        await player.set_eq(eq)
        return await ctx.send(f"Hey {ctx.author.mention} I have boosted your sound!")


    @filter.command(aliases=["normal", "flat"])
    async def revert(self, ctx):
        player: Player = self.bot.wavelink.get_player(guild_id=ctx.guild.id, cls=Player, context=ctx)

        if not player.is_connected:
            return await ctx.send(f"Sorry {ctx.author.mention} I am not connected to a voice channel!.")

        if not self.is_privileged(ctx):
            return await ctx.send(f"Sorry {ctx.author.mention} you are not a Admin or DJ.")
        
        flatEQ = {'flat': wavelink.Equalizer.flat()}
        eq = flatEQ.get('flat', None)
        await player.set_eq(eq)
        return await ctx.send(f"Hey {ctx.author.mention} I have reverted your equilizer to flat!")

    @filter.command()
    async def metal(self, ctx):
        player: Player = self.bot.wavelink.get_player(guild_id=ctx.guild.id, cls=Player, context=ctx)

        if not player.is_connected:
            return await ctx.send(f"Sorry {ctx.author.mention} I am not connected to a voice channel!.")

        if not self.is_privileged(ctx):
            return await ctx.send(f"Sorry {ctx.author.mention} you are not a Admin or DJ.")
        
        metalEQ = {'metal': wavelink.Equalizer.metal()}
        eq = metalEQ.get('metal', None)
        await player.set_eq(eq)
        return await ctx.send(f"Hey {ctx.author.mention} I have turned the sound into metal!")

    @filter.command()
    async def piano(self, ctx):
        player: Player = self.bot.wavelink.get_player(guild_id=ctx.guild.id, cls=Player, context=ctx)

        if not player.is_connected:
            return await ctx.send(f"Sorry {ctx.author.mention} I am not connected to a voice channel!.")

        if not self.is_privileged(ctx):
            return await ctx.send(f"Sorry {ctx.author.mention} you are not a Admin or DJ.")
        
        pianoEQ = {'piano': wavelink.Equalizer.piano()}
        eq = pianoEQ.get('piano', None)
        await player.set_eq(eq)
        return await ctx.send(f"Hey {ctx.author.mention} I have turned the sound into piano!")

    @filter.command()
    async def jazz(self, ctx):
        player: Player = self.bot.wavelink.get_player(guild_id=ctx.guild.id, cls=Player, context=ctx)

        if not player.is_connected:
            return await ctx.send(f"Sorry {ctx.author.mention} I am not connected to a voice channel!.")

        if not self.is_privileged(ctx):
            return await ctx.send(f"Sorry {ctx.author.mention} you are not a Admin or DJ.")
        
        jazzEQ = {'jazz': wavelink.Equalizer.build(levels=[(0, -0.13), (1, -0.11), (2, 0.1), (3, -0.1), (4, 0.14), (5, 0.2), (6, -0.18), (7, 0.0), (8, 0.24), (9, 0.22), (10, 0.2), (11, 0.0), (12, 0.0), (13, 0.0), (14, 0.0)], name="jazz")}
        eq = jazzEQ.get('jazz', None)
        await player.set_eq(eq)
        return await ctx.send(f"Hey {ctx.author.mention} I have jazzed up the sound")

    @filter.command()
    async def pop(self, ctx):
        player: Player = self.bot.wavelink.get_player(guild_id=ctx.guild.id, cls=Player, context=ctx)

        if not player.is_connected:
            return await ctx.send(f"Sorry {ctx.author.mention} I am not connected to a voice channel!.")

        if not self.is_privileged(ctx):
            return await ctx.send(f"Sorry {ctx.author.mention} you are not a Admin or DJ.")
        
        popEQ = {'pop': wavelink.Equalizer.build(levels=[(0, -0.02), (1, -0.01), (2, 0.08), (3, 0.1), (4, 0.15), (5, 0.1), (6, 0.03), (7, -0.02), (8, -0.035), (9, -0.05), (10, -0.05), (11, -0.05), (12, -0.05), (13, -0.05), (14, -0.05)], name="pop")}
        eq = popEQ.get('pop', None)
        await player.set_eq(eq)
        return await ctx.send(f"Hey {ctx.author.mention} I have added some pop into the sound!")

    @commands.command(aliases=["dj", "whodk", "whoisdj"])
    async def djinfo(self, ctx):
        player: Player = self.bot.wavelink.get_player(guild_id=ctx.guild.id, cls=Player, context=ctx)
        await ctx.send(f"{player.dj} is the voice channel\'s dj!")
            
def setup(bot):
    bot.add_cog(Music(bot))
    print("COG: music.py Has been loaded!")

