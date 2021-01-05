from aiohttp import ClientSession
from random import randint, choice
from pykakasi import kakasi
from discord.ext import commands, tasks
from discord import Embed, File, PartialEmoji, Member, Spotify
from datetime import datetime
from typing import Optional
from io import BytesIO
from os import environ
from asyncio import TimeoutError
from pymongo import MongoClient
from framework import Misc, Wealth
from time import time
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from twemoji_parser import TwemojiParser
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
        self.Country = [{"name":"Afghanistan","code":"AF"},{"name":"Aland Islands","code":"AX"},{"name":"Albania","code":"AL"},{"name":"Algeria","code":"DZ"},{"name":"American Samoa","code":"AS"},{"name":"AndorrA","code":"AD"},{"name":"Angola","code":"AO"},{"name":"Anguilla","code":"AI"},{"name":"Antarctica","code":"AQ"},{"name":"Antigua and Barbuda","code":"AG"},{"name":"Argentina","code":"AR"},{"name":"Armenia","code":"AM"},{"name":"Aruba","code":"AW"},{"name":"Australia","code":"AU"},{"name":"Austria","code":"AT"},{"name":"Azerbaijan","code":"AZ"},{"name":"Bahamas","code":"BS"},{"name":"Bahrain","code":"BH"},{"name":"Bangladesh","code":"BD"},{"name":"Barbados","code":"BB"},{"name":"Belarus","code":"BY"},{"name":"Belgium","code":"BE"},{"name":"Belize","code":"BZ"},{"name":"Benin","code":"BJ"},{"name":"Bermuda","code":"BM"},{"name":"Bhutan","code":"BT"},{"name":"Bolivia","code":"BO"},{"name":"Bosnia and Herzegovina","code":"BA"},{"name":"Botswana","code":"BW"},{"name":"Bouvet Island","code":"BV"},{"name":"Brazil","code":"BR"},{"name":"British Indian Ocean Territory","code":"IO"},{"name":"Brunei Darussalam","code":"BN"},{"name":"Bulgaria","code":"BG"},{"name":"Burkina Faso","code":"BF"},{"name":"Burundi","code":"BI"},{"name":"Cambodia","code":"KH"},{"name":"Cameroon","code":"CM"},{"name":"Canada","code":"CA"},{"name":"Cape Verde","code":"CV"},{"name":"Cayman Islands","code":"KY"},{"name":"Central African Republic","code":"CF"},{"name":"Chad","code":"TD"},{"name":"Chile","code":"CL"},{"name":"China","code":"CN"},{"name":"Christmas Island","code":"CX"},{"name":"Cocos (Keeling) Islands","code":"CC"},{"name":"Colombia","code":"CO"},{"name":"Comoros","code":"KM"},{"name":"Congo","code":"CG"},{"name":"Congo, The Democratic Republic of the","code":"CD"},{"name":"Cook Islands","code":"CK"},{"name":"Costa Rica","code":"CR"},{"name":"Cote D'Ivoire","code":"CI"},{"name":"Croatia","code":"HR"},{"name":"Cuba","code":"CU"},{"name":"Cyprus","code":"CY"},{"name":"Czech Republic","code":"CZ"},{"name":"Denmark","code":"DK"},{"name":"Djibouti","code":"DJ"},{"name":"Dominica","code":"DM"},{"name":"Dominican Republic","code":"DO"},{"name":"Ecuador","code":"EC"},{"name":"Egypt","code":"EG"},{"name":"El Salvador","code":"SV"},{"name":"Equatorial Guinea","code":"GQ"},{"name":"Eritrea","code":"ER"},{"name":"Estonia","code":"EE"},{"name":"Ethiopia","code":"ET"},{"name":"Falkland Islands (Malvinas)","code":"FK"},{"name":"Faroe Islands","code":"FO"},{"name":"Fiji","code":"FJ"},{"name":"Finland","code":"FI"},{"name":"France","code":"FR"},{"name":"French Guiana","code":"GF"},{"name":"French Polynesia","code":"PF"},{"name":"French Southern Territories","code":"TF"},{"name":"Gabon","code":"GA"},{"name":"Gambia","code":"GM"},{"name":"Georgia","code":"GE"},{"name":"Germany","code":"DE"},{"name":"Ghana","code":"GH"},{"name":"Gibraltar","code":"GI"},{"name":"Greece","code":"GR"},{"name":"Greenland","code":"GL"},{"name":"Grenada","code":"GD"},{"name":"Guadeloupe","code":"GP"},{"name":"Guam","code":"GU"},{"name":"Guatemala","code":"GT"},{"name":"Guernsey","code":"GG"},{"name":"Guinea","code":"GN"},{"name":"Guinea-Bissau","code":"GW"},{"name":"Guyana","code":"GY"},{"name":"Haiti","code":"HT"},{"name":"Heard Island and Mcdonald Islands","code":"HM"},{"name":"Holy See (Vatican City State)","code":"VA"},{"name":"Honduras","code":"HN"},{"name":"Hong Kong","code":"HK"},{"name":"Hungary","code":"HU"},{"name":"Iceland","code":"IS"},{"name":"India","code":"IN"},{"name":"Indonesia","code":"ID"},{"name":"Iran, Islamic Republic Of","code":"IR"},{"name":"Iraq","code":"IQ"},{"name":"Ireland","code":"IE"},{"name":"Isle of Man","code":"IM"},{"name":"Israel","code":"IL"},{"name":"Italy","code":"IT"},{"name":"Jamaica","code":"JM"},{"name":"Japan","code":"JP"},{"name":"Jersey","code":"JE"},{"name":"Jordan","code":"JO"},{"name":"Kazakhstan","code":"KZ"},{"name":"Kenya","code":"KE"},{"name":"Kiribati","code":"KI"},{"name":"Korea, Democratic People'S Republic of","code":"KP"},{"name":"Korea, Republic of","code":"KR"},{"name":"Kuwait","code":"KW"},{"name":"Kyrgyzstan","code":"KG"},{"name":"Lao People'S Democratic Republic","code":"LA"},{"name":"Latvia","code":"LV"},{"name":"Lebanon","code":"LB"},{"name":"Lesotho","code":"LS"},{"name":"Liberia","code":"LR"},{"name":"Libyan Arab Jamahiriya","code":"LY"},{"name":"Liechtenstein","code":"LI"},{"name":"Lithuania","code":"LT"},{"name":"Luxembourg","code":"LU"},{"name":"Macao","code":"MO"},{"name":"Macedonia, The Former Yugoslav Republic of","code":"MK"},{"name":"Madagascar","code":"MG"},{"name":"Malawi","code":"MW"},{"name":"Malaysia","code":"MY"},{"name":"Maldives","code":"MV"},{"name":"Mali","code":"ML"},{"name":"Malta","code":"MT"},{"name":"Marshall Islands","code":"MH"},{"name":"Martinique","code":"MQ"},{"name":"Mauritania","code":"MR"},{"name":"Mauritius","code":"MU"},{"name":"Mayotte","code":"YT"},{"name":"Mexico","code":"MX"},{"name":"Micronesia, Federated States of","code":"FM"},{"name":"Moldova, Republic of","code":"MD"},{"name":"Monaco","code":"MC"},{"name":"Mongolia","code":"MN"},{"name":"Montserrat","code":"MS"},{"name":"Morocco","code":"MA"},{"name":"Mozambique","code":"MZ"},{"name":"Myanmar","code":"MM"},{"name":"Namibia","code":"NA"},{"name":"Nauru","code":"NR"},{"name":"Nepal","code":"NP"},{"name":"Netherlands","code":"NL"},{"name":"Netherlands Antilles","code":"AN"},{"name":"New Caledonia","code":"NC"},{"name":"New Zealand","code":"NZ"},{"name":"Nicaragua","code":"NI"},{"name":"Niger","code":"NE"},{"name":"Nigeria","code":"NG"},{"name":"Niue","code":"NU"},{"name":"Norfolk Island","code":"NF"},{"name":"Northern Mariana Islands","code":"MP"},{"name":"Norway","code":"NO"},{"name":"Oman","code":"OM"},{"name":"Pakistan","code":"PK"},{"name":"Palau","code":"PW"},{"name":"Palestinian Territory, Occupied","code":"PS"},{"name":"Panama","code":"PA"},{"name":"Papua New Guinea","code":"PG"},{"name":"Paraguay","code":"PY"},{"name":"Peru","code":"PE"},{"name":"Philippines","code":"PH"},{"name":"Pitcairn","code":"PN"},{"name":"Poland","code":"PL"},{"name":"Portugal","code":"PT"},{"name":"Puerto Rico","code":"PR"},{"name":"Qatar","code":"QA"},{"name":"Reunion","code":"RE"},{"name":"Romania","code":"RO"},{"name":"Russian Federation","code":"RU"},{"name":"RWANDA","code":"RW"},{"name":"Saint Helena","code":"SH"},{"name":"Saint Kitts and Nevis","code":"KN"},{"name":"Saint Lucia","code":"LC"},{"name":"Saint Pierre and Miquelon","code":"PM"},{"name":"Saint Vincent and the Grenadines","code":"VC"},{"name":"Samoa","code":"WS"},{"name":"San Marino","code":"SM"},{"name":"Sao Tome and Principe","code":"ST"},{"name":"Saudi Arabia","code":"SA"},{"name":"Senegal","code":"SN"},{"name":"Serbia and Montenegro","code":"CS"},{"name":"Seychelles","code":"SC"},{"name":"Sierra Leone","code":"SL"},{"name":"Singapore","code":"SG"},{"name":"Slovakia","code":"SK"},{"name":"Slovenia","code":"SI"},{"name":"Solomon Islands","code":"SB"},{"name":"Somalia","code":"SO"},{"name":"South Africa","code":"ZA"},{"name":"South Georgia and the South Sandwich Islands","code":"GS"},{"name":"Spain","code":"ES"},{"name":"Sri Lanka","code":"LK"},{"name":"Sudan","code":"SD"},{"name":"Suriname","code":"SR"},{"name":"Svalbard and Jan Mayen","code":"SJ"},{"name":"Swaziland","code":"SZ"},{"name":"Sweden","code":"SE"},{"name":"Switzerland","code":"CH"},{"name":"Syrian Arab Republic","code":"SY"},{"name":"Taiwan, Province of China","code":"TW"},{"name":"Tajikistan","code":"TJ"},{"name":"Tanzania, United Republic of","code":"TZ"},{"name":"Thailand","code":"TH"},{"name":"Timor-Leste","code":"TL"},{"name":"Togo","code":"TG"},{"name":"Tokelau","code":"TK"},{"name":"Tonga","code":"TO"},{"name":"Trinidad and Tobago","code":"TT"},{"name":"Tunisia","code":"TN"},{"name":"Turkey","code":"TR"},{"name":"Turkmenistan","code":"TM"},{"name":"Turks and Caicos Islands","code":"TC"},{"name":"Tuvalu","code":"TV"},{"name":"Uganda","code":"UG"},{"name":"Ukraine","code":"UA"},{"name":"United Arab Emirates","code":"AE"},{"name":"United Kingdom","code":"GB"},{"name":"United States","code":"US"},{"name":"United States Minor Outlying Islands","code":"UM"},{"name":"Uruguay","code":"UY"},{"name":"Uzbekistan","code":"UZ"},{"name":"Vanuatu","code":"VU"},{"name":"Venezuela","code":"VE"},{"name":"Viet Nam","code":"VN"},{"name":"Virgin Islands, British","code":"VG"},{"name":"Virgin Islands, U.S.","code":"VI"},{"name":"Wallis and Futuna","code":"WF"},{"name":"Western Sahara","code":"EH"},{"name":"Yemen","code":"YE"},{"name":"Zambia","code":"ZM"},{"name":"Zimbabwe","code":"ZW"}]
        self.words = ["abandon","ability","able","about","above","absent","absorb","abstract","absurd","abuse","access","accident","account","accuse","achieve","acid","acoustic","acquire","across","act","action","actor","actress","actual","adapt","add","addict","address","adjust","admit","adult","advance","advice","aerobic","affair","afford","afraid","again","age","agent","agree","ahead","aim","air","airport","aisle","alarm","album","alcohol","alert","alien","all","alley","allow","almost","alone","alpha","already","also","alter","always","amateur","amazing","among","amount","amused","analyst","anchor","ancient","anger","angle","angry","animal","ankle","announce","annual","another","answer","antenna","antique","anxiety","any","apart","apology","appear","apple","approve","april","arch","arctic","area","arena","argue","arm","armed","armor","army","around","arrange","arrest","arrive","arrow","art","artefact","artist","artwork","ask","aspect","assault","asset","assist","assume","asthma","athlete","atom","attack","attend","attitude","attract","auction","audit","august","aunt","author","auto","autumn","average","avocado","avoid","awake","aware","away","awesome","awful","awkward","axis","baby","bachelor","bacon","badge","bag","balance","balcony","ball","bamboo","banana","banner","bar","barely","bargain","barrel","base","basic","basket","battle","beach","bean","beauty","because","become","beef","before","begin","behave","behind","believe","below","belt","bench","benefit","best","betray","better","between","beyond","bicycle","bid","bike","bind","biology","bird","birth","bitter","black","blade","blame","blanket","blast","bleak","bless","blind","blood","blossom","blouse","blue","blur","blush","board","boat","body","boil","bomb","bone","bonus","book","boost","border","boring","borrow","boss","bottom","bounce","box","boy","bracket","brain","brand","brass","brave","bread","breeze","brick","bridge","brief","bright","bring","brisk","broccoli","broken","bronze","broom","brother","brown","brush","bubble","buddy","budget","buffalo","build","bulb","bulk","bullet","bundle","bunker","burden","burger","burst","bus","business","busy","butter","buyer","buzz","cabbage","cabin","cable","cactus","cage","cake","call","calm","camera","camp","can","canal","cancel","candy","cannon","canoe","canvas","canyon","capable","capital","captain","car","carbon","card","cargo","carpet","carry","cart","case","cash","casino","castle","casual","cat","catalog","catch","category","cattle","caught","cause","caution","cave","ceiling","celery","cement","census","century","cereal","certain","chair","chalk","champion","change","chaos","chapter","charge","chase","chat","cheap","check","cheese","chef","cherry","chest","chicken","chief","child","chimney","choice","choose","chronic","chuckle","chunk","churn","cigar","cinnamon","circle","citizen","city","civil","claim","clap","clarify","claw","clay","clean","clerk","clever","click","client","cliff","climb","clinic","clip","clock","clog","close","cloth","cloud","clown","club","clump","cluster","clutch","coach","coast","coconut","code","coffee","coil","coin","collect","color","column","combine","come","comfort","comic","common","company","concert","conduct","confirm","congress","connect","consider","control","convince","cook","cool","copper","copy","coral","core","corn","correct","cost","cotton","couch","country","couple","course","cousin","cover","coyote","crack","cradle","craft","cram","crane","crash","crater","crawl","crazy","cream","credit","creek","crew","cricket","crime","crisp","critic","crop","cross","crouch","crowd","crucial","cruel","cruise","crumble","crunch","crush","cry","crystal","cube","culture","cup","cupboard","curious","current","curtain","curve","cushion","custom","cute","cycle","dad","damage","damp","dance","danger","daring","dash","daughter","dawn","day","deal","debate","debris","decade","december","decide","decline","decorate","decrease","deer","defense","define","defy","degree","delay","deliver","demand","demise","denial","dentist","deny","depart","depend","deposit","depth","deputy","derive","describe","desert","design","desk","despair","destroy","detail","detect","develop","device","devote","diagram","dial","diamond","diary","dice","diesel","diet","differ","digital","dignity","dilemma","dinner","dinosaur","direct","dirt","disagree","discover","disease","dish","dismiss","disorder","display","distance","divert","divide","divorce","dizzy","doctor","document","dog","doll","dolphin","domain","donate","donkey","donor","door","dose","double","dove","draft","dragon","drama","drastic","draw","dream","dress","drift","drill","drink","drip","drive","drop","drum","dry","duck","dumb","dune","during","dust","dutch","duty","dwarf","dynamic","eager","eagle","early","earn","earth","easily","east","easy","echo","ecology","economy","edge","edit","educate","effort","egg","eight","either","elbow","elder","electric","elegant","element","elephant","elevator","elite","else","embark","embody","embrace","emerge","emotion","employ","empower","empty","enable","enact","end","endless","endorse","enemy","energy","enforce","engage","engine","enhance","enjoy","enlist","enough","enrich","enroll","ensure","enter","entire","entry","envelope","episode","equal","equip","era","erase","erode","erosion","error","erupt","escape","essay","essence","estate","eternal","ethics","evidence","evil","evoke","evolve","exact","example","excess","exchange","excite","exclude","excuse","execute","exercise","exhaust","exhibit","exile","exist","exit","exotic","expand","expect","expire","explain","expose","express","extend","extra","eye","eyebrow","fabric","face","faculty","fade","faint","faith","fall","false","fame","family","famous","fan","fancy","fantasy","farm","fashion","fat","fatal","father","fatigue","fault","favorite","feature","february","federal","fee","feed","feel","female","fence","festival","fetch","fever","few","fiber","fiction","field","figure","file","film","filter","final","find","fine","finger","finish","fire","firm","first","fiscal","fish","fit","fitness","fix","flag","flame","flash","flat","flavor","flee","flight","flip","float","flock","floor","flower","fluid","flush","fly","foam","focus","fog","foil","fold","follow","food","foot","force","forest","forget","fork","fortune","forum","forward","fossil","foster","found","fox","fragile","frame","frequent","fresh","friend","fringe","frog","front","frost","frown","frozen","fruit","fuel","fun","funny","furnace","fury","future","gadget","gain","galaxy","gallery","game","gap","garage","garbage","garden","garlic","garment","gas","gasp","gate","gather","gauge","gaze","general","genius","genre","gentle","genuine","gesture","ghost","giant","gift","giggle","ginger","giraffe","girl","give","glad","glance","glare","glass","glide","glimpse","globe","gloom","glory","glove","glow","glue","goat","goddess","gold","good","goose","gorilla","gospel","gossip","govern","gown","grab","grace","grain","grant","grape","grass","gravity","great","green","grid","grief","grit","grocery","group","grow","grunt","guard","guess","guide","guilt","guitar","gun","gym","habit","hair","half","hammer","hamster","hand","happy","harbor","hard","harsh","harvest","hat","have","hawk","hazard","head","health","heart","heavy","hedgehog","height","hello","helmet","help","hen","hero","hidden","high","hill","hint","hip","hire","history","hobby","hockey","hold","hole","holiday","hollow","home","honey","hood","hope","horn","horror","horse","hospital","host","hotel","hour","hover","hub","huge","human","humble","humor","hundred","hungry","hunt","hurdle","hurry","hurt","husband","hybrid","ice","icon","idea","identify","idle","ignore","ill","illegal","illness","image","imitate","immense","immune","impact","impose","improve","impulse","inch","include","income","increase","index","indicate","indoor","industry","infant","inflict","inform","inhale","inherit","initial","inject","injury","inmate","inner","innocent","input","inquiry","insane","insect","inside","inspire","install","intact","interest","into","invest","invite","involve","iron","island","isolate","issue","item","ivory","jacket","jaguar","jar","jazz","jealous","jeans","jelly","jewel","job","join","joke","journey","joy","judge","juice","jump","jungle","junior","junk","just","kangaroo","keen","keep","ketchup","key","kick","kid","kidney","kind","kingdom","kiss","kit","kitchen","kite","kitten","kiwi","knee","knife","knock","know","lab","label","labor","ladder","lady","lake","lamp","language","laptop","large","later","latin","laugh","laundry","lava","law","lawn","lawsuit","layer","lazy","leader","leaf","learn","leave","lecture","left","leg","legal","legend","leisure","lemon","lend","length","lens","leopard","lesson","letter","level","liar","liberty","library","license","life","lift","light","like","limb","limit","link","lion","liquid","list","little","live","lizard","load","loan","lobster","local","lock","logic","lonely","long","loop","lottery","loud","lounge","love","loyal","lucky","luggage","lumber","lunar","lunch","luxury","lyrics","machine","mad","magic","magnet","maid","mail","main","major","make","mammal","man","manage","mandate","mango","mansion","manual","maple","marble","march","margin","marine","market","marriage","mask","mass","master","match","material","math","matrix","matter","maximum","maze","meadow","mean","measure","meat","mechanic","medal","media","melody","melt","member","memory","mention","menu","mercy","merge","merit","merry","mesh","message","metal","method","middle","midnight","milk","million","mimic","mind","minimum","minor","minute","miracle","mirror","misery","miss","mistake","mix","mixed","mixture","mobile","model","modify","mom","moment","monitor","monkey","monster","month","moon","moral","more","morning","mosquito","mother","motion","motor","mountain","mouse","move","movie","much","muffin","mule","multiply","muscle","museum","mushroom","music","must","mutual","myself","mystery","myth","naive","name","napkin","narrow","nasty","nation","nature","near","neck","need","negative","neglect","neither","nephew","nerve","nest","net","network","neutral","never","news","next","nice","night","noble","noise","nominee","noodle","normal","north","nose","notable","note","nothing","notice","novel","now","nuclear","number","nurse","nut","oak","obey","object","oblige","obscure","observe","obtain","obvious","occur","ocean","october","odor","off","offer","office","often","oil","okay","old","olive","olympic","omit","once","one","onion","online","only","open","opera","opinion","oppose","option","orange","orbit","orchard","order","ordinary","organ","orient","original","orphan","ostrich","other","outdoor","outer","output","outside","oval","oven","over","own","owner","oxygen","oyster","ozone","pact","paddle","page","pair","palace","palm","panda","panel","panic","panther","paper","parade","parent","park","parrot","party","pass","patch","path","patient","patrol","pattern","pause","pave","payment","peace","peanut","pear","peasant","pelican","pen","penalty","pencil","people","pepper","perfect","permit","person","pet","phone","photo","phrase","physical","piano","picnic","picture","piece","pig","pigeon","pill","pilot","pink","pioneer","pipe","pistol","pitch","pizza","place","planet","plastic","plate","play","please","pledge","pluck","plug","plunge","poem","poet","point","polar","pole","police","pond","pony","pool","popular","portion","position","possible","post","potato","pottery","poverty","powder","power","practice","praise","predict","prefer","prepare","present","pretty","prevent","price","pride","primary","print","priority","prison","private","prize","problem","process","produce","profit","program","project","promote","proof","property","prosper","protect","proud","provide","public","pudding","pull","pulp","pulse","pumpkin","punch","pupil","puppy","purchase","purity","purpose","purse","push","put","puzzle","pyramid","quality","quantum","quarter","question","quick","quit","quiz","quote","rabbit","raccoon","race","rack","radar","radio","rail","rain","raise","rally","ramp","ranch","random","range","rapid","rare","rate","rather","raven","raw","razor","ready","real","reason","rebel","rebuild","recall","receive","recipe","record","recycle","reduce","reflect","reform","refuse","region","regret","regular","reject","relax","release","relief","rely","remain","remember","remind","remove","render","renew","rent","reopen","repair","repeat","replace","report","require","rescue","resemble","resist","resource","response","result","retire","retreat","return","reunion","reveal","review","reward","rhythm","rib","ribbon","rice","rich","ride","ridge","rifle","right","rigid","ring","riot","ripple","risk","ritual","rival","river","road","roast","robot","robust","rocket","romance","roof","rookie","room","rose","rotate","rough","round","route","royal","rubber","rude","rug","rule","run","runway","rural","sad","saddle","sadness","safe","sail","salad","salmon","salon","salt","salute","same","sample","sand","satisfy","satoshi","sauce","sausage","save","say","scale","scan","scare","scatter","scene","scheme","school","science","scissors","scorpion","scout","scrap","screen","script","scrub","sea","search","season","seat","second","secret","section","security","seed","seek","segment","select","sell","seminar","senior","sense","sentence","series","service","session","settle","setup","seven","shadow","shaft","shallow","share","shed","shell","sheriff","shield","shift","shine","ship","shiver","shock","shoe","shoot","shop","short","shoulder","shove","shrimp","shrug","shuffle","shy","sibling","sick","side","siege","sight","sign","silent","silk","silly","silver","similar","simple","since","sing","siren","sister","situate","six","size","skate","sketch","ski","skill","skin","skirt","skull","slab","slam","sleep","slender","slice","slide","slight","slim","slogan","slot","slow","slush","small","smart","smile","smoke","smooth","snack","snake","snap","sniff","snow","soap","soccer","social","sock","soda","soft","solar","soldier","solid","solution","solve","someone","song","soon","sorry","sort","soul","sound","soup","source","south","space","spare","spatial","spawn","speak","special","speed","spell","spend","sphere","spice","spider","spike","spin","spirit","split","spoil","sponsor","spoon","sport","spot","spray","spread","spring","spy","square","squeeze","squirrel","stable","stadium","staff","stage","stairs","stamp","stand","start","state","stay","steak","steel","stem","step","stereo","stick","still","sting","stock","stomach","stone","stool","story","stove","strategy","street","strike","strong","struggle","student","stuff","stumble","style","subject","submit","subway","success","such","sudden","suffer","sugar","suggest","suit","summer","sun","sunny","sunset","super","supply","supreme","sure","surface","surge","surprise","surround","survey","suspect","sustain","swallow","swamp","swap","swarm","swear","sweet","swift","swim","swing","switch","sword","symbol","symptom","syrup","system","table","tackle","tag","tail","talent","talk","tank","tape","target","task","taste","tattoo","taxi","teach","team","tell","ten","tenant","tennis","tent","term","test","text","thank","that","theme","then","theory","there","they","thing","this","thought","three","thrive","throw","thumb","thunder","ticket","tide","tiger","tilt","timber","time","tiny","tip","tired","tissue","title","toast","tobacco","today","toddler","toe","together","toilet","token","tomato","tomorrow","tone","tongue","tonight","tool","tooth","top","topic","topple","torch","tornado","tortoise","toss","total","tourist","toward","tower","town","toy","track","trade","traffic","tragic","train","transfer","trap","trash","travel","tray","treat","tree","trend","trial","tribe","trick","trigger","trim","trip","trophy","trouble","truck","true","truly","trumpet","trust","truth","try","tube","tuition","tumble","tuna","tunnel","turkey","turn","turtle","twelve","twenty","twice","twin","twist","two","type","typical","ugly","umbrella","unable","unaware","uncle","uncover","under","undo","unfair","unfold","unhappy","uniform","unique","unit","universe","unknown","unlock","until","unusual","unveil","update","upgrade","uphold","upon","upper","upset","urban","urge","usage","use","used","useful","useless","usual","utility","vacant","vacuum","vague","valid","valley","valve","van","vanish","vapor","various","vast","vault","vehicle","velvet","vendor","venture","venue","verb","verify","version","very","vessel","veteran","viable","vibrant","vicious","victory","video","view","village","vintage","violin","virtual","virus","visa","visit","visual","vital","vivid","vocal","voice","void","volcano","volume","vote","voyage","wage","wagon","wait","walk","wall","walnut","want","warfare","warm","warrior","wash","wasp","waste","water","wave","way","wealth","weapon","wear","weasel","weather","web","wedding","weekend","weird","welcome","west","wet","whale","what","wheat","wheel","when","where","whip","whisper","wide","width","wife","wild","will","win","window","wine","wing","wink","winner","winter","wire","wisdom","wise","wish","witness","wolf","woman","wonder","wood","wool","word","work","world","worry","worth","wrap","wreck","wrestle","wrist","write","wrong","yard","year","yellow","you","young","youth","zebra","zero","zone","zoo"]
        self.akiObj = Akinator()
        self.gameCache = {}
        self.color = 0x2F3136
        self.session = ClientSession()
        self.sp = _Spotify(auth_manager=SpotifyClientCredentials(client_id=environ["SP_ID"], client_secret=environ["SP_SECRET"]))
        self.collection = MongoClient(environ["MONGODB_URL"])["Coins"]["Points/others"]
        self.goodmessages = ["Wow speedy!", "Nice time!", "That was pretty good!", "Wow, you fast at typing!", "You speedy, that's for sure!"]
        self.badmessages = ["How slow can you type?", "That was slow!", "You need to practice more!", "It's ok i won't tell anybody that your a slow typer"]
        self.aliaresponses = [
            "Ali A Kills Himself",
            "Ali A Ignores And Hits A 360 Noscope",
            "Ali A Approves",
            "Ali A Dosnt Approve"
        ]
        self.hearts = ['💔', '💝', '💚', '💙', '💜']

    @commands.command(help="World can make you laugh with his amazing jokes!")
    async def joke(self, ctx):
        headers = {"Accept": "application/json"}
        req = await self.session.get("https://icanhazdadjoke.com", headers=headers)
        r = await req.json()
        embed = Embed(title="Epic joke!",description=r["joke"], color=self.color)
        await ctx.send(embed=embed)

    @commands.command(help="Ask Alister-A a question!")
    async def askali(self, ctx, *, question):
        await ctx.send(embed=Embed(title="Ask Alister-A", description=f"{ctx.author.mention} - {choice(self.aliaresponses)}", color=self.color).set_thumbnail(url="https://tenor.com/view/ali-a-hue-funny-dance-gif-12395829"))

    @askali.error
    async def askali_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/askali <question>`")


    @commands.command(name="f", help="Give respects.")
    async def f(self, ctx, *, text: commands.clean_content = None):
        reason = f"for **{text}** " if text else ""
        await ctx.send(embed=Embed(title = f"**{ctx.author.name}** has paid their respect {reason}{choice(self.hearts)}", color=self.color))

    @commands.command(help="Shows a meme from random subreddits.")
    @commands.cooldown(rate=4, per=7, type=commands.BucketType.member)
    async def meme(self, ctx):
        r = await self.session.get(f"https://memes.blademaker.tv/api?lang=en")
        res = await r.json()
        embed = Embed(title=f"Title: {res['title']}\nSubreddit: r/{res['subreddit']}", color=self.color).set_image(url=res["image"]).set_footer(text=f"👍Ups:{res['ups']}")
        await ctx.send(embed=embed)

    @meme.error
    async def meme_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            a = error.retry_after
            a = round(a)
            await ctx.send(f"Sorry {ctx.author.mention} This command in on cooldown, Try again in {a} seconds.")

    @commands.command(help="Enlarge a discord emoji!")
    async def enlarge(self, ctx, emoji: PartialEmoji):
    	embed = Embed(title="Enlarge", description=f"`{emoji.name}` was enlarged.", color=self.color).set_image(url=emoji.url)
    	await ctx.send(embed=embed)

    @enlarge.error
    async def enlarge_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/enlarge <emoji>`")
        if isinstance(error, commands.PartialEmojiConversionFailure):
            await ctx.send(f"Sorry {ctx.author.mention} that emoji was not found!")


    @commands.command(aliases=["pepe"], help="Shows users pp size.")
    async def pp(self, ctx, *, user: Member = None):
        if user is None:
            user = ctx.author
        size = randint(1, 15)
        dong = ""
        for _i in range(0, size):
            dong += "="
        embed = Embed(title=f"{user}'s pepe size", description=f"8{dong}D", color=self.color)
        await ctx.send(embed=embed)

    @commands.command(help="Steal a users avatar.", aliases=["av"])
    async def avatar(self, ctx, *, user: Member=None):
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
        embed = Embed(color=self.color).set_image(url=res["message"])
        await ctx.send(embed=embed)
        await r.close(close_session=False)

    @tweet.error
    async def tweet_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/tweet <username> <message>`")

    @commands.command(help="Is that user gay?.")
    async def gay(self, ctx, *, user: Member=None):
        user = user or (ctx.author)
        randomPercentage = randint(1, 100)
        embed = Embed(title="Gayrate!", description=f"**{user}** is {randomPercentage}% gay", color=self.color).set_thumbnail(url=user.avatar_url)
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

        gameObj = await self.akiObj.start_game(child_mode=True)

        currentChannel = ctx.channel

        self.gameCache.update(
            {ctx.channel.id: {
                "user": ctx.author,
                "channel": ctx.channel.id
            }})

        while self.akiObj.progression <= 80:
            try:
                message1 = await ctx.send(embed=Embed(title="Question", description=gameObj, color=self.color))
                resp = await ctx.bot.wait_for("message", check=lambda message: message.author == ctx.author and message.channel == ctx.channel and message.guild == ctx.guild and message.content.lower(), timeout=15)
            except:
                await ctx.send(embed=Embed(title="Hurry next time!", description=f"{ctx.author.mention} took too long to respond so we ended the game\nCurrent timeout: `15` Seconds.", color=self.color))
                del self.gameCache[ctx.channel.id]
                return await message1.delete(delay=None)
            if resp.content == "b":
                try:
                    gameObj = await self.akiObj.back()
                except:
                    await ctx.send(embed=Embed(title="Cannot go back any further :(",description="Continue playing anyway", color=self.color))
            elif resp.content == "q" or resp.content == "quit":
                await ctx.send(embed=Embed(title="Game over", description="You have left the game.", color=self.color))
                del self.gameCache[ctx.channel.id]
                break
            else:
                try:
                    gameObj = await self.akiObj.answer(resp.content)
                except:
                    del self.gameCache[ctx.channel.id]
                    return await ctx.send(embed=Embed(title="Invalid Answer", description="You typed a invalid answer the only answer options are:\n`y` OR `yes` for yes\n`n` OR `no` for no\n`i` OR `idk` for i dont know\n`p` OR `probably` for probably\n`pn` OR `probably not` for probably not\n`b` for back\n`q` or `quit` for stop the game", color=self.color))

        await self.akiObj.win()

        embed = Embed(title="I have outsmarted your outsmarting", color=self.color).add_field(name="I think...", value="it is {0.first_guess[name]} {0.first_guess[description]}?\n\nSorry if im wrong, Akinator has tried.".format(akiObj)).set_image(url=self.akiObj.first_guess['absolute_picture_path'])

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
        await ctx.send(embed=embed)

    @_8ball.error
    async def _8ball_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/8ball <question>`")

    @commands.command(help="Turn text into emojis!.")
    async def emojify(self, ctx, *, stuff):
        if len(stuff) > 20:
            return await ctx.send(f"Sorry {ctx.author.mention} a limit of `20` chars please!")
        emj = ("".join([":regional_indicator_"+l+":"  if l in "abcdefghijklmnopqrstuvwyx" else [":zero:", ":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:", ":nine:"][int(l)] if l.isdigit() else ":question:" if l == "?" else ":exclamation:" if l == "!" else l for l in stuff.lower()]))
        embed = Embed(title='Emojify', description=f'{emj}', color=self.color)
        await ctx.send(embed=embed)

    @emojify.error
    async def emojify_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/emojify <text>`")

    @commands.command(help="Kill a user")
    async def kill(self, ctx, user: Member):
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
        embed = Embed(title="Murder", description=f"{ctx.author.mention} you killed {user.mention} because {choice(kills)}", color=self.color)
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

            embed = Embed(title=res['word'], description=res['definition'], color=self.color).add_field(name="Example", value=res['example']).set_footer(text=f"👍 {res['thumbs_up']} | 👎{res['thumbs_down']}")
            await ctx.send(embed=embed)

    @urban.error
    async def urban_error(self, ctx, error):
        if isinstance(error, commands.errors.NSFWChannelRequired):
            embed = Embed(title="NSFW", description=f"Sorry {ctx.author.mention} but this command is nsfw and this is not a nsfw channel.", color=self.color).set_image(url="https://media.discordapp.net/attachments/265156286406983680/728328135942340699/nsfw.gif")
            return await ctx.send(embed=embed)

    @commands.command(help="Advice from world.")
    async def advice(self, ctx):
        r = await self.session.get(f"https://api.adviceslip.com/advice", headers={"Accept": "application/json"})
        res = await r.json(content_type="text/html")
        embed = Embed(title="Advice", description=f"{res['slip']['advice']}", color=self.color)
        await ctx.send(embed=embed)

    @commands.command(help="Generate qr code")
    async def qr(self, ctx, *, text):
        embed = Embed(title="Qr code", description=f"Generated `{text}`", color=self.color).set_image(url=f"http://api.qrserver.com/v1/create-qr-code/?data={quote(text)}&margin=25")
        await ctx.send(embed=embed)

    @qr.error
    async def qr_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/qr <text>`")

    @commands.command(help="This command will show you a cute duck", aliases=['quack', 'duk'])
    async def duck(self, ctx):
        r = await self.session.get('https://random-d.uk/api/v2/random')
        res = await r.json()
        embed = Embed(title='Quack!', color=self.color).set_image(url=res['url'])
        await ctx.send(embed=embed)

    @commands.command(help="Flip a users avatar!", aliases=["flipav", "avflip"])
    async def flip(self, ctx, user: Member=None):
        user = user or ctx.author

        av_img = await Misc.fetch_pfp(user)
        done = av_img.rotate(180)
        await ctx.send(file=Misc.save_image(done))


    @commands.command(help="Blur a users avatar!")
    async def blur(self, ctx, user: Member=None):
        user = user or ctx.author

        av_img = await Misc.fetch_pfp(user)
        done = av_img.filter(ImageFilter.GaussianBlur(radius=8))
        await ctx.send(file=Misc.save_image(done))

    @commands.command(hlep="Generate a fake discord message!", aliases=["fq", "fakeq", "fakemessage", "fakemsg"])
    async def fakequote(self, ctx, user: Optional[Member], *, message) -> None:
        now = datetime.now()
        user = user or ctx.author

        font = ImageFont.truetype("fonts/Whitney-Medium.ttf", 22, encoding="unic")
        fontsmall = ImageFont.truetype("fonts/Whitney-Medium.ttf", 16, encoding="unic")
        fontnormal = ImageFont.truetype("fonts/Whitney-Medium.ttf", 20, encoding="unic")
        fontchannel = ImageFont.truetype("fonts/Whitney-Medium.ttf", 16, encoding="unic")

        userchar = font.getsize(user.name)[0]
        color = (255, 255, 255) if (Misc.hex_to_rgb(str(user.color)) == (0, 0, 0)) else Misc.hex_to_rgb(str(user.color))

        image = Image.open("images/fake.png")

        msg = message if len(message) <= 30 else f'{message[0:38]}...'

        parser = TwemojiParser(image, parse_discord_emoji=True)
        await Misc.parser_draw_text(parser, user.name, font, color, 80, 30)
        await Misc.parser_draw_text(parser, str(now.strftime("Today at %H:%M")), fontsmall, 'grey', 80 + userchar + 8, 33)
        await Misc.parser_draw_text(parser, msg, fontnormal, (220,221,222), 80, 57)
        await parser.close()

        CONVERT = await Misc.circle_pfp(user, 50, 50)
        image.paste(CONVERT, (20, 30), CONVERT)
        await ctx.send(file=Misc.save_image(image))

    @fakequote.error
    async def fakequote_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/fakequote <user> <text>`")

    @commands.command(help="Write a top.gg Review", aliases=["tgg", "topggreview", "topggbotreview", "botreview"])
    async def topgg(self, ctx, user: Optional[Member], *, message):
        user = user or ctx.author
        if len(message) > 30:
            return await ctx.send(f"Sorry {ctx.author.mention} there is a limit of `30` chars.")

        ran_days = randint(2, 30)

        font = ImageFont.truetype("fonts/karla1.ttf", 19, encoding="unic")
        fontsmall = ImageFont.truetype("fonts/karla1.ttf", 15, encoding="unic")
        fontnormal = ImageFont.truetype("fonts/karla1.ttf", 18, encoding="unic")

        userchars = font.getsize(user.name)[0]

        mainimage = Image.open("images/tgg.png")

        parser = TwemojiParser(mainimage, parse_discord_emoji=True)
        await Misc.parser_draw_text(parser, user.name, font, 'black', 126, 43)
        await Misc.parser_draw_text(parser, f"{ran_days} days ago", fontsmall, 'grey', 132 + userchars + 2, 47)
        await Misc.parser_draw_text(parser, message, font, 'black', 129, 84)
        await parser.close()

        CONVERT = await Misc.circle_pfp(user, 41, 41)
        mainimage.paste(CONVERT, (62, 46), CONVERT)
        await ctx.send(file=Misc.save_image(mainimage))

    @topgg.error
    async def topgg_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Sorry {ctx.author.mention} Please Type `w/topgg <user> <text>`")

    @commands.command(help="Widen a discord avatar!", aliases=["widen", "putin", "wideputin"])
    async def wide(self, ctx, user: Member=None):
        user = user or ctx.author
        av_img = await Misc.fetch_pfp(user)
        await ctx.send(file=Misc.save_image(av_img.resize((350, 180))))

    @commands.command(help="Show what you are listening to in a photo!\nYou can also use `w/spotify --artist <artist>` and `w/spotify --song <song>` to find out information about a artist or song.", aliases=["sp"])
    @commands.cooldown(rate=2, per=8, type=commands.BucketType.member)
    async def spotify(self, ctx, user: Optional[Member], option: Optional[str], *, song: Optional[str]):
        if option == "--artist":
        	if not song:
        		return await ctx.send(f"Sorry {ctx.author.mention} please specify a artist's name!")

        	results = self.sp.search(q=song, limit=1, type='artist')
        	for track in self.sp.search(q=song, limit=1, type='artist'):
        		items = results['artists']['items']

        		try:
        			artist = items[0]
        		except IndexError:
        			return await ctx.send(f"Sorry {ctx.author.mention} but that artist does not exist!")

        		embed = Embed(title=artist['name'], color=self.color).add_field(name="Artist information", value=f"Followers: `{artist['followers']['total']:,}`\nPopularity: `{artist['popularity']}%`\nArtist Link: [`{artist['name']}`](https://open.spotify.com/artist/{artist['id']})").set_thumbnail(url=artist['images'][0]['url'])
        		return await ctx.send(embed=embed)

        if option == "--song":
        	if not song:
        		return await ctx.send(f"Sorry {ctx.author.mention} Please specify a song name!")

        	results = self.sp.search(q=song, limit=1, type='track')
        	for track in results:
        		items = results['tracks']['items']

        		try:
        			song = items[0]
        			spotify = results['tracks']['items'][0]
        			name = ', '.join([artist['name'] for artist in spotify['artists']])
        		except IndexError:
        			return await ctx.send(f"Sorry {ctx.author.mention} but that artist does not exist!")

        		embed = Embed(title=song['name'], color=self.color).add_field(name="Song information", value=f"Artist(s): `{name}`\nPopularity: `{song['popularity']}%`\nRelease date: `{spotify['album']['release_date']}`\nSong Link: [`{song['name']}`](https://open.spotify.com/track/{song['id']})").set_thumbnail(url=spotify['album']['images'][0]['url'])
        		return await ctx.send(embed=embed)
        try:
        	user = user or ctx.author
        	spotify_activity = next(
        		(activity for activity in user.activities if isinstance(activity, Spotify)),
        		None
        		)

        	if spotify_activity is None:
        		return await ctx.send(f"Sorry {ctx.author.mention} {user.name} is not currently listening to Spotify.")

        	r = await self.session.get(str(spotify_activity.album_cover_url))
        	res = BytesIO(await r.read())
        	r.close()

        	color_thief = ColorThief(res)
        	dominant_color = color_thief.get_color(quality=40)

        	font = ImageFont.truetype("fonts/spotify.ttf", 42, encoding="unic")
        	fontbold = ImageFont.truetype("fonts/spotify-bold.ttf", 53, encoding="unic")

        	title = self.kks.convert(spotify_activity.title)
        	album = self.kks.convert(spotify_activity.album)
        	artists = self.kks.convert(spotify_activity.artists)

        	title_new = ''.join(item['hepburn'] for item in title)
        	album_new = ''.join(item['hepburn'] for item in album)
        	transliterated_artists = [self.kks.convert(artist) for artist in spotify_activity.artists]
        	artists_new = ', '.join(''.join(item['hepburn'] for item in artist) for artist in transliterated_artists)

        	abridged = album_new if len(album_new) <= 30 else f'{album_new[0:27]}...'
        	cbridged = title_new if len(title_new) <= 20 else f'{title_new[0:17]}...'
        	dbridged = artists_new if len(artists_new) <= 30 else f'{artists_new[0:27]}...'

        	luminance = Misc.relative_luminance(dominant_color)

        	text_colour = 'black' if luminance > 0.5 else 'white'

        	img = Image.new('RGB', (999, 395), color=dominant_color)

        	album = Image.open(res)
        	resized_album = album.resize((245, 245))
        	img.paste(resized_album, (41, 76))

        	parser = TwemojiParser(img, parse_discord_emoji=False)
        	await Misc.parser_draw_text(parser, cbridged, fontbold, text_colour, 300, 90) # Top section - Song name
        	await Misc.parser_draw_text(parser, dbridged, font, text_colour, 303, 170) # Middle secion - Artists of the song
        	await Misc.parser_draw_text(parser, abridged, font, text_colour, 303, 228) # Album name - Bottom section
        	await parser.close()
        	await ctx.send(file=Misc.save_image(Misc.add_corners(img, 42)))
        except Exception as e:
        	return await ctx.send(e)

    @spotify.error
    async def spotify_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            a = error.retry_after
            a = round(a)
            await ctx.send(f"Sorry {ctx.author.mention} This command in on cooldown, Try again in {a} seconds.")


    @commands.command(help="Are you a fast typer?!\nUse `w/fast --rank` to see rank.", aliases=["type", "typingtest"])
    @commands.cooldown(rate=3, per=8, type=commands.BucketType.member)
    async def fast(self, ctx, option: Optional[str], user: Optional[Member]=None):
        user = user or ctx.author
        if option in ["--rank", "rank"]:
            if not (Misc._has_account(user.id)):
                return await ctx.send(f"Sorry {ctx.author.mention} that user is not ranked yet.")
                
            img = Image.new('RGB', (1000, 300), color=(35, 39, 42))

            font = ImageFont.truetype("fonts/Whitney-Medium.ttf", 65, encoding="unic")
            fontsmall = ImageFont.truetype("fonts/Whitney-Medium.ttf", 49, encoding="unic")

            result = self.collection.find_one({"_id": user.id})
            user_points = result['points']

            rank = self.collection.find({"points":{"$gt":user_points}}).count() + 1

            CONVERT = await Misc.circle_pfp(user, 180, 180)

            if Misc.hex_to_rgb(str(user.color)) == (0, 0, 0):
                color = (255, 255, 255)
            else:
                color = Misc.hex_to_rgb(str(user.color))

            name = user.name if len(user.name) <= 16 else f'{user.name[0:13]}...'

            result = self.collection.find_one({"_id": user.id})
            user_points = result['points']

            parser = TwemojiParser(img)
            await Misc.parser_draw_text(parser, name, font, color, 249, 69) # Name of author
            await Misc.parser_draw_text(parser, f"Global rank: #{rank}, Points: {user_points:,}", fontsmall, 'white', 250, 160) # Current rank, and points
            await parser.close()

            img.paste(CONVERT, (50, 67), CONVERT)
            return await ctx.send(file=Misc.save_image(img))
        
        word = choice(self.words)

        font = ImageFont.truetype("fonts/Arial-bold.ttf", 25, encoding="unic")

        wx, wy = font.getsize(word)
        offset_y = font.getsize(word)[1]
        height = offset_y + wy

        img = Image.new('RGB', (wx+30, height), color='lightblue')

        imgdraw = ImageDraw.Draw(img)
        imgdraw.text((14, 9), word, fill='black', font=font)
        game = await ctx.send(file=Misc.save_image(img))

        while True:
            try:
                start = round(time() * 100)
                resp = await self.bot.wait_for("message", check=lambda message: message.channel == ctx.channel and message.guild == ctx.guild and message.content.lower() == word, timeout=18)
                elapse = round(time() * 100) - start
                if resp.content.lower() == word:
                    if not (Misc._has_account(resp.author.id)):
                        await Misc._insert_to_collection(resp.author.id)
                    if elapse/1000 > 6:
                        isfast = choice(self.badmessages)
                        random_points = randint(10, 45)
                        Misc.give_points(resp.author.id, random_points)
                    else:
                        isfast = choice(self.goodmessages)
                        random_points = randint(5, 17)
                        Misc.give_points(resp.author.id, random_points)
                    embed = Embed(title="Fastest typer!",description=f"{resp.author.mention} typed the word `{word}` first, also has earned `{random_points}` Points.", color=self.color).add_field(name=":alarm_clock: | Time information", value=f"Time took in milliseconds: `{elapse}ms`\nTime took in seconds: `{elapse/1000}s`").add_field(name="<:Worldcool:768201555492864030> | Message from World", value=f"{isfast}", inline=False)
                    return await ctx.send(embed=embed)
            except:
                await game.delete()
                return await ctx.send(f"Sorry {ctx.author.mention} nobody took part! So i have ended the game.")

    @commands.command(help="Mock some text.")
    async def mock(self, ctx, *, text) -> None:
        if not text:
            return await ctx.send(f"Sorry {ctx.author.mention} you forgot to add some text for me to mock.")
        " ".join(text)
        return await ctx.send("".join([choice([index.lower(), index.upper()]) for index in list(text)]))

    @fast.error
    async def fast_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            a = error.retry_after
            a = round(a)
            await ctx.send(f"Sorry {ctx.author.mention} This command in on cooldown, Try again in {a} seconds.")

    @commands.command(help="Guess the flag from the picture!!", aliases=["gtf"])
    async def guesstheflag(self, ctx):
    	FlagChosen = choice(self.Country)

    	req = await self.session.get(f"https://www.countryflags.io/{FlagChosen['code'].lower()}/flat/64.png")
    	if req.status != 200:
    		return await ctx.send(f"Sorry {ctx.author.mention} The api is down.")
    	req.close()

    	embed = Embed(title="Guess the flag!", color=self.color).set_image(url=f"https://www.countryflags.io/{FlagChosen['code'].lower()}/flat/64.png")
    	FirstMessage = await ctx.send(embed=embed)


    	while True:
    		try:
    			start = round(time() * 100)
    			resp = await self.bot.wait_for("message", check=lambda message: message.channel == ctx.channel and message.guild == ctx.guild and message.content == FlagChosen['name'], timeout=18)
    			elapse = round(time() * 100) - start
    			if resp.content.lower() == FlagChosen['name'].lower():
    				if not Wealth._has_account(resp.author.id):
    					Wealth._create_account(resp.author.id)
    				RandomCoins = randint(15, 60)
    				Wealth.give_coins(resp.author.id, RandomCoins)
    				embed = Embed(title="Guess the flag", description=f"{resp.author.mention} guessed the country right!\nThe country was `{FlagChosen['name']}`\nTime took: `{elapse/1000}s`\nCoins earned: `{RandomCoins}`", color=self.color)
    				return await ctx.send(embed=embed)
    		except TimeoutError:
    			await FirstMessage.delete()
    			return await ctx.send(f"Sorry {ctx.author.mention} nobody guessed the flag! It was: `{FlagChosen['name']}`")
def setup(bot):
    bot.add_cog(FunCog(bot))
