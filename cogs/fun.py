from random import randint, choice
from pykakasi import kakasi
from discord.ext import commands
from discord import Embed, File, PartialEmoji, Member, Spotify
from datetime import datetime
from typing import Optional
from io import BytesIO
from os import environ
from pymongo import MongoClient
from framework import Misc, Wealth
import time
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from twemoji_parser import TwemojiParser, emoji_to_url, image
from colorthief import ColorThief

from urllib.parse import quote
from akinator.async_aki import Akinator
from spotipy import Spotify as _Spotify
from spotipy.oauth2 import SpotifyClientCredentials

__import__("dotenv").load_dotenv()

class FunCog(commands.Cog):
    def __init__(self, bot): # all constants is better using self.<variable> rather than declaring it every time a command is invoked
        self.kks = kakasi()
        self.bot = bot
        self.countries = {'af': 'afghanistan', 'ax': 'aland islands', 'al': 'albania', 'dz': 'algeria', 'as': 'american samoa', 'ad': 'andorra', 'ao': 'angola', 'ai': 'anguilla', 'aq': 'antarctica', 'ag': 'antigua and barbuda', 'ar': 'argentina', 'am': 'armenia', 'aw': 'aruba', 'au': 'australia', 'at': 'austria', 'az': 'azerbaijan', 'bs': 'bahamas', 'bh': 'bahrain', 'bd': 'bangladesh', 'bb': 'barbados', 'by': 'belarus', 'be': 'belgium', 'bz': 'belize', 'bj': 'benin', 'bm': 'bermuda', 'bt': 'bhutan', 'bo': 'bolivia', 'ba': 'bosnia and herzegovina', 'bw': 'botswana', 'bv': 'bouvet island', 'br': 'brazil', 'io': 'british indian ocean territory', 'bn': 'brunei darussalam', 'bg': 'bulgaria', 'bf': 'burkina faso', 'bi': 'burundi', 'kh': 'cambodia', 'cm': 'cameroon', 'ca': 'canada', 'cv': 'cape verde', 'ky': 'cayman islands', 'cf': 'central african republic', 'td': 'chad', 'cl': 'chile', 'cn': 'china', 'cx': 'christmas island', 'cc': 'cocos (keeling) islands', 'co': 'colombia', 'km': 'comoros', 'cg': 'congo', 'cd': 'congo, the democratic republic of the', 'ck': 'cook islands', 'cr': 'costa rica', 'ci': "cote d'ivoire", 'hr': 'croatia', 'cu': 'cuba', 'cy': 'cyprus', 'cz': 'czech republic', 'dk': 'denmark', 'dj': 'djibouti', 'dm': 'dominica', 'do': 'dominican republic', 'ec': 'ecuador', 'eg': 'egypt', 'sv': 'el salvador', 'gq': 'equatorial guinea', 'er': 'eritrea', 'ee': 'estonia', 'et': 'ethiopia', 'fk': 'falkland islands (malvinas)', 'fo': 'faroe islands', 'fj': 'fiji', 'fi': 'finland', 'fr': 'france', 'gf': 'french guiana', 'pf': 'french polynesia', 'tf': 'french southern territories', 'ga': 'gabon', 'gm': 'gambia', 'ge': 'georgia', 'de': 'germany', 'gh': 'ghana', 'gi': 'gibraltar', 'gr': 'greece', 'gl': 'greenland', 'gd': 'grenada', 'gp': 'guadeloupe', 'gu': 'guam', 'gt': 'guatemala', 'gg': 'guernsey', 'gn': 'guinea', 'gw': 'guinea-bissau', 'gy': 'guyana', 'ht': 'haiti', 'hm': 'heard island and mcdonald islands', 'va': 'holy see (vatican city state)', 'hn': 'honduras', 'hk': 'hong kong', 'hu': 'hungary', 'is': 'iceland', 'in': 'india', 'id': 'indonesia', 'ir': 'iran, islamic republic of', 'iq': 'iraq', 'ie': 'ireland', 'im': 'isle of man', 'il': 'israel', 'it': 'italy', 'jm': 'jamaica', 'jp': 'japan', 'je': 'jersey', 'jo': 'jordan', 'kz': 'kazakhstan', 'ke': 'kenya', 'ki': 'kiribati', 'kp': "korea, democratic people's republic of", 'kr': 'korea, republic of', 'kw': 'kuwait', 'kg': 'kyrgyzstan', 'la': "lao people's democratic republic", 'lv': 'latvia', 'lb': 'lebanon', 'ls': 'lesotho', 'lr': 'liberia', 'ly': 'libyan arab jamahiriya', 'li': 'liechtenstein', 'lt': 'lithuania', 'lu': 'luxembourg', 'mo': 'macao', 'mk': 'macedonia, the former yugoslav republic of', 'mg': 'madagascar', 'mw': 'malawi', 'my': 'malaysia', 'mv': 'maldives', 'ml': 'mali', 'mt': 'malta', 'mh': 'marshall islands', 'mq': 'martinique', 'mr': 'mauritania', 'mu': 'mauritius', 'yt': 'mayotte', 'mx': 'mexico', 'fm': 'micronesia, federated states of', 'md': 'moldova, republic of', 'mc': 'monaco', 'mn': 'mongolia', 'ms': 'montserrat', 'ma': 'morocco', 'mz': 'mozambique', 'mm': 'myanmar', 'na': 'namibia', 'nr': 'nauru', 'np': 'nepal', 'nl': 'netherlands', 'an': 'netherlands antilles', 'nc': 'new caledonia', 'nz': 'new zealand', 'ni': 'nicaragua', 'ne': 'niger', 'ng': 'nigeria', 'nu': 'niue', 'nf': 'norfolk island', 'mp': 'northern mariana islands', 'no': 'norway', 'om': 'oman', 'pk': 'pakistan', 'pw': 'palau', 'ps': 'palestinian territory, occupied', 'pa': 'panama', 'pg': 'papua new guinea', 'py': 'paraguay', 'pe': 'peru', 'ph': 'philippines', 'pn': 'pitcairn', 'pl': 'poland', 'pt': 'portugal', 'pr': 'puerto rico', 'qa': 'qatar', 're': 'reunion', 'ro': 'romania', 'ru': 'russian federation', 'rw': 'rwanda', 'sh': 'saint helena', 'kn': 'saint kitts and nevis', 'lc': 'saint lucia', 'pm': 'saint pierre and miquelon', 'vc': 'saint vincent and the grenadines', 'ws': 'samoa', 'sm': 'san marino', 'st': 'sao tome and principe', 'sa': 'saudi arabia', 'sn': 'senegal', 'cs': 'serbia and montenegro', 'sc': 'seychelles', 'sl': 'sierra leone', 'sg': 'singapore', 'sk': 'slovakia', 'si': 'slovenia', 'sb': 'solomon islands', 'so': 'somalia', 'za': 'south africa', 'gs': 'south georgia and the south sandwich islands', 'es': 'spain', 'lk': 'sri lanka', 'sd': 'sudan', 'sr': 'suriname', 'sj': 'svalbard and jan mayen', 'sz': 'swaziland', 'se': 'sweden', 'ch': 'switzerland', 'sy': 'syrian arab republic', 'tw': 'taiwan, province of china', 'tj': 'tajikistan', 'tz': 'tanzania, united republic of', 'th': 'thailand', 'tl': 'timor-leste', 'tg': 'togo', 'tk': 'tokelau', 'to': 'tonga', 'tt': 'trinidad and tobago', 'tn': 'tunisia', 'tr': 'turkey', 'tm': 'turkmenistan', 'tc': 'turks and caicos islands', 'tv': 'tuvalu', 'ug': 'uganda', 'ua': 'ukraine', 'ae': 'united arab emirates', 'gb': 'united kingdom', 'us': 'united states', 'um': 'united states minor outlying islands', 'uy': 'uruguay', 'uz': 'uzbekistan', 'vu': 'vanuatu', 've': 'venezuela', 'vn': 'viet nam', 'vg': 'virgin islands, british', 'vi': 'virgin islands, u.s.', 'wf': 'wallis and futuna', 'eh': 'western sahara', 'ye': 'yemen', 'zm': 'zambia', 'zw': 'zimbabwe'}
        self.akiObj = Akinator()
        self.gameCache = {}
        self.sp = _Spotify(auth_manager=SpotifyClientCredentials(client_id=environ["SP_ID"], client_secret=environ["SP_SECRET"]))
        self.collection = MongoClient(environ["MONGODB_URL"])["Coins"]["Points/others"]
        self.goodmessages = ("Wow speedy!", "Nice time!", "That was pretty good!", "Wow, you fast at typing!", "You speedy, that's for sure!")
        self.badmessages = ("How slow can you type?", "That was slow!", "You need to practice more!", "It's ok i won't tell anybody that your a slow typer")
        self.aliaresponses = (
            "Kills Himself",
            "Ignores And Hits A 360 Noscope",
            "Approves",
            "Doesn't Approve"
        )
        self._8ball_responses = (
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes - definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Most likely.",
            "Outlook good.",
            "World Says Yes!",
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
            "World Thinks Its Very doubtful.",
        )
        self.hearts = ('💔', '💝', '💚', '💙', '💜')
        self.kills = (
            "stole money from your bank",
            "ate your cookies",
            "tried to steal your phone",
            "smelled like poop",
            "didn't like you",
            "lied to you",
            "didnt trust you"
        )

    @property
    def session(self):
        return self.bot.http._HTTPClient__session

    @commands.command(help="World can make you laugh with his amazing jokes!")
    async def joke(self, ctx):
        req = await self.session.get("https://icanhazdadjoke.com", headers={"Accept": "application/json"})
        r = await req.json()
        await ctx.send(embed=Embed(title="Epic joke!", description=r["joke"], color=self.bot.color))

    @commands.command(help="Ask Alister-A a question!")
    async def askali(self, ctx, *, question):
        await ctx.send(embed=Embed(title="Ask Alister-A", description=f"{ctx.author.mention} - Ali A {choice(self.aliaresponses)}", color=self.bot.color).set_thumbnail(url="https://tenor.com/view/ali-a-hue-funny-dance-gif-12395829"))


    @commands.command(help="Fetch the minecraft skin of a player.")
    async def mcskin(self, ctx, user):
        req = await self.session.get(f'https://mc-heads.net/body/{quote(user or ctx.author.display_name)[:128]}/600')
        await ctx.send(file=File(BytesIO(await req.read()), 'skin.png'), embed=Embed(title=f"{req.name}'s skin", color=self.bot.color).set_image(url='attachment://skin.png'))

    @commands.command(name="f")
    async def f(self, ctx, *, text: commands.clean_content = None):
        await ctx.send(embed=Embed(title = f"**{ctx.author.name}** has paid their respect {f'for **{text}** ' if text else ''}{choice(self.hearts)}", color=self.bot.color))

    @commands.command(help="Shows a meme from random subreddits.")
    @commands.cooldown(rate=4, per=7, type=commands.BucketType.member)
    async def meme(self, ctx):
        r = await self.session.get(f"https://memes.blademaker.tv/api?lang=en")
        res = await r.json()
        await ctx.send(embed=Embed(title=f"Title: {res['title']}\nSubreddit: r/{res['subreddit']}", color=self.bot.color).set_image(url=res["image"]).set_footer(text=f"👍Ups:{res['ups']}"))

    @commands.command(help="Enlarge a discord emoji!")
    async def enlarge(self, ctx, emoji: PartialEmoji):
        await ctx.send(embed=Embed(title="Enlarge", description=f"`{emoji.name}` was enlarged.", color=self.bot.color).set_image(url=emoji.url))

    @enlarge.error
    async def enlarge_error(self, ctx, error):
        try:
            assert isinstance(error, commands.PartialEmojiConversionFailure)
            
            message_content = ctx.message.content.split()[1].lower()
            if ("pp" in message_content) or ("tits" in message_content):
                return await ctx.send(f"{ctx.author.mention}, go to horny jail.")
            
            emoji_url = await emoji_to_url(message_content, session=self.session)
            assert emoji_url != message_content
            await ctx.send(embed=Embed(title="Enlarge", description=f"{message_content} was enlarged.", color=self.bot.color).set_image(url=emoji_url))
        except:
            await ctx.send(f"Sorry {ctx.author.mention} that emoji was not found!")

    @commands.command(aliases=["pepe"])
    async def pp(self, ctx, *, user: Member = None):
        dong = "=" * randint(1, 15)
        await ctx.send(embed=Embed(title=f"{(user or ctx.author).display_name}'s pepe size", description=f"8{dong}D", color=self.bot.color))

    @commands.command(help="Steal a users avatar.", aliases=["av"])
    async def avatar(self, ctx, *, user: Member=None):
        user = user or ctx.author
        _format = "gif" if user.is_avatar_animated() else "png"
        avatar = user.avatar_url_as(format=_format)
        resp = await self.session.get(str(avatar))
        image = await resp.read()
        await ctx.send(file=File(BytesIO(image), f"Avatar.{_format}"))

    @commands.command(help="Fake tweet text.")
    async def tweet(self, ctx, username: str, *, message: str):
        r = await self.session.get(f"https://nekobot.xyz/api/imagegen?type=tweet&username={username}&text={message[:50]}") # [:50] trims the string to the first 50 characters (if it's longer than 50 characters)
        res = await r.json()
        await ctx.send(embed=Embed(color=self.bot.color).set_image(url=res["message"]))
        await r.close(close_session=False)

    @commands.command(help="Is that user gay?.")
    async def gay(self, ctx, *, user: Member=None):
        user = user or ctx.author
        randomPercentage = randint(1, 100)
        await ctx.send(embed=Embed(title="Gayrate!", description=f"**{user.display_name}** is {randomPercentage}% gay", color=self.bot.color).set_thumbnail(url=user.avatar_url))

    @commands.command(aliases=["aki"])
    async def akinator(self, ctx: commands.Context):
        if ctx.channel.id in self.gameCache.keys():
            return await ctx.send(
                "Sorry, {0[user]} is already playing akinator in <#{0[channel]}>, try again when they finish or move to another channel!"
                .format(self.gameCache[ctx.channel.id]))

        gameObj = await self.akiObj.start_game(child_mode=True)

        self.gameCache.update(
            {ctx.channel.id: {
                "user": ctx.author,
                "channel": ctx.channel.id
            }})

        while self.akiObj.progression <= 80:
            try:
                message1 = await ctx.send(embed=Embed(title="Question", description=gameObj, color=self.bot.color))
                resp = await ctx.bot.wait_for("message", check=lambda message: message.author == ctx.author and message.channel == ctx.channel and message.guild == ctx.guild and message.content.lower(), timeout=15)
            except:
                await ctx.send(embed=Embed(title="Hurry next time!", description=f"{ctx.author.mention} took too long to respond so we ended the game\nCurrent timeout: `15` Seconds.", color=self.bot.color))
                del self.gameCache[ctx.channel.id]
                return await message1.delete(delay=None)
            if resp.content.lower() == "b":
                try:
                    gameObj = await self.akiObj.back()
                except:
                    await ctx.send(embed=Embed(title="Cannot go back any further :(", description="Continue playing anyway", color=self.bot.color))
            elif resp.content.lower() == "q" or resp.content.lower() == "quit":
                await ctx.send(embed=Embed(title="Game over", description="You have left the game.", color=self.bot.color))
                del self.gameCache[ctx.channel.id]
                break
            else:
                try:
                    gameObj = await self.akiObj.answer(resp.content)
                except:
                    del self.gameCache[ctx.channel.id]
                    return await ctx.send(embed=Embed(title="Invalid Answer", description="You typed a invalid answer the only answer options are:\n`y` OR `yes` for yes\n`n` OR `no` for no\n`i` OR `idk` for i dont know\n`p` OR `probably` for probably\n`pn` OR `probably not` for probably not\n`b` for back\n`q` or `quit` for stop the game", color=self.bot.color))

        await self.akiObj.win()
        del self.gameCache[ctx.channel.id]
        await ctx.send(embed=Embed(title="I have outsmarted your outsmarting", color=self.bot.color).add_field(name="I think...", value="it is {0.first_guess[name]} {0.first_guess[description]}?\n\nSorry if im wrong, Akinator has tried.".format(self.akiObj)).set_image(url=self.akiObj.first_guess['absolute_picture_path']))


    @commands.command(aliases=["8ball"])
    async def _8ball(self, ctx, *, question):
        await ctx.send(embed=Embed(title=":8ball: The Almighty 8ball :8ball:", description=f"Question = `{question}`\n **Answer**: :8ball: {choice(self._8ball_responses)} :8ball:", color=self.bot.color))

    @commands.command(help="Turn text into emojis!.")
    async def emojify(self, ctx, *, stuff):
        await ctx.send(("".join([":regional_indicator_"+l+":" if l in "abcdefghijklmnopqrstuvwyx" else [":zero:", ":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:", ":nine:"][int(l)] if l.isdigit() else ":question:" if l == "?" else ":exclamation:" if l == "!" else l for l in stuff[:100].lower()])))



    @commands.command(help="Kill a user")
    async def kill(self, ctx, user: Member):
        await ctx.send(embed=Embed(title="Murder", description=f"{ctx.author.mention} you killed {(user or ctx.author).mention} because they {choice(self.kills)}", color=self.bot.color))

    @commands.command(help="Urban Dictionary")
    @commands.is_nsfw()
    async def urban(self, ctx, *name):
        if ctx.channel.is_nsfw():
            r = await self.session.get(f"http://api.urbandictionary.com/v0/define?term={'%20'.join(name)}")
            if r.status != 200:
                return await ctx.send(f"Sorry {ctx.author.mention} Api has broken.")

            json = await r.json()
            list1 = json['list']
            if not list1:
                return await ctx.send(f"Sorry {ctx.author.mention} This word was not found in Urban.")
            res = list1[0]
            await ctx.send(embed=Embed(title=res['word'], description=res['definition'], color=self.bot.color).add_field(name="Example", value=res['example']).set_footer(text=f"👍 {res['thumbs_up']} | 👎{res['thumbs_down']}"))

    @commands.command(help="Advice from world.")
    async def advice(self, ctx):
        r = await self.session.get(f"https://api.adviceslip.com/advice", headers={"Accept": "application/json"})
        res = await r.json(content_type="text/html")
        await ctx.send(embed=Embed(title="Advice", description=f"{res['slip']['advice']}", color=self.bot.color))

    @commands.command(help="Generate qr code")
    async def qr(self, ctx, *, text):
        await ctx.send(embed=Embed(title="Qr code", description=f"Generated `{text}`", color=self.bot.color).set_image(url=f"http://api.qrserver.com/v1/create-qr-code/?data={quote(text)}&margin=25"))


    @commands.command(help="This command will show you a cute duck", aliases=['quack', 'duk'])
    async def duck(self, ctx):
        r = await self.session.get('https://random-d.uk/api/v2/random')
        res = await r.json()
        await ctx.send(embed=Embed(title='Quack!', color=self.bot.color).set_image(url=res['url']))

    @commands.command(help="Flip a users avatar!", aliases=["flipav", "avflip"])
    async def flip(self, ctx, user: Member=None):
        av_img = await Misc.fetch_pfp(user or ctx.author)
        done = av_img.rotate(180)
        await ctx.send(file=Misc.save_image(done))


    @commands.command(help="Blur a users avatar!")
    async def blur(self, ctx, user: Member=None):
        av_img = await Misc.fetch_pfp(user or ctx.author)
        done = av_img.filter(ImageFilter.GaussianBlur(radius=8))
        await ctx.send(file=Misc.save_image(done))

    @commands.command(hlep="Generate a fake discord message!", aliases=["fq", "fakeq", "fakemessage", "fakemsg"])
    async def fakequote(self, ctx, user: Optional[Member], *, message):
        user = user or ctx.author

        font = ImageFont.truetype("fonts/Whitney-Medium.ttf", 22, encoding="unic")
        fontsmall = ImageFont.truetype("fonts/Whitney-Medium.ttf", 16, encoding="unic")
        fontnormal = ImageFont.truetype("fonts/Whitney-Medium.ttf", 20, encoding="unic")

        userchar = font.getsize(user.name)[0]
        image = Image.open("images/fake.png")
        
        parser = TwemojiParser(image, parse_discord_emoji=True)
        await parser.draw_text((80, 30), user.name, font=font, fill=(255, 255, 255) if (user.color.to_rgb() == (0, 0, 0)) else Misc.hex_to_rgb(str(user.color)))
        await parser.draw_text((88 + userchar, 33), datetime.now().strftime("Today at %H:%M"), font=fontsmall, fill='grey')
        await parser.draw_text((80, 57), message if len(message) <= 30 else f'{message[:38]}...', font=fontnormal, fill=(220, 221, 222))
        await parser.close()

        CONVERT = await Misc.circle_pfp(user, 50, 50)
        image.paste(CONVERT, (20, 30), CONVERT)
        await ctx.send(file=Misc.save_image(image))

    @commands.command(help="Write a top.gg Review", aliases=["tgg", "topggreview", "topggbotreview", "botreview"])
    async def topgg(self, ctx, user: Optional[Member], *, message):
        user = user or ctx.author
        ran_days = randint(2, 30)

        font = ImageFont.truetype("fonts/karla1.ttf", 19, encoding="unic")
        fontsmall = ImageFont.truetype("fonts/karla1.ttf", 15, encoding="unic")

        userchars = font.getsize(user.name)[0]
        mainimage = Image.open("images/tgg.png")

        parser = TwemojiParser(mainimage, parse_discord_emoji=True)
        await parser.draw_text((126, 43), user.name, font=font, fill='black')
        await parser.draw_text((134 + userchars, 47), f"{ran_days} days ago", font=fontsmall, fill='grey')
        await parser.draw_text((129, 84), message[:30], font=font, fill='black')
        await parser.close()

        CONVERT = await Misc.circle_pfp(user, 41, 41)
        mainimage.paste(CONVERT, (62, 46), CONVERT)
        await ctx.send(file=Misc.save_image(mainimage))

    @commands.command(help="Widen a discord avatar!", aliases=["widen", "putin", "wideputin"])
    async def wide(self, ctx, user: Member=None):
        av_img = await Misc.fetch_pfp(user or ctx.author)
        await ctx.send(file=Misc.save_image(av_img.resize((350, 180))))

    @commands.command(help="Show what you are listening to in a photo!\nYou can also use `w/spotify --artist <artist>` and `w/spotify --song <song>` to find out information about a artist or song. You can also do `w/spotify --current` to show information on the current song you are listening to within spotify.", aliases=["sp"])
    @commands.cooldown(rate=2, per=8, type=commands.BucketType.member)
    async def spotify(self, ctx, user: Optional[Member], option: Optional[str], *, song: Optional[str]):
        if option == "--artist":
            if not song:
                return await ctx.send(f"Sorry {ctx.author.mention} please specify a artist's name!")

            try:
                results = self.sp.search(q=song, limit=1, type='artist')['artists']['items']
                assert results and results[0]
                artist = results[0]
            except (KeyError, AssertionError):
                return await ctx.send(f"Sorry {ctx.author.mention} but that artist does not exist!")
            return await ctx.send(embed=Embed(title=artist['name'], color=self.bot.color).add_field(name="Artist information", value=f"Followers: `{artist['followers']['total']:,}`\nPopularity: `{artist['popularity']}%`\nArtist Link: [`{artist['name']}`](https://open.spotify.com/artist/{artist['id']})").set_thumbnail(url=artist['images'][0]['url']))

        elif option == "--current":
            user = user or ctx.author
            try:
                spotify_activity = next((activity for activity in user.activities if isinstance(activity, Spotify)), None)
                if not spotify_activity:
                    return await ctx.send(f"Sorry {ctx.author.mention} you are not listening to Spotify")
                result = self.sp.search(q=spotify_activity.title, limit=1, type='track')['tracks']['items']
                assert result and result[0]
            except(KeyError, AssertionError):
                return await ctx.send(f"Sorry {ctx.author.mention} but i could not find your current song information.")
            
            res = result[0]
            name = ', '.join([f"[`{artist['name']}`]({artist['external_urls'].get('spotify', 'https://youtube.com/watch?v=dQw4w9WgXcQ')})" for artist in res['artists']])
            duration = time.strftime("%M:%S", time.gmtime(res['duration_ms'] // 1000))
            return await ctx.send(embed=Embed(title=spotify_activity.title, color=self.bot.color).add_field(name="Song information", value=f"Artist(s): {name}\nPopularity: `{res['popularity']}%`\nRelease date: `{res['album']['release_date']}`\nDuration: `{duration}`\nSong Link: [`{res['name']}`](https://open.spotify.com/track/{res['id']})").set_thumbnail(url=res['album']['images'][0]['url']))

        if option == "--song":
            if not song:
                return await ctx.send(f"Sorry {ctx.author.mention} Please specify a song name!")

            try:
                spotify = self.sp.search(q=song, limit=1, type='track')['tracks']['items']
                assert spotify and spotify[0]
            except (KeyError, AssertionError):
                return await ctx.send(f"Sorry {ctx.author.mention} but that song does not exist!")
            
            spotify = spotify[0]
            name = ', '.join([f"[`{artist['name']}`]({artist['external_urls'].get('spotify', 'https://youtube.com/watch?v=dQw4w9WgXcQ')})" for artist in spotify['artists']])
            duration = time.strftime("%M:%S", time.gmtime(spotify['duration_ms'] // 1000))
            return await ctx.send(embed=Embed(title=song, color=self.bot.color).add_field(name="Song information", value=f"Artist(s): {name}\nPopularity: `{spotify['popularity']}%`\nRelease date: `{spotify['album']['release_date']}`\nDuration: `{duration}`\nSong Link: [`{spotify['name']}`](https://open.spotify.com/track/{spotify['id']})").set_thumbnail(url=spotify['album']['images'][0]['url']))
        
        try:
            user = user or ctx.author
            spotify_activity = next((activity for activity in user.activities if isinstance(activity, Spotify)), None)

            if not spotify_activity:
                return await ctx.send(f"Sorry {ctx.author.mention} {user.name} is not currently listening to Spotify.")

            r = await self.session.get(str(spotify_activity.album_cover_url))
            res = BytesIO(await r.read())
            r.close()
            
            dominant_color = ColorThief(res).get_color(quality=40)
            
            font = ImageFont.truetype("fonts/spotify.ttf", 42, encoding="unic")
            fontbold = ImageFont.truetype("fonts/spotify-bold.ttf", 53, encoding="unic")

            title_new = ''.join(item['hepburn'] for item in self.kks.convert(spotify_activity.title))
            album_new = ''.join(item['hepburn'] for item in self.kks.convert(spotify_activity.album))
            artists_new = ', '.join(''.join(item['hepburn'] for item in artist) for artist in [self.kks.convert(artist) for artist in spotify_activity.artists])
            text_colour = 'black' if Misc.relative_luminance(dominant_color) > 0.5 else 'white'

            img = Image.new('RGB', (999, 395), color=dominant_color)

            album = Image.open(res)
            resized_album = album.resize((245, 245))
            img.paste(resized_album, (41, 76))

            parser = TwemojiParser(img, parse_discord_emoji=False)
            await parser.draw_text((300, 90), title_new if len(title_new) <= 20 else f'{title_new[:17]}...', font=fontbold, fill=text_colour) # Top section - Song name
            await parser.draw_text((303, 170), artists_new if len(artists_new) <= 30 else f'{artists_new[:27]}...', font=font, fill=text_colour) # Middle secion - Artists of the song
            await parser.draw_text((303, 228), album_new if len(album_new) <= 30 else f'{album_new[:27]}...', font=font, fill=text_colour) # Album name - Bottom section
            await parser.close()
            await ctx.send(file=Misc.save_image(Misc.add_corners(img, 42)))
        except Exception as e:
            return await ctx.send(e)

    @commands.command(help="Are you a fast typer?!\nUse `w/fast --rank` to see rank.", aliases=["type", "typingtest"])
    @commands.cooldown(rate=3, per=8, type=commands.BucketType.member)
    async def fast(self, ctx, option: Optional[str], user: Optional[Member]=None):
        user = user or ctx.author
        if option in ("--rank", "rank"):
            result = Wealth.collection.find_one({"_id": user.id})
        
            if not result:
                return await ctx.send(f"Sorry {ctx.author.mention} that user is not ranked yet.")
            
            img = Image.new('RGB', (1000, 300), color=(35, 39, 42))
            font = ImageFont.truetype("fonts/Whitney-Medium.ttf", 65, encoding="unic")
            fontsmall = ImageFont.truetype("fonts/Whitney-Medium.ttf", 49, encoding="unic")
            rank = self.collection.find({"points":{"$gt": result['points']}}).count() + 1
            CONVERT = await Misc.circle_pfp(user, 180, 180)
            color = (255, 255, 255) if (user.color.to_rgb() == (0, 0, 0)) else user.color.to_rgb()
            name = user.name if len(user.name) <= 16 else f'{user.name[:13]}...'

            parser = TwemojiParser(img)
            await parser.draw_text((249, 69), name, font=font, fill=color) # Name of author
            await parser.draw_text((250, 160), f"Global rank: #{rank}, Points: {result['points']:,}", font=fontsmall, fill='white') # Current rank, and points
            await parser.close()

            img.paste(CONVERT, (50, 67), CONVERT)
            return await ctx.send(file=Misc.save_image(img))
        
        word = choice(Misc.ALL_WORDS)
        font = ImageFont.truetype("fonts/Arial-bold.ttf", 25, encoding="unic")

        wx, wy = font.getsize(word)
        img = Image.new('RGB', (wx + 30, wy * 2), color='lightblue')

        imgdraw = ImageDraw.Draw(img)
        imgdraw.text((14, 9), word, fill='black', font=font)
        game = await ctx.send(file=Misc.save_image(img))

        while True:
            try:
                start = round(time.time() * 100)
                resp = await self.bot.wait_for("message", check=lambda message: message.channel == ctx.channel and message.guild == ctx.guild and message.content.lower() == word, timeout=18)
                elapse = round(time.time() * 100) - start
                if resp.content.lower() == word:
                    if not Wealth.collection.find_one({"_id": user.id}):
                        Wealth.collection.insert_one({
                            "_id": user.id,
                            "points": 0
                        })
                    
                    isfast = choice(self.badmessages if (elapse/1000 > 6) else self.goodmessages)
                    random_points = randint(10, 45) if (elapse/1000 > 6) else randint(5, 17)
                    Wealth.collection.update_one({"_id": resp.author.id}, {"$inc": {"coins": random_points}})
                    return await ctx.send(embed=Embed(title="Fastest typer!", description=f"{resp.author.mention} typed the word `{word}` first, also has earned `{random_points}` Points.", color=self.bot.color).add_field(name=":alarm_clock: | Time information", value=f"Time took in milliseconds: `{elapse}ms`\nTime took in seconds: `{elapse/1000}s`").add_field(name="<:Worldcool:768201555492864030> | Message from World", value=f"{isfast}", inline=False))
            except:
                await game.delete()
                return await ctx.send(f"Sorry {ctx.author.mention} nobody took part! So i have ended the game.")

    @commands.command(help="Mock some text.")
    async def mock(self, ctx, *, text):
        if not text:
            return await ctx.send(f"Sorry {ctx.author.mention} you forgot to add some text for me to mock.")
        return await ctx.send("".join([choice([index.lower(), index.upper()]) for index in list(text)]))

    @commands.command(help="Guess the flag from the picture!!", aliases=["gtf"])
    async def guesstheflag(self, ctx):
        FlagChosen = choice(list(self.countries.keys()))

        req = await self.session.get(f"https://www.countryflags.io/{FlagChosen}/flat/64.png")
        if req.status >= 400:
            return await ctx.send(f"Sorry {ctx.author.mention} The api is down.")
        
        FirstMessage = await ctx.send(file=File(BytesIO(await req.read()), 'flag.png'), embed=Embed(title="Guess the flag!", color=self.bot.color).set_image(url="attachment://flag.png"))

        while True:
            try:
                start = round(time.time() * 100)
                resp = await self.bot.wait_for("message", check=lambda message: message.channel == ctx.channel and message.guild == ctx.guild and message.content.lower() == self.countries[FlagChosen]['name'], timeout=18)
                elapse = round(time.time() * 100) - start
                if not Wealth._has_account(resp.author.id):
                    Wealth._create_account(resp.author.id)
                RandomCoins = randint(15, 60)
                Wealth.collection.update_one({"_id": resp.author.id}, {"$inc": {"coins": RandomCoins}})
                return await ctx.send(embed=Embed(title="Guess the flag", description=f"{resp.author.mention} guessed the country right!\nThe country was `{FlagChosen['name']}`\nTime took: `{elapse/1000}s`\nCoins earned: `{RandomCoins}`", color=self.bot.color))
            except:
                await FirstMessage.delete()
                return await ctx.send(f"Sorry {ctx.author.mention} nobody guessed the flag! It was: `{FlagChosen['name']}`")
    
    @commands.command()
    async def steam(self, ctx, user: Optional[Member], *, message = None):
        """Returns a Image of a Steam notifaction!"""
        user = user or ctx.author
        image = Image.open("images/steam.png")
        font = ImageFont.truetype("fonts/Arial.ttf", 46, encoding="unic") # Steam's notifaction font.

        pfp = await Misc.fetch_pfp(user)
        CONVERT = pfp.resize((140, 140)) # Resize the Members Avatar.

        KKS_MESSAGE_CONVERT = ''.join(item['hepburn'] for item in self.kks.convert(message or "Nothing")) # Transliteration if the text is CJK
        KKS_NAME_CONVERT = ''.join(item['hepburn'] for item in self.kks.convert(user.name)) # Transliteration if the text is CJK

        MSG_CHECK = KKS_MESSAGE_CONVERT if len(KKS_MESSAGE_CONVERT) <= 25 else f'{KKS_MESSAGE_CONVERT[:22]}'
        NAME_CHECK = KKS_NAME_CONVERT if len(KKS_NAME_CONVERT) <= 25 else f'{KKS_NAME_CONVERT[:22]}...'

        parser = TwemojiParser(image)
        await parser.draw_text((262, 77), NAME_CHECK, font=font, fill=(139, 195, 21)) # Name of discord.Member
        await parser.draw_text((264, 132), "is now playing", font=font, fill="grey")
        await parser.draw_text((263, 188), MSG_CHECK, font=font, fill=(139, 195, 21)) # Message/Game name (message)
        await parser.close() # Close the session

        image.paste(CONVERT, (92, 92), CONVERT)
        return await ctx.send(file=Misc.save_image(image))

    @commands.command(help="Returns a random emoji out of all the emojis.", aliases=["re", "ranemoji"])
    async def randomemoji(self, ctx):
        return await ctx.send(f":{choice(Misc.ALL_EMOJIS)}:")

    @commands.command(help="Search something in google...", alises=["gs", "googlesearch"])
    async def google(self, ctx, *, text):
        image = Image.open("images/google.png")
        font = ImageFont.truetype("fonts/Arial.ttf", 20, encoding="unic")

        query = text if len(text) <=57 else f"{text[:54]}..."

        parser = TwemojiParser(image, parse_discord_emoji=False)
        await parser.draw_text((116,208), query.lower(), font=font, fill=(0,0,0))
        await parser.close()

        return await ctx.send(file=Misc.save_image(image))


def setup(bot):
    bot.add_cog(FunCog(bot))