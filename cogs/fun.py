import discord
import aggdraw
import spotipy

from aiohttp import ClientSession
from random import randint, choice
from pykakasi import kakasi
from discord.ext import commands, tasks
from discord import Embed
from discord import File
from datetime import datetime
from typing import Optional
from humanfriendly import format_timespan
from io import BytesIO
from os import environ

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
from twemoji_parser import TwemojiParser
from colorthief import ColorThief

from urllib.parse import urlparse, quote
from akinator.async_aki import Akinator
from dotenv import load_dotenv
from time import time
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()

akiObj = Akinator()
kks = kakasi()

words = ["abandon","ability","able","about","above","absent","absorb","abstract","absurd","abuse","access","accident","account","accuse","achieve","acid","acoustic","acquire","across","act","action","actor","actress","actual","adapt","add","addict","address","adjust","admit","adult","advance","advice","aerobic","affair","afford","afraid","again","age","agent","agree","ahead","aim","air","airport","aisle","alarm","album","alcohol","alert","alien","all","alley","allow","almost","alone","alpha","already","also","alter","always","amateur","amazing","among","amount","amused","analyst","anchor","ancient","anger","angle","angry","animal","ankle","announce","annual","another","answer","antenna","antique","anxiety","any","apart","apology","appear","apple","approve","april","arch","arctic","area","arena","argue","arm","armed","armor","army","around","arrange","arrest","arrive","arrow","art","artefact","artist","artwork","ask","aspect","assault","asset","assist","assume","asthma","athlete","atom","attack","attend","attitude","attract","auction","audit","august","aunt","author","auto","autumn","average","avocado","avoid","awake","aware","away","awesome","awful","awkward","axis","baby","bachelor","bacon","badge","bag","balance","balcony","ball","bamboo","banana","banner","bar","barely","bargain","barrel","base","basic","basket","battle","beach","bean","beauty","because","become","beef","before","begin","behave","behind","believe","below","belt","bench","benefit","best","betray","better","between","beyond","bicycle","bid","bike","bind","biology","bird","birth","bitter","black","blade","blame","blanket","blast","bleak","bless","blind","blood","blossom","blouse","blue","blur","blush","board","boat","body","boil","bomb","bone","bonus","book","boost","border","boring","borrow","boss","bottom","bounce","box","boy","bracket","brain","brand","brass","brave","bread","breeze","brick","bridge","brief","bright","bring","brisk","broccoli","broken","bronze","broom","brother","brown","brush","bubble","buddy","budget","buffalo","build","bulb","bulk","bullet","bundle","bunker","burden","burger","burst","bus","business","busy","butter","buyer","buzz","cabbage","cabin","cable","cactus","cage","cake","call","calm","camera","camp","can","canal","cancel","candy","cannon","canoe","canvas","canyon","capable","capital","captain","car","carbon","card","cargo","carpet","carry","cart","case","cash","casino","castle","casual","cat","catalog","catch","category","cattle","caught","cause","caution","cave","ceiling","celery","cement","census","century","cereal","certain","chair","chalk","champion","change","chaos","chapter","charge","chase","chat","cheap","check","cheese","chef","cherry","chest","chicken","chief","child","chimney","choice","choose","chronic","chuckle","chunk","churn","cigar","cinnamon","circle","citizen","city","civil","claim","clap","clarify","claw","clay","clean","clerk","clever","click","client","cliff","climb","clinic","clip","clock","clog","close","cloth","cloud","clown","club","clump","cluster","clutch","coach","coast","coconut","code","coffee","coil","coin","collect","color","column","combine","come","comfort","comic","common","company","concert","conduct","confirm","congress","connect","consider","control","convince","cook","cool","copper","copy","coral","core","corn","correct","cost","cotton","couch","country","couple","course","cousin","cover","coyote","crack","cradle","craft","cram","crane","crash","crater","crawl","crazy","cream","credit","creek","crew","cricket","crime","crisp","critic","crop","cross","crouch","crowd","crucial","cruel","cruise","crumble","crunch","crush","cry","crystal","cube","culture","cup","cupboard","curious","current","curtain","curve","cushion","custom","cute","cycle","dad","damage","damp","dance","danger","daring","dash","daughter","dawn","day","deal","debate","debris","decade","december","decide","decline","decorate","decrease","deer","defense","define","defy","degree","delay","deliver","demand","demise","denial","dentist","deny","depart","depend","deposit","depth","deputy","derive","describe","desert","design","desk","despair","destroy","detail","detect","develop","device","devote","diagram","dial","diamond","diary","dice","diesel","diet","differ","digital","dignity","dilemma","dinner","dinosaur","direct","dirt","disagree","discover","disease","dish","dismiss","disorder","display","distance","divert","divide","divorce","dizzy","doctor","document","dog","doll","dolphin","domain","donate","donkey","donor","door","dose","double","dove","draft","dragon","drama","drastic","draw","dream","dress","drift","drill","drink","drip","drive","drop","drum","dry","duck","dumb","dune","during","dust","dutch","duty","dwarf","dynamic","eager","eagle","early","earn","earth","easily","east","easy","echo","ecology","economy","edge","edit","educate","effort","egg","eight","either","elbow","elder","electric","elegant","element","elephant","elevator","elite","else","embark","embody","embrace","emerge","emotion","employ","empower","empty","enable","enact","end","endless","endorse","enemy","energy","enforce","engage","engine","enhance","enjoy","enlist","enough","enrich","enroll","ensure","enter","entire","entry","envelope","episode","equal","equip","era","erase","erode","erosion","error","erupt","escape","essay","essence","estate","eternal","ethics","evidence","evil","evoke","evolve","exact","example","excess","exchange","excite","exclude","excuse","execute","exercise","exhaust","exhibit","exile","exist","exit","exotic","expand","expect","expire","explain","expose","express","extend","extra","eye","eyebrow","fabric","face","faculty","fade","faint","faith","fall","false","fame","family","famous","fan","fancy","fantasy","farm","fashion","fat","fatal","father","fatigue","fault","favorite","feature","february","federal","fee","feed","feel","female","fence","festival","fetch","fever","few","fiber","fiction","field","figure","file","film","filter","final","find","fine","finger","finish","fire","firm","first","fiscal","fish","fit","fitness","fix","flag","flame","flash","flat","flavor","flee","flight","flip","float","flock","floor","flower","fluid","flush","fly","foam","focus","fog","foil","fold","follow","food","foot","force","forest","forget","fork","fortune","forum","forward","fossil","foster","found","fox","fragile","frame","frequent","fresh","friend","fringe","frog","front","frost","frown","frozen","fruit","fuel","fun","funny","furnace","fury","future","gadget","gain","galaxy","gallery","game","gap","garage","garbage","garden","garlic","garment","gas","gasp","gate","gather","gauge","gaze","general","genius","genre","gentle","genuine","gesture","ghost","giant","gift","giggle","ginger","giraffe","girl","give","glad","glance","glare","glass","glide","glimpse","globe","gloom","glory","glove","glow","glue","goat","goddess","gold","good","goose","gorilla","gospel","gossip","govern","gown","grab","grace","grain","grant","grape","grass","gravity","great","green","grid","grief","grit","grocery","group","grow","grunt","guard","guess","guide","guilt","guitar","gun","gym","habit","hair","half","hammer","hamster","hand","happy","harbor","hard","harsh","harvest","hat","have","hawk","hazard","head","health","heart","heavy","hedgehog","height","hello","helmet","help","hen","hero","hidden","high","hill","hint","hip","hire","history","hobby","hockey","hold","hole","holiday","hollow","home","honey","hood","hope","horn","horror","horse","hospital","host","hotel","hour","hover","hub","huge","human","humble","humor","hundred","hungry","hunt","hurdle","hurry","hurt","husband","hybrid","ice","icon","idea","identify","idle","ignore","ill","illegal","illness","image","imitate","immense","immune","impact","impose","improve","impulse","inch","include","income","increase","index","indicate","indoor","industry","infant","inflict","inform","inhale","inherit","initial","inject","injury","inmate","inner","innocent","input","inquiry","insane","insect","inside","inspire","install","intact","interest","into","invest","invite","involve","iron","island","isolate","issue","item","ivory","jacket","jaguar","jar","jazz","jealous","jeans","jelly","jewel","job","join","joke","journey","joy","judge","juice","jump","jungle","junior","junk","just","kangaroo","keen","keep","ketchup","key","kick","kid","kidney","kind","kingdom","kiss","kit","kitchen","kite","kitten","kiwi","knee","knife","knock","know","lab","label","labor","ladder","lady","lake","lamp","language","laptop","large","later","latin","laugh","laundry","lava","law","lawn","lawsuit","layer","lazy","leader","leaf","learn","leave","lecture","left","leg","legal","legend","leisure","lemon","lend","length","lens","leopard","lesson","letter","level","liar","liberty","library","license","life","lift","light","like","limb","limit","link","lion","liquid","list","little","live","lizard","load","loan","lobster","local","lock","logic","lonely","long","loop","lottery","loud","lounge","love","loyal","lucky","luggage","lumber","lunar","lunch","luxury","lyrics","machine","mad","magic","magnet","maid","mail","main","major","make","mammal","man","manage","mandate","mango","mansion","manual","maple","marble","march","margin","marine","market","marriage","mask","mass","master","match","material","math","matrix","matter","maximum","maze","meadow","mean","measure","meat","mechanic","medal","media","melody","melt","member","memory","mention","menu","mercy","merge","merit","merry","mesh","message","metal","method","middle","midnight","milk","million","mimic","mind","minimum","minor","minute","miracle","mirror","misery","miss","mistake","mix","mixed","mixture","mobile","model","modify","mom","moment","monitor","monkey","monster","month","moon","moral","more","morning","mosquito","mother","motion","motor","mountain","mouse","move","movie","much","muffin","mule","multiply","muscle","museum","mushroom","music","must","mutual","myself","mystery","myth","naive","name","napkin","narrow","nasty","nation","nature","near","neck","need","negative","neglect","neither","nephew","nerve","nest","net","network","neutral","never","news","next","nice","night","noble","noise","nominee","noodle","normal","north","nose","notable","note","nothing","notice","novel","now","nuclear","number","nurse","nut","oak","obey","object","oblige","obscure","observe","obtain","obvious","occur","ocean","october","odor","off","offer","office","often","oil","okay","old","olive","olympic","omit","once","one","onion","online","only","open","opera","opinion","oppose","option","orange","orbit","orchard","order","ordinary","organ","orient","original","orphan","ostrich","other","outdoor","outer","output","outside","oval","oven","over","own","owner","oxygen","oyster","ozone","pact","paddle","page","pair","palace","palm","panda","panel","panic","panther","paper","parade","parent","park","parrot","party","pass","patch","path","patient","patrol","pattern","pause","pave","payment","peace","peanut","pear","peasant","pelican","pen","penalty","pencil","people","pepper","perfect","permit","person","pet","phone","photo","phrase","physical","piano","picnic","picture","piece","pig","pigeon","pill","pilot","pink","pioneer","pipe","pistol","pitch","pizza","place","planet","plastic","plate","play","please","pledge","pluck","plug","plunge","poem","poet","point","polar","pole","police","pond","pony","pool","popular","portion","position","possible","post","potato","pottery","poverty","powder","power","practice","praise","predict","prefer","prepare","present","pretty","prevent","price","pride","primary","print","priority","prison","private","prize","problem","process","produce","profit","program","project","promote","proof","property","prosper","protect","proud","provide","public","pudding","pull","pulp","pulse","pumpkin","punch","pupil","puppy","purchase","purity","purpose","purse","push","put","puzzle","pyramid","quality","quantum","quarter","question","quick","quit","quiz","quote","rabbit","raccoon","race","rack","radar","radio","rail","rain","raise","rally","ramp","ranch","random","range","rapid","rare","rate","rather","raven","raw","razor","ready","real","reason","rebel","rebuild","recall","receive","recipe","record","recycle","reduce","reflect","reform","refuse","region","regret","regular","reject","relax","release","relief","rely","remain","remember","remind","remove","render","renew","rent","reopen","repair","repeat","replace","report","require","rescue","resemble","resist","resource","response","result","retire","retreat","return","reunion","reveal","review","reward","rhythm","rib","ribbon","rice","rich","ride","ridge","rifle","right","rigid","ring","riot","ripple","risk","ritual","rival","river","road","roast","robot","robust","rocket","romance","roof","rookie","room","rose","rotate","rough","round","route","royal","rubber","rude","rug","rule","run","runway","rural","sad","saddle","sadness","safe","sail","salad","salmon","salon","salt","salute","same","sample","sand","satisfy","satoshi","sauce","sausage","save","say","scale","scan","scare","scatter","scene","scheme","school","science","scissors","scorpion","scout","scrap","screen","script","scrub","sea","search","season","seat","second","secret","section","security","seed","seek","segment","select","sell","seminar","senior","sense","sentence","series","service","session","settle","setup","seven","shadow","shaft","shallow","share","shed","shell","sheriff","shield","shift","shine","ship","shiver","shock","shoe","shoot","shop","short","shoulder","shove","shrimp","shrug","shuffle","shy","sibling","sick","side","siege","sight","sign","silent","silk","silly","silver","similar","simple","since","sing","siren","sister","situate","six","size","skate","sketch","ski","skill","skin","skirt","skull","slab","slam","sleep","slender","slice","slide","slight","slim","slogan","slot","slow","slush","small","smart","smile","smoke","smooth","snack","snake","snap","sniff","snow","soap","soccer","social","sock","soda","soft","solar","soldier","solid","solution","solve","someone","song","soon","sorry","sort","soul","sound","soup","source","south","space","spare","spatial","spawn","speak","special","speed","spell","spend","sphere","spice","spider","spike","spin","spirit","split","spoil","sponsor","spoon","sport","spot","spray","spread","spring","spy","square","squeeze","squirrel","stable","stadium","staff","stage","stairs","stamp","stand","start","state","stay","steak","steel","stem","step","stereo","stick","still","sting","stock","stomach","stone","stool","story","stove","strategy","street","strike","strong","struggle","student","stuff","stumble","style","subject","submit","subway","success","such","sudden","suffer","sugar","suggest","suit","summer","sun","sunny","sunset","super","supply","supreme","sure","surface","surge","surprise","surround","survey","suspect","sustain","swallow","swamp","swap","swarm","swear","sweet","swift","swim","swing","switch","sword","symbol","symptom","syrup","system","table","tackle","tag","tail","talent","talk","tank","tape","target","task","taste","tattoo","taxi","teach","team","tell","ten","tenant","tennis","tent","term","test","text","thank","that","theme","then","theory","there","they","thing","this","thought","three","thrive","throw","thumb","thunder","ticket","tide","tiger","tilt","timber","time","tiny","tip","tired","tissue","title","toast","tobacco","today","toddler","toe","together","toilet","token","tomato","tomorrow","tone","tongue","tonight","tool","tooth","top","topic","topple","torch","tornado","tortoise","toss","total","tourist","toward","tower","town","toy","track","trade","traffic","tragic","train","transfer","trap","trash","travel","tray","treat","tree","trend","trial","tribe","trick","trigger","trim","trip","trophy","trouble","truck","true","truly","trumpet","trust","truth","try","tube","tuition","tumble","tuna","tunnel","turkey","turn","turtle","twelve","twenty","twice","twin","twist","two","type","typical","ugly","umbrella","unable","unaware","uncle","uncover","under","undo","unfair","unfold","unhappy","uniform","unique","unit","universe","unknown","unlock","until","unusual","unveil","update","upgrade","uphold","upon","upper","upset","urban","urge","usage","use","used","useful","useless","usual","utility","vacant","vacuum","vague","valid","valley","valve","van","vanish","vapor","various","vast","vault","vehicle","velvet","vendor","venture","venue","verb","verify","version","very","vessel","veteran","viable","vibrant","vicious","victory","video","view","village","vintage","violin","virtual","virus","visa","visit","visual","vital","vivid","vocal","voice","void","volcano","volume","vote","voyage","wage","wagon","wait","walk","wall","walnut","want","warfare","warm","warrior","wash","wasp","waste","water","wave","way","wealth","weapon","wear","weasel","weather","web","wedding","weekend","weird","welcome","west","wet","whale","what","wheat","wheel","when","where","whip","whisper","wide","width","wife","wild","will","win","window","wine","wing","wink","winner","winter","wire","wisdom","wise","wish","witness","wolf","woman","wonder","wood","wool","word","work","world","worry","worth","wrap","wreck","wrestle","wrist","write","wrong","yard","year","yellow","you","young","youth","zebra","zero","zone","zoo"]

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=environ["SP_ID"], client_secret=environ["SP_SECRET"]))

