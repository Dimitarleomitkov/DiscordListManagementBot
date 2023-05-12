import discord
import requests
import datetime
import dateutil.tz as dateutils
from discord.ext import commands, tasks
from bs4 import BeautifulSoup
import re


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
        response = requests.get("https://apod.nasa.gov/apod/astropix.html")
        soup = BeautifulSoup(response.text, "html.parser")
        list_of_links = soup.find_all('a')

        data = []
        image_links = []

        for link in list_of_links:
            if re.search("image", str(link)) != None:
                image_links.append(re.search("image", str(link)).string)

        image_link = re.split('href="', image_links[0])[1]
        image_link = re.split('"', image_link)[0]

        data.append("https://apod.nasa.gov/apod/" + image_link)

        title = re.split("Image Credit", soup.find_all('center')[1].text)[0]
        title = re.sub("\n", " ", title).strip(" ")

        data.append(title)

        explanation = None

        list_of_ps = soup.find_all('p')

        for paragraph in list_of_ps:
            if re.search("Explanation", paragraph.text) != None:
                explanation = re.split("Tomorrow", paragraph.text)[0]
                explanation = re.sub("\n", " ", explanation).strip(" ")

        data.append(explanation)

        return data


    @commands.command(  name = 'space_image',
                        help = 'The bot show the daily space image from NASA.',
                        brief = '- Shows the daily space image from NASA.')
    async def space_image_cmd(self, ctx):
        space_img_info = await self.get_space_img()
        explanation = ""

        if len(space_img_info[2]) < 1024:
            explanation = space_img_info["explanation"]
        else:
            explanation = "https://apod.nasa.gov/apod/astropix.html"
        
        embed = discord.Embed(title = space_img_info[1])
        embed.set_image(url = space_img_info[0])
        embed.add_field(name = "Description",
                        value = explanation,
                        inline = False)
        
        await ctx.send(embed = embed)
      
    @tasks.loop(time = time)
    async def good_morning_message(self):
        text_chan = self.bot.get_channel(337156974754136064)
        space_img_info = await self.get_space_img()
        explanation = ""
        
        if len(space_img_info["explanation"]) < 1024:
            explanation = space_img_info["explanation"]
        else:
            explanation = "https://go-apod.herokuapp.com/apod"
        
        embed = discord.Embed(title = space_img_info["title"])
        
        if space_img_info["media_type"] == "image":
            embed.set_image(url = space_img_info["hdurl"])
        else:
            explanation = "Not an image. https://go-apod.herokuapp.com/apod"

        embed.add_field(name = "Descripition",
                        value = explanation,
                        inline = False)
        
        await text_chan.send(f"Your daily space imagery from NASA:\n", embed = embed)


    @commands.Cog.listener()
    async def on_ready(self):
        print("space_images module is loaded.")
        self.good_morning_message.start()

