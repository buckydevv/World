import discord
import pymongo
import os 
import PIL
import aggdraw
import twemoji_parser 

from os import environ, listdir
from discord import Spotify

from discord.ext import commands
from io import BytesIO
from dotenv import load_dotenv
from pymongo import MongoClient
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps
from twemoji_parser import TwemojiParser
from colorthief import ColorThief

load_dotenv()

cluster = MongoClient(os.environ["MONGODB_URL"])

db = cluster["Coins"]
collection = db["Points/others"]

class Misc:
    def __init__(self):
        self.color = 0x2F3136

    def give_points(user_id: int, points: int) -> None:
        """Update a users points."""
        result = collection.find_one(
            {"_id": user_id}
            )

        oldpoints = result['points']

        collection.update_one({"_id": user_id}, {"$set": {"points": oldpoints + points}})


    def _has_account(user_id: int) -> None:
        """Returns True if the user has a acoount."""
        return bool(collection.find_one(
            {"_id": user_id}
        ))


    def _insert_to_collection(user_id: int) -> None:
        """insert user into database"""
        collection.insert_one({
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

    def hex_to_rgb(value):
        value = value.lstrip('#')
        lv = len(value)
        return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

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

    async def fetch_pfp(author):
    	pfp = author.avatar_url_as(format='png')
    	buffer_avatar = BytesIO()
    	await pfp.save(buffer_avatar)
    	buffer_avatar.seek(0)
    	return buffer_avatar

    async def parser_draw_text(source, text, textfont, color, x: int, y: int):
        output = await source.draw_text((x, y), text, fill=color, font=textfont)
        return output

    def draw_text(source, text, textfont, color, x: int, y: int):
        output = source.draw_text((x, y), text, fill=color, font=textfont)
        return output