def add_corners(im, rad): # Thanks to Stackoverflow: https://stackoverflow.com/questions/11287402/how-to-round-corner-a-logo-without-white-backgroundtransparent-on-it-using-pi/11291419#11291419
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2, rad * 2), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im

def round_corner_jpg(image, radius): # # Thanks to Stackoverflow: https://stackoverflow.com/questions/11287402/how-to-round-corner-a-logo-without-white-backgroundtransparent-on-it-using-pi/11291419#11291419
    mask = Image.new('L', image.size)
    draw = aggdraw.Draw(mask)
    brush = aggdraw.Brush('white')
    width, height = mask.size
    draw.pieslice((0,0,radius*2, radius*2), 90, 180, None, brush)
    draw.pieslice((width - radius*2, 0, width, radius*2), 0, 90, None, brush)
    draw.pieslice((0, height - radius * 2, radius*2, height),180, 270, None, brush)
    draw.pieslice((width - radius * 2, height - radius * 2, width, height), 270, 360, None, brush)
    draw.rectangle((radius, radius, width - radius, height - radius), brush)
    draw.rectangle((radius, 0, width - radius, radius), brush)
    draw.rectangle((0, radius, radius, height-radius), brush)
    draw.rectangle((radius, height-radius, width-radius, height), brush)
    draw.rectangle((width-radius, radius, width, height-radius), brush)
    draw.flush()
    image = image.convert('RGBA')
    image.putalpha(mask)
    return image

