import wavelink
import asyncio
import re
import itertools
from discord.ext import commands
from typing import Union
from discord import Embed, Member, VoiceChannel, VoiceState
from datetime import timedelta

RURL = re.compile("https?:\/\/(?:www\.)?.+")


class MusicController:
    def __init__(self, bot, guild_id):
        self.bot = bot
        self.guild_id = guild_id
        self.color = 0x2F3136
        self.channel = None

        self.next = asyncio.Event()
        self.queue = asyncio.Queue()

        self.volume = 45
        self.now_playing = None

        self.bot.loop.create_task(self.controller_loop())

    async def controller_loop(self):
        await self.bot.wait_until_ready()

        player: Player = self.bot.wavelink.get_player(guild_id=ctx.guild.id, cls=Player)
        await player.set_volume(self.volume)

        while True:
            if self.now_playing:
                await self.now_playing.delete()

            self.next.clear()

            song = await self.queue.get()
            await player.play(song)
            embed = Embed(
                title=f"Now playing `{song}`", color=self.color
            ).set_thumbnail(url=song.thumb)
            self.now_playing = await self.channel.send(embed=embed)
            await self.next.wait()


class Player(wavelink.Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.context: commands.Context = kwargs.get("context", None)
        self.dj = None
        if self.context:
            self.dj: Member = self.context.author


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.controllers = {}
        self.color = 0x2F3136
        if not hasattr(bot, "wavelink"):
            self.bot.wavelink = wavelink.Client(bot=self.bot)
        self.bot.loop.create_task(self.start_nodes())

    async def start_nodes(self):
        await self.bot.wait_until_ready()  # Wait until bot is ready to make a connection!
        node = await self.bot.wavelink.initiate_node(
            host="127.0.0.1",
            port=2333,
            rest_uri="http://127.0.0.1:2333",
            password="youshallnotpass",
            identifier="TEST",
            region="us_central",
        )
        node.set_hook(self.on_event_hook)

    async def on_event_hook(self, event):
        if isinstance(event, (wavelink.TrackEnd, wavelink.TrackException)):
            controller = self.get_controller(event.player)
            controller.next.set()

    def get_controller(self, value: Union[commands.Context, wavelink.Player]):
        if isinstance(value, commands.Context):
            gid = value.guild.id
        else:
            gid = value.guild_id

        try:
            controller = self.controllers[gid]
        except KeyError:
            controller = MusicController(self.bot, gid)
            self.controllers[gid] = controller

        return controller

    @commands.Cog.listener()
    async def on_voice_state_update(
        self, member: Member, before: VoiceState, after: VoiceState
    ):
        if member.bot:
            return

        player: Player = self.bot.wavelink.get_player(
            guild_id=member.guild.id, cls=Player
        )

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
        """Check whether the user is an Administrator or DJ."""
        player: Player = self.bot.wavelink.get_player(
            ctx.guild.id, cls=Player, context=ctx
        )
        return player.dj == ctx.author or ctx.author.guild_permissions.ban_members

    @commands.command(name="connect")
    async def connect_(self, ctx, *, channel: VoiceChannel = None):
        """Get World to connect to the authors Voicechannel."""
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                await ctx.send(
                    f"Sorry {ctx.author.mention} no channel to join, As you are not connected to one. Please connect to a voice channel!"
                )

        player: Player = self.bot.wavelink.get_player(
            guild_id=ctx.guild.id, cls=Player, context=ctx
        )
        await player.connect(channel.id)
        await ctx.send(f"Connected to `{channel.name}`", delete_after=3)

        controller = self.get_controller(ctx)
        controller.channel = ctx.channel

    @commands.command()
    async def play(self, ctx, *, query: str):
        """Search for a song and either play it or add it to the queue."""
        if not RURL.match(query):
            query = f"ytsearch:{query}"

        tracks = await self.bot.wavelink.get_tracks(query)

        if not tracks:
            return await ctx.send(
                f"Sorry {ctx.author.mention} That track was not found!"
            )

        player: Player = self.bot.wavelink.get_player(
            guild_id=ctx.guild.id, cls=Player, context=ctx
        )
        if not player.is_connected:
            await ctx.invoke(self.connect_)

        track = tracks[0]

        controller = self.get_controller(ctx)
        await controller.queue.put(track)
        embed = Embed(
            title="World music",
            description=f"Added `{str(track)}` to the queue.",
            color=self.color,
        ).set_thumbnail(url=track.thumb)
        await ctx.send(embed=embed)

    @commands.command()
    async def pause(self, ctx):
        """Pause the current playing song."""
        player: Player = self.bot.wavelink.get_player(
            guild_id=ctx.guild.id, cls=Player, context=ctx
        )
        if not player.is_playing:
            return await ctx.send(
                f"Sorry {ctx.author.mention} There is not a song currently playing."
            )

        if self.is_privileged(ctx):
            await ctx.send(f"Paused the song: {player.current}")
            await player.set_pause(True)
        else:
            return await ctx.send(
                f"Sorry {ctx.author.mention} you are not a Admin or DJ."
            )

    @commands.command(aliases=["resume"])
    async def unpause(self, ctx):
        """Resume the song that was playing."""
        player: Player = self.bot.wavelink.get_player(
            guild_id=ctx.guild.id, cls=Player, context=ctx
        )
        if not player.paused:
            return await ctx.send(
                f"Sorry {ctx.author.mention} The song currently playing is not paused!"
            )

        if self.is_privileged(ctx):
            await ctx.send(f"Unpaused the song: {player.current}")
            await player.set_pause(False)
        else:
            return await ctx.send(
                f"Sorry {ctx.author.mention} you are not a Admin or DJ."
            )

    @commands.command()
    async def skip(self, ctx):
        """Skip the song that is currently playing!"""
        player: Player = self.bot.wavelink.get_player(
            guild_id=ctx.guild.id, cls=Player, context=ctx
        )

        if not player.is_playing:
            return await ctx.send(
                f"Sorry {ctx.author.mention} i am not currently playing a song!"
            )

        if self.is_privileged:
            await player.stop()
            await ctx.send(f"Hey {ctx.author.mention}, The song has been skipped")
        else:
            return await ctx.send(
                f"Sorry {ctx.author.mention} you are not a Admin or DJ."
            )

    @commands.command(aliases=["vol"])
    async def volume(self, ctx, *, vol: int):
        """Change the volume of the sound coming out from World."""
        player: Player = self.bot.wavelink.get_player(
            guild_id=ctx.guild.id, cls=Player, context=ctx
        )
        controller = self.get_controller(ctx)

        if vol > 100:
            return await ctx.send(
                f"Sorry {ctx.author.mention} `100%` is the max volume."
            )

        vol = max(min(vol, 100), 0)
        controller.volume = vol

        if self.is_privileged:
            await ctx.send(f"Hey {ctx.author.mention} Volume has been set to `{vol}%`")
            await player.set_volume(vol)
        else:
            return await ctx.send(
                f"Sorry {ctx.author.mention} you are not a Admin or DJ."
            )

    @commands.command(aliases=["np", "current"])
    async def nowplaying(self, ctx):
        """Show the current song playing within the voice channel."""
        player: Player = self.bot.wavelink.get_player(
            guild_id=ctx.guild.id, cls=Player, context=ctx
        )

        if not player.current:
            return await ctx.send(
                f"Sorry {ctx.author.mention} there is not a song currently playing!"
            )

        controller = self.get_controller(ctx)

        embed = Embed(
            title="Playing",
            description=f"Now playing: `{player.current}` | Filter: {player.eq}",
            color=self.color,
        ).set_thumbnail(url=player.current.thumb)
        controller.now_playing = await ctx.send(embed=embed)

    @commands.command(aliases=["q"])
    async def queue(self, ctx):
        """Return the next upcoming 5 songs."""
        player: Player = self.bot.wavelink.get_player(
            guild_id=ctx.guild.id, cls=Player, context=ctx
        )
        controller = self.get_controller(ctx)

        if not player.current or not controller.queue._queue:
            return await ctx.send("There are no songs currently in the queue.")

        upcoming = list(itertools.islice(controller.queue._queue, 0, 5))

        fqueue = "".join(
            f"```{str(song)} | {timedelta(milliseconds=song.duration)}\n```"
            for song in upcoming
        )
        embed = Embed(
            title=f"Upcoming songs: {len(upcoming)}",
            description=fqueue,
            color=self.color,
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=["disconnect", "dc", "leave"])
    async def stop(self, ctx):
        """Remove World from the voice channel."""
        player: Player = self.bot.wavelink.get_player(
            guild_id=ctx.guild.id, cls=Player, context=ctx
        )

        try:
            del self.controllers[ctx.guild.id]
        except KeyError:
            await player.disconnect()
            return await ctx.send(
                f"Sorry {ctx.author.mention} i am currently not in a voice channel."
            )

        if self.is_privileged:
            await player.disconnect()
            await ctx.send("I left the voice channel, Bye!")
        else:
            return await ctx.send(
                f"Sorry {ctx.author.mention} you are not a Admin or DJ."
            )

    @commands.command(aliases=["swap", "givedj", "sdj"])
    async def swapdj(self, ctx: commands.Context, *, member: Member = None):
        """Give DJ position to another person in the Voice chat."""
        player: Player = self.bot.wavelink.get_player(
            guild_id=ctx.guild.id, cls=Player, context=ctx
        )

        if not player.is_connected:
            return

        if not self.is_privileged(ctx):
            return await ctx.send(
                f"Sorry {ctx.author.mention} but only admins or the DJ may use this command."
            )

        members = self.bot.get_channel(int(player.channel_id)).members

        if member and member not in members:
            return await ctx.send(
                f"{member} isn't in the voice chat! They cannot be DJ."
            )
        if member and member == player.dj:
            return await ctx.send(
                f"I can't change the DJ to someone who is already the DJ..."
            )
        if len(members) <= 2:
            return await ctx.send(
                f"Sorry {ctx.author.mention} There are no other members in this VC to swap DJ with."
            )
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
            return await ctx.send(
                f"Sorry {ctx.author.mention} please type `w/filter <FILTER>`"
            )

    @filter.command()
    async def boost(self, ctx):
        player: Player = self.bot.wavelink.get_player(
            guild_id=ctx.guild.id, cls=Player, context=ctx
        )

        if not player.is_connected:
            return

        if not self.is_privileged(ctx):
            return await ctx.send(
                f"Sorry {ctx.author.mention} you are not a Admin or DJ."
            )

        boostEQ = {"boost": wavelink.Equalizer.boost()}
        eq = boostEQ.get("boost", None)
        await player.set_eq(eq)
        return await ctx.send(f"Hey {ctx.author.mention} I have boosted your sound!")

    @filter.command(aliases=["normal", "flat"])
    async def revert(self, ctx):
        player: Player = self.bot.wavelink.get_player(
            guild_id=ctx.guild.id, cls=Player, context=ctx
        )

        if not player.is_connected:
            return

        if not self.is_privileged(ctx):
            return await ctx.send(
                f"Sorry {ctx.author.mention} you are not a Admin or DJ."
            )

        flatEQ = {"flat": wavelink.Equalizer.flat()}
        eq = flatEQ.get("flat", None)
        await player.set_eq(eq)
        return await ctx.send(
            f"Hey {ctx.author.mention} I have reverted your equilizer to flat!"
        )

    @filter.command()
    async def metal(self, ctx):
        player: Player = self.bot.wavelink.get_player(
            guild_id=ctx.guild.id, cls=Player, context=ctx
        )

        if not player.is_connected:
            return

        if not self.is_privileged(ctx):
            return await ctx.send(
                f"Sorry {ctx.author.mention} you are not a Admin or DJ."
            )

        metalEQ = {"metal": wavelink.Equalizer.metal()}
        eq = metalEQ.get("metal", None)
        await player.set_eq(eq)
        return await ctx.send(
            f"Hey {ctx.author.mention} I have turned the sound into metal!"
        )

    @filter.command()
    async def piano(self, ctx):
        player: Player = self.bot.wavelink.get_player(
            guild_id=ctx.guild.id, cls=Player, context=ctx
        )

        if not player.is_connected:
            return

        if not self.is_privileged(ctx):
            return await ctx.send(
                f"Sorry {ctx.author.mention} you are not a Admin or DJ."
            )

        pianoEQ = {"piano": wavelink.Equalizer.piano()}
        eq = pianoEQ.get("piano", None)
        await player.set_eq(eq)
        return await ctx.send(
            f"Hey {ctx.author.mention} I have turned the sound into piano!"
        )


def setup(bot):
    bot.add_cog(Music(bot))
