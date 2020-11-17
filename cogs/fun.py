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
from discord.ext import commands, tasks
from urllib.parse import urlparse, quote
from akinator.async_aki import Akinator
from discord import Spotify
from googletrans import Translator

akiObj = akinator.async_aki.Akinator()

world_pfp = ("https://cdn.discordapp.com/attachments/727241613901824563/764885646162395156/world.png")

class FunCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.gameCache = {}

    @commands.command(help="World is funny.")
    async def joke(self, ctx):
        headers = {"Accept": "application/json"}
        async with aiohttp.ClientSession() as session:
            async with session.get("https://icanhazdadjoke.com", headers=headers) as req:
                r = await req.json()
        await ctx.send(r["joke"])

    @commands.command(help="Make a user wasted.")
    async def wasted(self, ctx, user : discord.Member=None):
        if user == None:
            user = ctx.author
        embed=discord.Embed(title=f"Wasted Machine", color=0x2F3136)
        embed.set_image(url=f'https://some-random-api.ml/canvas/wasted?avatar={user.avatar_url_as(format="png")}')
        embed.set_footer(text=f"Requested by {ctx.author}")
        await ctx.send(embed=embed)

    @commands.command()
    async def askali(self, ctx, *, desc):
        responses = [
            "Ali A Kills Himself",
            "Ali A Ignores And Hits A 360 Noscope",
            "Ali A Approves",
            "Ali A Dosnt Approve"
        ]
        em = discord.Embed(title="Ask Alister-A ")
        em.description = (f"{ctx.author.mention} - {random.choice(responses)}")
        em.add_field(name=f"**Question**", value=f'{desc}', inline=False)
        em.set_thumbnail(url='https://cdn.discordapp.com/attachments/710141167722824070/717777626877395004/aaaaa.png')
        em.colour = (0x2F3136)
        await ctx.send(embed=em)

    @askali.error
    async def askali_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/askali <question>`")

    @commands.command(help="Generate some P*rn Hub text.")
    async def phtext(self,ctx,text1,line,text):
        if line == '&':
            embed = discord.Embed(title='P*rn Hub Text', description=f'Requested By {ctx.author.mention}', color=0xffa31a)
            embed.set_image(url=f'https://api.alexflipnote.dev/pornhub?text={quote(text1)}{line}text2={quote(text)}')
            await ctx.send(embed=embed)

    @commands.command(help="Make a user the impostor")
    async def impostor(self, ctx, user: discord.Member=None):
        user = user.name or ctx.author.name
        IMAGE_WIDTH = 600
        IMAGE_HEIGHT = 300

        response = urllib.request.urlopen("https://im-a-dev.xyz/vHkANH4W.png")
        image = Image.open(response)
        draw = ImageDraw.Draw(image)
        draw.rectangle([50, 50, IMAGE_WIDTH-50, IMAGE_HEIGHT-50], fill=(0,0,0), outline=(0,0,0))
        text = f'{user} was the impostor'
        font = ImageFont.truetype('Arial', 30)

        text_width, text_height = draw.textsize(text, font=font)
        x = (IMAGE_WIDTH - text_width)//2
        y = (IMAGE_HEIGHT - text_height)//2

        draw.text( (x, y), text, fill=(0,0,255), font=font)
        buffer = io.BytesIO()

        image.save(buffer, format='PNG')    
        buffer.seek(0) 
        await ctx.send(file=File(buffer, 'impostor.png'))

    @phtext.error
    async def phtext_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/phtext text & text`")

    @commands.command(help="Show love between users.")
    async def ship(self, ctx, text1: discord.Member, line, text: discord.Member):
        if line == '&':
            embed = discord.Embed(title='Cuties', description=f'Requested By {ctx.author.mention}', color=0x2F3136)
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
        embed = discord.Embed(title='Supreme', description=f'Requested By {ctx.author.mention}')
        embed.set_image(url=f'https://api.alexflipnote.dev/supreme?text={urllib.parse.quote(sent)}')
        embed.add_field(name='**Supreme Machine!**', value='Supreme Text Was Generated')
        embed.color=0x2F3136
        await ctx.send(embed=embed)

    @commands.command(name="f", help="Sad times.")
    async def f(self, ctx, *, text: commands.clean_content = None):
        """ Press F to pay respect """
        sean = ['💔', '💝', '💚', '💙', '💜']
        reason = f"for **{text}** " if text else ""
        finchat = discord.Embed(title = f"**{ctx.author.name}** has paid their respect {reason}{random.choice(sean)}", color =0x2F3136)
        await ctx.send(embed=finchat)

    @commands.command(help="Shows a meme from random subreddits.")
    @commands.cooldown(rate=4, per=7, type=commands.BucketType.member)
    async def meme(self, ctx):
        r = requests.get("https://memes.blademaker.tv/api?lang=en")
        res = r.json()
        title = res["title"]
        ups = res["ups"]
        downs = res["downs"]
        subr = res["subreddit"]
        em = discord.Embed()
        em.title = f"Title: {title}\nSubreddit: r/{subr}"
        em.set_image(url=res["image"])
        em.color = 0x2F3136
        em.set_footer(text=f"👍Ups:{ups} 👎Downs:{downs}")
        await ctx.send(embed=em)

    @commands.command(help="Enlarge a discord emoji!")
    async def enlarge(self, ctx, emoji: discord.PartialEmoji):
        if emoji.animated:
            embed = discord.Embed(title="Enlarge", description=f"`{emoji.name}` was enlarged.", color=0x2F3136)
            embed.set_image(url=emoji.url)
            await ctx.send(embed=embed)
        if not emoji.animated:
            embed = discord.Embed(title="Enlarge", description=f"`{emoji.name}` was enlarged.", color=0x2F3136)
            embed.set_image(url=emoji.url)
            await ctx.send(embed=embed)

    @enlarge.error
    async def enlarge_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/enlarge <emoji>`")
        if isinstance(error, commands.PartialEmojiConversionFailure):
            await ctx.send(f"Sorry {ctx.author.mention} that emoji was not found!")

    @meme.error
    async def meme_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            a = error.retry_after
            a = round(a)
            await ctx.send(f"Sorry {ctx.author.mention} This command in on cooldown, Try again in {a} seconds.")

    @commands.command(aliases=["pepe"], help="Shows users pp size.")
    async def pp(self, ctx, *, user: discord.Member = None):
        if user is None:
            user = ctx.author
        size = random.randint(1, 15)
        dong = ""
        for _i in range(0, size):
            dong += "="
        em = discord.Embed(
            title=f"{user}'s pepe size", description=f"8{dong}D", colour=0x2F3136
        )
        await ctx.send(embed=em)

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
            await ctx.send(file = discord.File(file, f"Avatar.{format}"))

    @commands.command(help="Fake tweet text.")
    @commands.guild_only()
    async def tweet(self, ctx, username: str, *, message: str):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(
                f"https://nekobot.xyz/api/imagegen?type=tweet&username={username}&text={message}"
            ) as r:
                res = await r.json()
                em = discord.Embed()
                em.color = 0x2F3136
                em.set_image(url=res["message"])
                await ctx.send(embed=em)

    @tweet.error
    async def tweet_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/tweet <username> <message>`")

    @commands.command(help="Is that user gay?.")
    async def gay(self, ctx, *, user: discord.Member=None):
        user = user or (ctx.author)
        randomPercentage = random.randint(1, 100)
        em = discord.Embed(title=":rainbow_flag:Gay Machine | No Mistakes Were Made:rainbow_flag:")
        em.description = (f"**{user}** You Are 0% Gay")
        em.add_field(name=f"**Gay Machine**", value=f'Requested By {ctx.author.mention}', inline=False)
        em.set_thumbnail(url=user.avatar_url)
        em.colour = (0x2F3136)
        em1 = discord.Embed(title=":rainbow_flag:Gay Machine | No Mistakes Were Made:rainbow_flag:")
        em1.description = (f"**{user}** is {randomPercentage}% gay")
        em1.add_field(name=f"**Gay Machine**", value=f'Requested By {ctx.author.mention}', inline=False)
        em1.set_thumbnail(url=user.avatar_url)
        em1.colour = (0x2F3136)
        if user.id == 662334026098409480:
            await ctx.send(embed=em)
        else:
            await ctx.send(embed=em1)

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
                    embed=discord.Embed(title="Question", description=gameObj))
                resp = await ctx.bot.wait_for(
                    "message",
                    check=lambda message: message.author == ctx.author and
                    message.channel == ctx.channel and message.guild == ctx.
                    guild and message.content.lower(), timeout=15)
            except asyncio.TimeoutError:
                await ctx.send(embed=discord.Embed(
                    title="Hurry next time!",
                    description=
                    f"{ctx.author.mention} took too long to respond so we ended the game\nCurrent timeout: `15` Seconds.", color=0x2F3136))
                del self.gameCache[ctx.channel.id]
                return await message1.delete(delay=None)
            if resp.content == "b":
                try:
                    gameObj = await akiObj.back()
                except akinator.CantGoBackAnyFurther:
                    await ctx.send(embed=discord.Embed(
                        title="Cannot go back any further :(",
                        description="Continue playing anyway", color=0x2F3136))
            elif resp.content == "q" or resp.content == "quit":
                await ctx.send(embed=discord.Embed(
                    title="Game over",
                    description=
                    "You have left the game.",
                    color=0x2F3136
                    ))
                del self.gameCache[ctx.channel.id]
                break
            else:
                try:
                    gameObj = await akiObj.answer(resp.content)
                except:
                    del self.gameCache[ctx.channel.id]
                    return await ctx.send(embed=discord.Embed(
                        title="Invalid Answer",
                        description=
                        "You typed a invalid answer the only answer options are:\n`y` OR `yes` for yes\n`n` OR `no` for no\n`i` OR `idk` for i dont know\n`p` OR `probably` for probably\n`pn` OR `probably not` for probably not\n`b` for back\n`q` or `quit` for stop the game",
                        color=0x2F3136
                    ))

        await akiObj.win()

        embed = discord.Embed(
            title="I have outsmarted your outsmarting",
            color=0x2F3136
        ).add_field(
            name="I think...",
            value="it is {0.first_guess[name]} {0.first_guess[description]}?\n\nSorry if im wrong, Akinator has tried.".
            format(akiObj)).set_image(
                    url=akiObj.first_guess['absolute_picture_path']
                ).set_footer(text="Thanks to nomadiccode for helping!")

        del self.gameCache[ctx.channel.id]
        await ctx.send(embed=embed)


    @commands.command(aliases=["8ball"], help="Magical answers.")
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
        em = discord.Embed(title=":8ball: The Almighty 8ball :8ball:")
        em.description = (f"Question = `{question}`\n **Answer**: :8ball: {random.choice(responses)} :8ball:")
        em.add_field(name=f"**8ball - World**", value=f'Requested By {ctx.author.mention}', inline=False)
        em.set_thumbnail(url='https://cdn.discordapp.com/attachments/717038947846455406/717784205249085470/aaaaaaaaaaaaaaaaaaa.png')
        em.colour = (0x000000)
        await ctx.send(embed=em)

    @_8ball.error
    async def _8ball_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/8ball <question>`")

    @commands.command(help="Turn text into emojis!.")
    async def emojify(self, ctx, *, stuff):
        if len(stuff) > 20:
            return await ctx.send(f"Sorry {ctx.author.mention} a limit of 20 chars please!")
        emj = ("".join([":regional_indicator_"+l+":"  if l in "abcdefghijklmnopqrstuvwyx" else [":zero:", ":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:", ":nine:"][int(l)] if l.isdigit() else ":question:" if l == "?" else ":exclamation:" if l == "!" else l for l in f"{stuff}"]))
        embed = discord.Embed(title='Emojify', description=f'Requested By {ctx.author.mention}', color=0x2F3136)
        embed.add_field(name='Your Message Was Emojifyed', value=f'{emj}')
        await ctx.send(embed=embed)

    @emojify.error
    async def emojify_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/emojify <text>`")

    @commands.command(help="Ask the boss.")
    async def asktrump(self, ctx, *, question):
        r = requests.get(f"https://api.whatdoestrumpthink.com/api/v1/quotes/personalized?q={question}")
        r = r.json()
        em = discord.Embed(color=0x2F3136, title="Ask Mr Presendent?")
        em.description = f"**Question:** {question}\n\n**Trump:** {r['message']}"
        em.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        em.set_footer(text="World - Ask Trump")
        await ctx.send(embed=em)

    @asktrump.error
    async def asktrump_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/asktrump <question>`")

    @commands.command(help="Sends a random gif.")
    async def gif(self, ctx):
        try:
            em = discord.Embed(color=0x2F3136, title="Random GIF")
            r = requests.get(f'https://api.giphy.com/v1/gifs/trending?api_key=5LLc05m7k8Ws5wj8F2Xsbe2HHXeFMfCQ')
            r = r.json()
            em.set_image(url=f"https://media.giphy.com/media/{r['data'][random.randint(0, len(r['data']) - 1)]['id']}/giphy.gif")
            em.set_author(name=f"Requested by: {ctx.author.name}", icon_url=ctx.author.avatar_url)
            em.set_footer(text='World - Random Gif')
            await ctx.send(embed=em)
        except Exception as e:
            em = discord.Embed(color=discord.Color(value=0x2F3136), title="An error occurred.")
            em.description = f"ERROR: \n\n```{e}```"
            await ctx.send(embed=em)


    @commands.command(aliases=["russianrulette"], help="Play Russian rulette.")
    async def rr(self, ctx):
        responses = [
            "🔫Pow Your Dead!, Try again?",
            "🎉You lived!!!",
            "🔫SPLAT!, You died. Try again?",
            "🎉You were lucky enough to survive!!",
        ]
        em = discord.Embed(title=":gun: Russian roulette :gun:")
        em.description = (f"\n{random.choice(responses)}")
        em.add_field(name=f"**Have Another Go!!**", value=f'Requested By {ctx.author.mention}', inline=False)
        em.colour = (0x2F3136)
        await ctx.send(embed=em)

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
        embed = discord.Embed(
            title="Murder",
            description=f"{ctx.author.mention} you killed {user.mention} because {random.choice(kills)}",
            color=0x2F3136
            )
        await ctx.send(embed=embed)

    @commands.command()
    async def translate(self, ctx, *, translation):
        try:
            translator = Translator()
            result = translator.translate(translation)
            embed = discord.Embed(title=f"Translator", description=f"`{result.origin}`", color=0x2F3136)
            embed.add_field(name=f"Translation", value=f"`{result.text}`", inline=False)
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(title=f"Error: `{e}`")
            await ctx.send(embed=embed)

    @commands.command(help="Urban Dictionary")
    @commands.is_nsfw()
    async def urban(self, ctx, *name):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"http://api.urbandictionary.com/v0/define?term={'%20'.join(name)}") as r:
                if r.status != 200:
                    return await ctx.send(f"Sorry {ctx.author.mention} Api has broken.")
                json = await r.json()
                list1 = json['list']
                if len(list1) < 1:
                    return await ctx.send(f"Sorry {ctx.author.mention} This word was not found in Urban.")
                res = list1[0]
                embed = discord.Embed(title=res['word'], color=0x2F3136)
                embed.description = res['definition']
                embed.add_field(name="Example", value=res['example'])
                embed.set_footer(text=f"👍 {res['thumbs_up']} | 👎{res['thumbs_down']}")
                await ctx.send(embed=embed)


    @commands.command(name="activity")
    async def _activity(self, ctx: commands.Context, *, user: discord.Member = None):
        user = user or ctx.author
        if user.bot == True:
            embed = discord.Embed(
                title="Activity",
                color=0x2F3136,
                description=f"Sorry {ctx.author.mention} that's a bot, please mention a user!"
                )
            return await ctx.send(embed=embed)
        if user.activity == None:
            embed = discord.Embed(
                title="Activity",
                color=0x2F3136,
                description=f"Sorry {ctx.author.mention} that user does not have a status!"
                )
            return await ctx.send(embed=embed)
        for activity in user.activities:
            if activity.type is discord.ActivityType.playing:
                embed = discord.Embed(
                   title=f"Activity",
                    color=0x2F3136
                    ).add_field(
                    name=f"Playing {user.activity.name}",
                    value=f"{user.activity.state}"
                    ).set_thumbnail(
                    url=f"{user.activity.large_image_url}"
                    )
                await ctx.send(embed=embed)
            elif isinstance(activity, Spotify):
                embed = discord.Embed(
                    title=f"Activity",
                    description=f"Listening to {user.activity.name}\n[`{user.activity.artist} - {user.activity.title}`](https://open.spotify.com/track/{user.activity.track_id})",
                    color=0x2F3136
                    ).set_thumbnail(
                    url=activity.album_cover_url
                    )
                await ctx.send(embed=embed)
            elif activity.type is discord.ActivityType.streaming:
                embed = discord.Embed(
                    title=f"Activity",
                    color=0x2F3136,
                    description=f"Streaming {user.activity.name}\n[`Watch`]({user.activity.url})"
                    )
                await ctx.send(embed=embed)
            elif isinstance(activity, discord.CustomActivity):
                embed = discord.Embed(
                    title="Activity",
                    color=0x2F3136,
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
                embed = discord.Embed(
                    title="Advice",
                    color=0x2F3136
                    ).add_field(
                    name="Advice from World",
                    value=f"{res['slip']['advice']}"
                    )
                await ctx.send(embed=embed)

    @commands.command(help="Generate qr code")
    async def qr(self, ctx, *, text):
        embed = discord.Embed(
            title="Qr code",
            description=f"Generated `{text}`",
            color=0x2F3136
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
        embed = discord.Embed(
        	title='Quack!',
        	 color=0x2F3136
        	 ).set_image(
        	 url=duckimg
        	 )
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(FunCog(bot))