def relative_luminance(rgb_triplet):
    r, g, b = tuple(x / 255 for x in rgb_triplet)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

class FunCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.gameCache = {}
        self.color = 0x2F3136
        self.session = ClientSession()

    @commands.command(help="World can make you laugh with his amazing jokes!")
    async def joke(self, ctx):
        headers = {"Accept": "application/json"}
        res = await self.session.get("https://icanhazdadjoke.com", headers=headers)
        r = await req.json()
        embed = Embed(
            title="Epic joke!",
            description=r["joke"],
            color=self.color
            )
        await ctx.send(embed=embed)

    @commands.command(help="Ask Alister-A a question!")
    async def askali(self, ctx, *, question):
        responses = [
            "Ali A Kills Himself",
            "Ali A Ignores And Hits A 360 Noscope",
            "Ali A Approves",
            "Ali A Dosnt Approve"
        ]
        embed = Embed(title="Ask Alister-A", description=f"{ctx.author.mention} - {choice(responses)}", color=self.color)
        embed.add_field(name=f"**Question**", value=f'{question}', inline=False)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/710141167722824070/717777626877395004/aaaaa.png')
        await ctx.send(embed=embed)

    @askali.error
    async def askali_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/askali <question>`")


    @commands.command(name="f", help="Give respects.")
    async def f(self, ctx, *, text: commands.clean_content = None):
        sean = ['💔', '💝', '💚', '💙', '💜']
        reason = f"for **{text}** " if text else ""
        finchat = Embed(title = f"**{ctx.author.name}** has paid their respect {reason}{choice(sean)}", color=self.color)
        await ctx.send(embed=finchat)

    @commands.command(help="Shows a meme from random subreddits.")
    @commands.cooldown(rate=4, per=7, type=commands.BucketType.member)
    async def meme(self, ctx):
        r = await self.session.get(f"https://memes.blademaker.tv/api?lang=en")
        res = await r.json()
        embed = Embed(title=f"Title: {res['title']}\nSubreddit: r/{res['subreddit']}", color=self.color)
        embed.set_image(url=res["image"])
        embed.set_footer(text=f"👍Ups:{res['ups']}")
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
        size = randint(1, 15)
        dong = ""
        for _i in range(0, size):
            dong += "="
        embed = Embed(title=f"{user}'s pepe size", description=f"8{dong}D", color=self.color)
        await ctx.send(embed=embed)

    @commands.command(help="Steal a users avatar.", aliases=["av"])
    async def avatar(self, ctx, *, user: discord.Member=None):
        format = "gif"
        user = user or ctx.author
        if user.is_avatar_animated() != True:
            format = "png"
        avatar = user.avatar_url_as(format = format if format != "gif" else None)
        resp = await self.session.get(str(avatar))
        image = await resp.read()
        with BytesIO(image) as file:
            await ctx.send(file=File(file, f"Avatar.{format}"))

    @commands.command(help="Fake tweet text.")
    async def tweet(self, ctx, username: str, *, message: str):
        if len(message) >50:
            return await ctx.send(f"Sorry {ctx.author.mention} a limit of `50` chars please.")
        r = await self.session.get(f"https://nekobot.xyz/api/imagegen?type=tweet&username={username}&text={message}")
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
        randomPercentage = randint(1, 100)
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
            except:
                await ctx.send(embed=Embed(
                    title="Hurry next time!",
                    description=
                    f"{ctx.author.mention} took too long to respond so we ended the game\nCurrent timeout: `15` Seconds.", color=self.color))
                del self.gameCache[ctx.channel.id]
                return await message1.delete(delay=None)
            if resp.content == "b":
                try:
                    gameObj = await akiObj.back()
                except:
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
            "World Says Yes.",
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
        ]
        embed = Embed(title=":8ball: The Almighty 8ball :8ball:", description=f"Question = `{question}`\n **Answer**: :8ball: {choice(responses)} :8ball:", color=self.color)
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/717038947846455406/717784205249085470/aaaaaaaaaaaaaaaaaaa.png')
        await ctx.send(embed=embed)

    @_8ball.error
    async def _8ball_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/8ball <question>`")

    @commands.command(help="Turn text into emojis!.")
    async def emojify(self, ctx, *, stuff):
        if len(stuff) > 20:
            return await ctx.send(f"Sorry {ctx.author.mention} a limit of `20` chars please!")
        emj = ("".join([":regional_indicator_"+l+":"  if l in "abcdefghijklmnopqrstuvwyx" else [":zero:", ":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:", ":nine:"][int(l)] if l.isdigit() else ":question:" if l == "?" else ":exclamation:" if l == "!" else l for l in f"{stuff}"]))
        embed = Embed(title='Emojify', description=f'{emj}', color=self.color)
        await ctx.send(embed=embed)

    @emojify.error
    async def emojify_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/emojify <text>`")

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
            description=f"{ctx.author.mention} you killed {user.mention} because {choice(kills)}",
            color=self.color
            )
        await ctx.send(embed=embed)

    @commands.command(help="Urban Dictionary")
    @commands.is_nsfw()
    async def urban(self, ctx, *name):
        if ctx.channel.is_nsfw():
            r = await self.session.get(f"http://api.urbandictionary.com/v0/define?term={'%20'.join(name)}")
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
        r = await self.session.get(f"https://api.adviceslip.com/advice", headers={"Accept": "application/json"})
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

    @qr.error
    async def qr_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/qr <text>`")

    @commands.command(help="This command will show you a cute duck", aliases=['quack', 'duk'])
    async def duck(self, ctx):
        r = await self.session.get('https://random-d.uk/api/v2/random')
        res = await r.json()
        embed = Embed(
            title='Quack!',
            color=self.color
        ).set_image(url=res['url'])
        await ctx.send(embed=embed)

    @commands.command(help="Flip a users avatar!", aliases=["flipav", "avflip"])
    async def flip(self, ctx, user: discord.Member=None):
        user = user or ctx.author

        pfp = user.avatar_url_as(format='png')

        buffer_avatar = BytesIO()
        await pfp.save(buffer_avatar)
        buffer_avatar.seek(0)

        av_img = Image.open(buffer_avatar)

        done = av_img.rotate(180)

        buffer = BytesIO()

        done.save(buffer, format='PNG')

        buffer.seek(0)

        file = File(buffer, "flippedimg.png")
        embed = Embed(title="Flip!", description=f"{user}'s avatar flipped", color=0x2F3136)
        embed.set_image(url="attachment://flippedimg.png")
        await ctx.send(embed=embed, file=file)


    @commands.command(help="Blur a users avatar!")
    async def blur(self, ctx, user: discord.Member=None):
        user = user or ctx.author
        pfp = user.avatar_url_as(format='png')
        buffer_avatar = BytesIO()

        await pfp.save(buffer_avatar)

        buffer_avatar.seek(0)

        av_img = Image.open(buffer_avatar)
        done = av_img.filter(ImageFilter.GaussianBlur(radius=8))

        buffer = BytesIO()
        done.save(buffer, format='PNG')
        buffer.seek(0)

        file = File(buffer, "blurimg.png")
        embed = Embed(title="blur!", description=f"{user}'s avatar blurred", color=0x2F3136)
        embed.set_image(url="attachment://blurimg.png")
        await ctx.send(embed=embed, file=file)

    @commands.command(hlep="Generate a fake discord message!", aliases=["fq", "fakeq", "fakemessage", "fakemsg"])
    async def fakequote(self, ctx, user: Optional[discord.Member], *, message) -> None:
        if len(message) > 50:
            return await ctx.send(f"Sorry {ctx.author.mention} there is a limit of `50` chars.")
        now = datetime.now()
        user = user or ctx.author
        pfp = user.avatar_url_as(format='png')
        buffer_avatar = BytesIO()

        await pfp.save(buffer_avatar)

        buffer_avatar.seek(0)
        font = ImageFont.truetype("fonts/Whitney-Medium.ttf", 22, encoding="unic")
        fontsmall = ImageFont.truetype("fonts/Whitney-Medium.ttf", 16, encoding="unic")
        fontnormal = ImageFont.truetype("fonts/Whitney-Medium.ttf", 20, encoding="unic")

        userchar = font.getsize(user.name)[0]

        av_img = Image.open(buffer_avatar)
        image = Image.open("images/fake.png")
        parser = TwemojiParser(image, session=self.session, parse_discord_emoji=True)
        await parser.draw_text((73, 65), user.name, fill='white', font=font)
        await parser.draw_text((73 + userchar + 8, 69), str(now.strftime("Today at %H:%M")), fill='grey', font=fontsmall)
        await parser.draw_text((74, 95), message, fill='white', font=fontnormal)
        await parser.close(close_session=False)

        resized = av_img.resize((45, 45));
        bigger = (resized.size[0] * 3, resized.size[1] * 3)
        maskimage = Image.new('L', bigger, 0)
        draw = ImageDraw.Draw(maskimage)
        draw.ellipse((0, 0) + bigger, fill=255)
        maskimage = maskimage.resize(resized.size, Image.ANTIALIAS)
        resized.putalpha(maskimage)

        output = ImageOps.fit(resized, maskimage.size, centering=(0.5, 0.5))
        output.putalpha(maskimage)
        image.paste(resized, (19, 69), resized)
        buffer = BytesIO()
        image.save(buffer, format='PNG')
        buffer.seek(0)

        file = File(buffer, "fakequote.png")
        embed = Embed(color=0x2F3136)
        embed.set_image(url="attachment://fakequote.png")
        await ctx.send(embed=embed, file=file)

    @fakequote.error
    async def fakequote_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/fakequote <user> <text>`")

    @commands.command(help="Write a top.gg Review", aliases=["tgg", "topggreview", "topggbotreview", "botreview"])
    async def topgg(self, ctx, user: Optional[discord.Member], *, message):
        user = user or ctx.author
        if len(message) > 30:
            return await ctx.send(f"Sorry {ctx.author.mention} there is a limit of `30` chars.")

        ran_days = randint(2, 30)
        picture = user.avatar_url_as(format='png')
        buf_avatar = BytesIO()

        await picture.save(buf_avatar)
        buf_avatar.seek(0)

        font = ImageFont.truetype("fonts/karla1.ttf", 19, encoding="unic")
        fontsmall = ImageFont.truetype("fonts/karla1.ttf", 15, encoding="unic")
        fontnormal = ImageFont.truetype("fonts/karla1.ttf", 18, encoding="unic")

        userchars = font.getsize(user.name)[0]

        mainimage = Image.open("images/tgg.png")
        parser = TwemojiParser(mainimage, session=self.session, parse_discord_emoji=True)
        await parser.draw_text((126, 43), user.name, fill='black', font=font)
        await parser.draw_text((132 + userchars + 2, 47.8), f"{ran_days} days ago", fill='grey', font=fontsmall)
        await parser.draw_text((129, 84), message, fill='black', font=font)
        await parser.close(close_session=False)

        user_picture = Image.open(buf_avatar)

        resize = user_picture.resize((41, 41));
        size_bigger = (resize.size[0] * 3, resize.size[1] * 3)
        maskimage = Image.new('L', size_bigger, 0)
        draw = ImageDraw.Draw(maskimage)
        draw.ellipse((0, 0) + size_bigger, fill=255)
        maskimage = maskimage.resize(resize.size, Image.ANTIALIAS)
        resize.putalpha(maskimage)

        output = ImageOps.fit(resize, maskimage.size, centering=(0.5, 0.5))
        output.putalpha(maskimage)
        mainimage.paste(resize, (62, 46), resize)

        buffer = BytesIO()
        mainimage.save(buffer, format='PNG')
        buffer.seek(0)

        file = File(buffer, "topggreview.png")
        embed = Embed(color=0x2F3136)
        embed.set_image(url="attachment://topggreview.png")
        await ctx.send(embed=embed, file=file)

    @topgg.error
    async def topgg_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/topgg <user> <text>`")

    @commands.command(help="Widen a discord avatar!", aliases=["widen", "putin", "wideputin"])
    async def wide(self, ctx, user: discord.Member=None):
        user = user or ctx.author

        pfp = user.avatar_url_as(format='png')

        buffer_avatar = BytesIO()
        await pfp.save(buffer_avatar)
        buffer_avatar.seek(0)

        av_img = Image.open(buffer_avatar)

        done = av_img.resize((350, 180))

        buffer = BytesIO()

        done.save(buffer, format='PNG')

        buffer.seek(0)

        file = File(buffer, "stretch.png")
        embed = Embed(title="Wide!", description=f"{user}'s avatar widened", color=0x2F3136)
        embed.set_image(url="attachment://stretch.png")
        await ctx.send(embed=embed, file=file)


    @commands.command(help="Show what you are listening to in a photo!\nYou can also use `w/spotify --artist <artist>` and `w/spotify --song <song>` to find out information about a artist or song.", aliases=["sp"])
    @commands.cooldown(rate=2, per=8, type=commands.BucketType.member)
    async def spotify(self, ctx, user: Optional[discord.Member], option: Optional[str], *, song: Optional[str]):
        if option == "--artist":
        	if song == None:
        		return await ctx.send(f"Sorry {ctx.author.mention} please specify a artist's name!")
        	results = sp.search(q=song, limit=1, type='artist')
        	for track in results:
        		items = results['artists']['items']
        		try:
        			artist = items[0]
        		except IndexError:
        			return await ctx.send(f"Sorry {ctx.author.mention} but that artist does not exist!")
        		embed = Embed(title=artist['name'], color=0x2F3136)
        		embed.add_field(name="Artist information", value=f"Followers: `{artist['followers']['total']:,}`\nPopularity: `{artist['popularity']}%`\nArtist Link: [`{artist['name']}`](https://open.spotify.com/artist/{artist['id']})")
        		embed.set_thumbnail(url=artist['images'][0]['url'])
        		return await ctx.send(embed=embed)
        if option == "--song":
        	if song == None:
        		return await ctx.send(f"Sorry {ctx.author.mention} Please specify a song name!")
        	results = sp.search(q=song, limit=1, type='track')
        	for track in results:
        		items = results['tracks']['items']
        		try:
        			song = items[0]
        			spotify = results['tracks']['items'][0]
        			name = ', '.join([artist['name'] for artist in spotify['artists']])
        		except IndexError:
        			return await ctx.send(f"Sorry {ctx.author.mention} but that artist does not exist!")
        		embed = Embed(title=song['name'], color=0x2F3136)
        		embed.add_field(name="Song information", value=f"Artist(s): `{name}`\nPopularity: `{song['popularity']}%`\nRelease date: `{spotify['album']['release_date']}`\nSong Link: [`{song['name']}`](https://open.spotify.com/track/{song['id']})")
        		embed.set_thumbnail(url=spotify['album']['images'][0]['url'])
        		return await ctx.send(embed=embed)
        user = user or ctx.author
        spotify_activity = next(
            (activity for activity in user.activities if isinstance(activity, Spotify)),
            None
            )
        if spotify_activity is None:
            return await ctx.send(f"Sorry {ctx.author.mention} {user.name} is not currently listening to Spotify.")

        r = await self.session.get(str(spotify_activity.album_cover_url))
        res = BytesIO(await r.read())

        color_thief = ColorThief(res)
        dominant_color = color_thief.get_color(quality=40)

        font = ImageFont.truetype("fonts/spotify.ttf", 42, encoding="unic")
        fontbold = ImageFont.truetype("fonts/spotify-bold.ttf", 53, encoding="unic")

        title = kks.convert(spotify_activity.title)
        album = kks.convert(spotify_activity.album)
        artists = kks.convert(spotify_activity.artists)

        title_new = ''.join(item['hepburn'] for item in title)
        album_new = ''.join(item['hepburn'] for item in album)
        transliterated_artists = [kks.convert(artist) for artist in spotify_activity.artists]
        artists_new = ', '.join(''.join(item['hepburn'] for item in artist) for artist in transliterated_artists)

        abridged = album_new if len(album_new) <= 30 else f'{album_new[0:27]}...'

        cbridged = title_new if len(title_new) <= 20 else f'{title_new[0:17]}...'

        dbridged = artists_new if len(artists_new) <= 30 else f'{artists_new[0:27]}...'

        luminance = relative_luminance(dominant_color)

        text_colour = 'black' if luminance > 0.5 else 'white'

        img = Image.new('RGB', (999, 395), color=dominant_color)

        album = Image.open(res)
        resized_album = album.resize((245, 245))
        img.paste(resized_album, (41, 76))

        # update to version 0.4.2, it's improved and supports aiohttp client sessions
        parser = TwemojiParser(img, session=self.session)

        await parser.draw_text((303, 170), dbridged, fill=text_colour, font=font) # Artists - Middle section
        await parser.draw_text((300, 90), cbridged, fill=text_colour, font=fontbold) # Title of song - Top section
        await parser.draw_text((303, 228), abridged, fill=text_colour, font=font) # Album name - Bottom section
        await parser.close(close_session=False)

        final = add_corners(img, 55)

        buffer = BytesIO()
        final.save(buffer, format='PNG')
        buffer.seek(0)

        file = File(buffer, "spotify.png")
        await ctx.send(file=file)

    @spotify.error
    async def spotify_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            a = error.retry_after
            a = round(a)
            await ctx.send(f"Sorry {ctx.author.mention} This command in on cooldown, Try again in {a} seconds.")

    @commands.command(help="Are you a fast typer?!", aliases=["type", "typingtest"])
    @commands.cooldown(rate=3, per=8, type=commands.BucketType.member)
    async def fast(self, ctx):

        goodmessages = ["Wow speedy!", "Nice time!", "That was pretty good!", "Wow, you fast at typing!", "You speedy, that's for sure!"]

        badmessages = ["How slow can you type?", "That was slow!", "You need to practice more!", "It's ok i won't tell anybody that your a slow typer"]

        word = choice(words)

        font = ImageFont.truetype("fonts/Arial-bold.ttf", 25, encoding="unic")

        wx, wy = font.getsize(word)
        offset_y = font.getsize(word)[1]
        height = offset_y + wy

        img = Image.new('RGB', (wx+20, height), color='lightblue')
        imgdraw = ImageDraw.Draw(img)
        imgdraw.text((10, 9), word, fill='black', font=font) # no need for twemoji parser since there are no emojis in the array

        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)

        file = File(buffer, "Fast.png")
        game = await ctx.send(file=file)

        while True:
            try:
                start = round(time() * 100)
                resp = await self.bot.wait_for("message", check=lambda message: message.channel == ctx.channel and message.guild == ctx.guild and message.content.lower() == word, timeout=18)
                elapse = round(time() * 100) - start
                if resp.content.lower() == word:
                    if elapse/1000 > 10:
                        isfast = choice(badmessages)
                    else:
                        isfast = choice(goodmessages)
                    embed = Embed(title="Fastest typer!",description=f"{resp.author.mention} typed the word `{word}` first!", color=0x2F3136)
                    embed.add_field(name=":alarm_clock: | Time information", value=f"Time took in milliseconds: `{elapse}ms`\nTime took in seconds: `{elapse/1000}s`")
                    embed.add_field(name="<:Worldcool:768201555492864030> | Message from World", value=f"{isfast}", inline=False)
                    return await ctx.send(embed=embed)
            except:
                await game.delete()
                return await ctx.send(f"Sorry {ctx.author.mention} nobody took part! So i have ended the game.")

    @fast.error
    async def fast_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            a = error.retry_after
            a = round(a)
            await ctx.send(f"Sorry {ctx.author.mention} This command in on cooldown, Try again in {a} seconds.")


def setup(bot):
    bot.add_cog(FunCog(bot))
