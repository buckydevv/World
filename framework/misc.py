from os import environ
from discord import File
from aggdraw import Draw, Brush
from discord.ext import commands
from time import time
from io import BytesIO
from pymongo import MongoClient
from PIL import Image, ImageDraw, ImageOps, ImageColor
from twemoji_parser import TwemojiParser
from colorthief import ColorThief

__import__("dotenv").load_dotenv()

class Misc:
    collection = MongoClient(environ["MONGODB_URL"])["Coins"]["Points/others"]
    _TIME = {
        31536000: "year",
        2592000: "month",
        86400: "day",
        3600: "hour",
        60: "minute"
    }

    def give_points(user_id: int, points: int) -> None:
        """Update a users points."""
        Misc.collection.update_one({"_id": user_id}, {"$inc": {"points": points}}) # $inc increments the number.

    def _has_account(user_id: int) -> None:
        """Returns True if the user has a acoount."""
        return bool(Misc.collection.find_one(
            {"_id": user_id}
        ))

    def _insert_to_collection(user_id: int) -> None:
        """insert user into database"""
        Misc.collection.insert_one({
            "_id": user_id,
            "points": 0
        })

    def add_corners(im, rad):
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

    def round_corner_jpg(image, radius):
        mask = Image.new('L', image.size)
        draw = Draw(mask)
        brush = Brush('white')
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

    async def circle_pfp(author, x: int, y: int):
        pfp = author.avatar_url_as(format='png')
        buffer_avatar = BytesIO()
        await pfp.save(buffer_avatar)
        buffer_avatar.seek(0)
        av_img = Image.open(buffer_avatar)

        resize = av_img.resize((x,y));
        size_bigger = (resize.size[0] * 3, resize.size[1] * 3)
        maskimage = Image.new('L', size_bigger, 0)
        draw = ImageDraw.Draw(maskimage)
        draw.ellipse((0, 0) + size_bigger, fill=255)
        maskimage = maskimage.resize(resize.size, Image.ANTIALIAS)
        resize.putalpha(maskimage)
        output = ImageOps.fit(resize, maskimage.size, centering=(0.5, 0.5))
        output.putalpha(maskimage)
        return resize

    def save_image(image):
        """ Saves a PIL.Image.Image object to a discord.File object. """
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)
        image.close()
        return File(buffer, "image.png")

    async def fetch_pfp(author):
        pfp = author.avatar_url_as(format='png')
        buffer_avatar = BytesIO()
        await pfp.save(buffer_avatar)
        buffer_avatar.seek(0)
        return Image.open(buffer_avatar)
    
    async def image_from_url(bot, url):
        response = await bot.http._HTTPClient__session.get(url) # this is the session discord.py uses
        byte = await response.read()
        return Image.open(BytesIO(byte))
    
    def __delayfstr(string):
        """ Gets time delay from a string with a format of 'MONTH/DAY/YEAR at HOURS:MINUTES:SECONDS' """
        seconds = round(time() - datetime.strptime(string, "%m/%d/%Y at %H:%M:%S").timestamp())
        if seconds < 60:
            return f"{seconds} second" + ("" if (seconds == 1) else "s")
        
        for key in Misc._TIME.keys():
            if seconds >= key:
                seconds //= key
                return f"{seconds} {Misc._TIME[key]}" + ("" if seconds == 1 else "s")
        
        seconds //= 31536000
        return f"{seconds} year" + ("" if seconds == 1 else "s")