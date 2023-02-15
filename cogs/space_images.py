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


    async def get_space_img(self):
        response = requests.get("https://go-apod.herokuapp.com/apod")
        json_data = json.loads(response.text)

        return json_data


    @tasks.loop(time = time)
    async def good_morning_message(self):
        text_chan = self.bot.get_channel(337156974754136064)
        space_img_info = await self.get_space_img()

        embed = discord.Embed(title = space_img_info["title"])
        embed.set_image(url = space_img_info["hdurl"])
        embed.add_field(name = "Descripition",
                        value = space_img_info["explanation"],
                        inline = False)
        
        await text_chan.send(f"Your daily space image:\n", embed = embed)


    @commands.Cog.listener()
    async def on_ready(self):
        print("space_images module is loaded.")
        self.good_morning_message.start()

