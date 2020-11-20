import discord
import asyncio
import urllib
import akinator
import random
import requests
import io
import datetime
import aiohttp
import googletrans
import os
import json
import PIL

from discord.ext import commands, tasks
from discord import Spotify
from discord import Embed
from discord import File

from PIL import Image, ImageDraw, ImageFont, ImageFilter

from urllib.parse import urlparse, quote
from akinator.async_aki import Akinator
from googletrans import Translator

akiObj = akinator.async_aki.Akinator()

world_pfp = ("https://cdn.discordapp.com/attachments/727241613901824563/764885646162395156/world.png")

class FunCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.gameCache = {}
        self.color = 0x2F3136

    @commands.command(help="World can make you laugh with his amazing jokes!")
    async def joke(self, ctx):
        headers = {"Accept": "application/json"}
        async with aiohttp.ClientSession() as session:
            async with session.get("https://icanhazdadjoke.com", headers=headers) as req:
                r = await req.json()
        embed = Embed(
            title="Epic joke!",
            description=r["joke"],
            color=self.color
            )
        await ctx.send(embed=embed)

    @commands.command(help="World will transform your avatar into the GTA world, and you become wasted.")
    async def wasted(self, ctx, user: discord.Member=None):
        if user == None:
            user = ctx.author
        embed = Embed(title=f"Wasted Machine", color=self.color)
        embed.set_image(url=f'https://some-random-api.ml/canvas/wasted?avatar={user.avatar_url_as(format="png")}')
        await ctx.send(embed=embed)

    @commands.command(help="Ask Alister-A a question!")
    async def askali(self, ctx, *, question):
        responses = [
            "Ali A Kills Himself",
            "Ali A Ignores And Hits A 360 Noscope",
            "Ali A Approves",
            "Ali A Dosnt Approve"
        ]
        embed = Embed(title="Ask Alister-A", description=f"{ctx.author.mention} - {random.choice(responses)}", color=self.color)
        embed.add_field(name=f"**Question**", value=f'{question}', inline=False)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/710141167722824070/717777626877395004/aaaaa.png')
        await ctx.send(embed=embed)

    @askali.error
    async def askali_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/askali <question>`")

    @commands.command(help="Generate some P*rn Hub text.")
    async def phtext(self, ctx, text1, line, text):
        if line == '&':
            embed = Embed(title='P*rn Hub Text', description=f'Requested By {ctx.author.mention}', color=self.color)
            embed.set_image(url=f'https://api.alexflipnote.dev/pornhub?text={quote(text1)}{line}text2={quote(text)}')
            await ctx.send(embed=embed)

    @phtext.error
    async def phtext_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/phtext text & text`")

    @commands.command(help="Show love between users.")
    async def ship(self, ctx, text1: discord.Member, line, text: discord.Member):
        if line == '&':
            embed = Embed(title='Cuties', description=f'Requested By {ctx.author.mention}', color=self.color)
            embed.set_image(url=f'https://api.alexflipnote.dev/ship?user={text1.avatar_url}{line}user2={text.avatar_url}')
            await ctx.send(embed=embed)

    @ship.error
    async def ship_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/ship <@user> <&> <@user>`")

    @commands.command(help="Generate supreme text.")
    async def supreme(self, ctx,*,message=None):
        if message == None:
            return await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/supreme <text>`")
        sent = message.lower()
        embed = Embed(title='Supreme', description=f'Your text was generated.', color=self.color)
        embed.set_image(url=f'https://api.alexflipnote.dev/supreme?text={urllib.parse.quote(sent)}')
        await ctx.send(embed=embed)

    @commands.command(name="f", help="Give respects.")
    async def f(self, ctx, *, text: commands.clean_content = None):
        sean = ['💔', '💝', '💚', '💙', '💜']
        reason = f"for **{text}** " if text else ""
        finchat = Embed(title = f"**{ctx.author.name}** has paid their respect {reason}{random.choice(sean)}", color=self.color)
        await ctx.send(embed=finchat)

    @commands.command(help="Shows a meme from random subreddits.")
    @commands.cooldown(rate=4, per=7, type=commands.BucketType.member)
    async def meme(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://memes.blademaker.tv/api?lang=en") as r:
                res = await r.json()
                title = res["title"]
                ups = res["ups"]
                subr = res["subreddit"]

                embed = Embed(title=f"Title: {title}\nSubreddit: r/{subr}", color=self.color)
                embed.set_image(url=res["image"])
                embed.set_footer(text=f"👍Ups:{ups}")
                await ctx.send(embed=embed)

    @meme.error
    async def meme_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            a = error.retry_after
            a = round(a)
            await ctx.send(f"Sorry {ctx.author.mention} This command in on cooldown, Try again in {a} seconds.")

    @commands.command(help="Enlarge a discord emoji!")
    async def enlarge(self, ctx, emoji: discord.PartialEmoji):
        if emoji.animated:
            embed = Embed(title="Enlarge", description=f"`{emoji.name}` was enlarged.", color=self.color)
            embed.set_image(url=emoji.url)
            await ctx.send(embed=embed)
        if not emoji.animated:
            embed = Embed(title="Enlarge", description=f"`{emoji.name}` was enlarged.", color=self.color)
            embed.set_image(url=emoji.url)
            await ctx.send(embed=embed)

    @enlarge.error
    async def enlarge_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/enlarge <emoji>`")
        if isinstance(error, commands.PartialEmojiConversionFailure):
            await ctx.send(f"Sorry {ctx.author.mention} that emoji was not found!")

    @commands.command(aliases=["pepe"], help="Shows users pp size.")
    async def pp(self, ctx, *, user: discord.Member = None):
        if user is None:
            user = ctx.author
        size = random.randint(1, 15)
        dong = ""
        for _i in range(0, size):
            dong += "="
        embed = Embed(title=f"{user}'s pepe size", description=f"8{dong}D", color=self.color)
        await ctx.send(embed=embed)

    @commands.command(help="Steal a users avatar.")
    async def avatar(self, ctx, *, user: discord.Member=None):
        format = "gif"
        user = user or ctx.author
        if user.is_avatar_animated() != True:
            format = "png"
        avatar = user.avatar_url_as(format = format if format != "gif" else None)
        async with aiohttp.ClientSession() as session:
            async with session.get(str(avatar)) as resp:
                image = await resp.read()
        with io.BytesIO(image) as file:
            await ctx.send(file=discord.File(file, f"Avatar.{format}"))

    @commands.command(help="Fake tweet text.")
    @commands.guild_only()
    async def tweet(self, ctx, username: str, *, message: str):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(
                f"https://nekobot.xyz/api/imagegen?type=tweet&username={username}&text={message}"
            ) as r:
                res = await r.json()
                embed = Embed(color=self.color)
                embed.set_image(url=res["message"])
                await ctx.send(embed=embed)

    @tweet.error
    async def tweet_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/tweet <username> <message>`")

    @commands.command(help="Is that user gay?.")
    async def gay(self, ctx, *, user: discord.Member=None):
        user = user or (ctx.author)
        randomPercentage = random.randint(1, 100)
        embed = Embed(title="Gayrate!", color=self.color)
        embed.description = (f"**{user}** is {randomPercentage}% gay")
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)

    @gay.error
    async def gay_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(f':regional_indicator_x: Sorry {ctx.author.mention} Please Mention A User')

    @commands.command(aliases=["aki"], help="Can the akinator beat you?")
    async def akinator(self, ctx: commands.Context):
        if ctx.channel.id in self.gameCache.keys():
            return await ctx.send(
                "Sorry, {0[user]} is already playing akinator in <#{0[channel]}>, try again when they finish or move to another channel!"
                .format(self.gameCache[ctx.channel.id]))

        gameObj = await akiObj.start_game(child_mode=True)

        currentChannel = ctx.channel

        self.gameCache.update(
            {ctx.channel.id: {
                "user": ctx.author,
                "channel": ctx.channel.id
            }})

        while akiObj.progression <= 80:
            try:
                message1 = await ctx.send(
                    embed=Embed(title="Question", description=gameObj, color=self.color))
                resp = await ctx.bot.wait_for(
                    "message",
                    check=lambda message: message.author == ctx.author and
                    message.channel == ctx.channel and message.guild == ctx.
                    guild and message.content.lower(), timeout=15)
            except asyncio.TimeoutError:
                await ctx.send(embed=Embed(
                    title="Hurry next time!",
                    description=
                    f"{ctx.author.mention} took too long to respond so we ended the game\nCurrent timeout: `15` Seconds.", color=self.color))
                del self.gameCache[ctx.channel.id]
                return await message1.delete(delay=None)
            if resp.content == "b":
                try:
                    gameObj = await akiObj.back()
                except akinator.CantGoBackAnyFurther:
                    await ctx.send(embed=Embed(
                        title="Cannot go back any further :(",
                        description="Continue playing anyway", color=self.color))
            elif resp.content == "q" or resp.content == "quit":
                await ctx.send(embed=Embed(
                    title="Game over",
                    description=
                    "You have left the game.",
                    color=self.color
                    ))
                del self.gameCache[ctx.channel.id]
                break
            else:
                try:
                    gameObj = await akiObj.answer(resp.content)
                except:
                    del self.gameCache[ctx.channel.id]
                    return await ctx.send(embed=Embed(
                        title="Invalid Answer",
                        description=
                        "You typed a invalid answer the only answer options are:\n`y` OR `yes` for yes\n`n` OR `no` for no\n`i` OR `idk` for i dont know\n`p` OR `probably` for probably\n`pn` OR `probably not` for probably not\n`b` for back\n`q` or `quit` for stop the game",
                        color=self.color
                    ))

        await akiObj.win()

        embed = Embed(
            title="I have outsmarted your outsmarting",
            color=self.color
        ).add_field(
            name="I think...",
            value="it is {0.first_guess[name]} {0.first_guess[description]}?\n\nSorry if im wrong, Akinator has tried.".
            format(akiObj)).set_image(
                    url=akiObj.first_guess['absolute_picture_path']
                ).set_footer(text="Thanks to nomadiccode for helping!")

        del self.gameCache[ctx.channel.id]
        await ctx.send(embed=embed)


    @commands.command(aliases=["8ball"], help="The magical World 8ball.")
    async def _8ball(self, ctx, *, question):
        responses = [
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes - definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "Sean Says Yes.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Ask again later.",
            "Better not tell you now.",
            "Cannot predict now.",
            "Concentrate and ask again.",
            "Dont count on it.",
            "My reply is no.",
            "My sources say no.",
            "Outlook not so good.",
            "Sean Thinks Its Very doubtful.",
        ]
        embed = Embed(title=":8ball: The Almighty 8ball :8ball:", description=f"Question = `{question}`\n **Answer**: :8ball: {random.choice(responses)} :8ball:", color=self.color)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/717038947846455406/717784205249085470/aaaaaaaaaaaaaaaaaaa.png')
        await ctx.send(embed=embed)

    @_8ball.error
    async def _8ball_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/8ball <question>`")

    @commands.command(help="Turn text into emojis!.")
    async def emojify(self, ctx, *, stuff):
        if len(stuff) > 20:
            return await ctx.send(f"Sorry {ctx.author.mention} a limit of 20 chars please!")
        emj = ("".join([":regional_indicator_"+l+":"  if l in "abcdefghijklmnopqrstuvwyx" else [":zero:", ":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:", ":nine:"][int(l)] if l.isdigit() else ":question:" if l == "?" else ":exclamation:" if l == "!" else l for l in f"{stuff}"]))
        embed = Embed(title='Emojify', description=f'{emj}', color=self.color)
        await ctx.send(embed=embed)

    @emojify.error
    async def emojify_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/emojify <text>`")

    @commands.command(aliases=["russianrulette"], help="Play a game of Russian rulette.")
    async def rr(self, ctx):
        responses = [
            "🔫Pow Your Dead!, Try again?",
            "🎉You lived!!!",
            "🔫SPLAT!, You died. Try again?",
            "🎉You were lucky enough to survive!!",
        ]
        embed = Embed(title=":gun: Russian roulette :gun:", description=f"{random.choice(responses)}", color=self.color)
        await ctx.send(embed=embed)

    @commands.command(help="Kill a user")
    async def kill(self, ctx, user: discord.Member):
        user = user or (ctx.author)
        kills = [
        "they stole money from your bank",
        "they ate your cookies",
        "they tried to steal your phone",
        "they smelled like poop",
        "they didn't like you",
        "they lied to you",
        "they didnt trust you"
        ]
        embed = Embed(
            title="Murder",
            description=f"{ctx.author.mention} you killed {user.mention} because {random.choice(kills)}",
            color=self.color
            )
        await ctx.send(embed=embed)

    @commands.command()
    async def translate(self, ctx, *, translation):
        translator = Translator()
        result = translator.translate(translation)
        embed = Embed(title=f"Translator", description=f"`{result.origin}`", color=self.color)
        embed.add_field(name=f"Translation", value=f"`{result.text}`", inline=False)
        await ctx.send(embed=embed)

    @commands.command(help="Urban Dictionary")
    @commands.is_nsfw()
    async def urban(self, ctx, *name):
        if ctx.channel.is_nsfw():
            async with aiohttp.ClientSession() as cs:
                async with cs.get(f"http://api.urbandictionary.com/v0/define?term={'%20'.join(name)}") as r:
                    if r.status != 200:
                        return await ctx.send(f"Sorry {ctx.author.mention} Api has broken.")
                    json = await r.json()
                    list1 = json['list']
                    if len(list1) < 1:
                        return await ctx.send(f"Sorry {ctx.author.mention} This word was not found in Urban.")
                    res = list1[0]
                    embed = Embed(title=res['word'], color=self.color)
                    embed.description = res['definition']
                    embed.add_field(name="Example", value=res['example'])
                    embed.set_footer(text=f"👍 {res['thumbs_up']} | 👎{res['thumbs_down']}")
                    await ctx.send(embed=embed)

    @urban.error
    async def urban_error(self, ctx, error):
        if isinstance(error, commands.errors.NSFWChannelRequired):
            embed = Embed(title="NSFW", description=f"Sorry {ctx.author.mention} but this command is nsfw and this is not a nsfw channel.", color=self.color)
            embed.set_image(url="https://media.discordapp.net/attachments/265156286406983680/728328135942340699/nsfw.gif")
            return await ctx.send(embed=embed)


    @commands.command(name="activity")
    async def _activity(self, ctx: commands.Context, *, user: discord.Member = None):
        user = user or ctx.author
        if user.bot == True:
            embed = Embed(
                title="Activity",
                color=self.color,
                description=f"Sorry {ctx.author.mention} that's a bot, please mention a user!"
                )
            return await ctx.send(embed=embed)
        if user.activity == None:
            embed = Embed(
                title="Activity",
                color=self.color,
                description=f"Sorry {ctx.author.mention} that user does not have a status!"
                )
            return await ctx.send(embed=embed)
        for activity in user.activities:
            if activity.type is discord.ActivityType.playing:
                embed = Embed(
                   title=f"Activity",
                    color=self.color
                    ).add_field(
                    name=f"Playing {user.activity.name}",
                    value=f"{user.activity.state}"
                    ).set_thumbnail(
                    url=f"{user.activity.large_image_url}"
                    )
                await ctx.send(embed=embed)
            elif isinstance(activity, Spotify):
                embed = Embed(
                    title=f"Activity",
                    description=f"Listening to {user.activity.name}\n[`{user.activity.artist} - {user.activity.title}`](https://open.spotify.com/track/{user.activity.track_id})",
                    color=self.color
                    ).set_thumbnail(
                    url=activity.album_cover_url
                    )
                await ctx.send(embed=embed)
            elif activity.type is discord.ActivityType.streaming:
                embed = Embed(
                    title=f"Activity",
                    color=self.color,
                    description=f"Streaming {user.activity.name}\n[`Watch`]({user.activity.url})"
                    )
                await ctx.send(embed=embed)
            elif isinstance(activity, discord.CustomActivity):
                embed = Embed(
                    title="Activity",
                    color=self.color,
                    description=f"{user.activity.emoji} {user.activity.name}"
                    )
                await ctx.send(embed=embed)

    @_activity.error
    async def _activity_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send(f'Sorry {ctx.author.mention} i could not find that user.')

    @commands.command(help="Advice from world.")
    async def advice(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://api.adviceslip.com/advice", headers={"Accept": "application/json"}) as r:
                res = await r.json(content_type="text/html")
                embed = Embed(
                    title="Advice",
                    description=f"{res['slip']['advice']}",
                    color=self.color
                    )
                await ctx.send(embed=embed)

    @commands.command(help="Generate qr code")
    async def qr(self, ctx, *, text):
        embed = Embed(
            title="Qr code",
            description=f"Generated `{text}`",
            color=self.color
            ).set_image(
            url=f"http://api.qrserver.com/v1/create-qr-code/?data={quote(text)}&margin=25"
            )
        await ctx.send(embed=embed)

    @commands.command(help="This command will show you a cute duck", aliases=['quack', 'duk'])
    async def duck(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://random-d.uk/api/v2/random') as r:
                res = await r.json()
                duckimg = res['url']
        embed = Embed(
            title='Quack!',
             color=self.color
             ).set_image(
             url=duckimg
             )
        await ctx.send(embed=embed)

    @commands.command(help="Flip a users avatar!", aliases=["flipav", "avflip"])
    async def flip(self, ctx, user: discord.Member=None):
        user = user or ctx.author

        pfp = user.avatar_url_as(format='png')

        buffer_avatar = io.BytesIO()
        await pfp.save(buffer_avatar)
        buffer_avatar.seek(0)

        av_img = Image.open(buffer_avatar)

        done = av_img.rotate(180)

        buffer = io.BytesIO()

        done.save(buffer, format='PNG')

        buffer.seek(0)

        file = discord.File(buffer, "flippedimg.png")
        embed = discord.Embed(title="Flip!", description=f"{user}'s avatar flipped", color=0x2F3136)
        embed.set_image(url="attachment://flippedimg.png")
        await ctx.send(embed=embed, file=file)


    @commands.command(help="Blur a users avatar!")
    async def blur(self, ctx, user: discord.Member=None):
        user = user or ctx.author
        pfp = user.avatar_url_as(format='png')
        buffer_avatar = io.BytesIO()

        await pfp.save(buffer_avatar)

        buffer_avatar.seek(0)

        av_img = Image.open(buffer_avatar)
        done = av_img.filter(PIL.ImageFilter.GaussianBlur(radius=8))

        buffer = io.BytesIO()
        done.save(buffer, format='PNG')
        buffer.seek(0)

        file = discord.File(buffer, "blurimg.png")
        embed = discord.Embed(title="blur!", description=f"{user}'s avatar blurred", color=0x2F3136)
        embed.set_image(url="attachment://blurimg.png")
        await ctx.send(embed=embed, file=file)

def setup(bot):
    bot.add_cog(FunCog(bot))
