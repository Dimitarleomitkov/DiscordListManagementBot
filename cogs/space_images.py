import discord
import requests
import json
import datetime
import dateutil.tz as dateutils
from discord.ext import commands, tasks


# If no tzinfo is given then UTC is assumed.
BG_time_zone = dateutils.tzoffset('UTC', 60 * 60 * 2)
time = datetime.time(hour = 8,\
                     minute = 00,\
                     second = 15,\
                     tzinfo = BG_time_zone)


async def setup(bot):
    await bot.add_cog(space_images(bot))


class space_images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    def get_space_img(self):
        response = requests.get("https://go-apod.herokuapp.com/apod")
        json_data = json.loads(response.text)
        space_img = json_data["hdurl"]

        return space_img


    @tasks.loop(time = time)
    async def good_morning_message(self):
        text_chan = self.bot.get_channel(337156974754136064)
        space_img = self.get_space_img()
        
        await text_chan.send(f"Your daily space image:\n{space_img}")


    @commands.Cog.listener()
    async def on_ready(self):
        print("space_images module is loaded.")
        self.good_morning_message.start()
