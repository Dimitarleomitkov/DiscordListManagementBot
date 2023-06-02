import discord
import requests
import datetime
import re
import pytz
from discord.ext import commands, tasks
from bs4 import BeautifulSoup


# If no tzinfo is given then UTC is assumed.
BG_time_zone = pytz.timezone("Europe/Sofia")
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
                explanation = re.split("Explanation:", paragraph.text)[1]
                explanation = re.split("Tomorrow", explanation)[0]
                explanation = re.sub("\n", " ", explanation).strip(" ")

        # print(type(explanation), explanation)
        data.append(explanation)

        return data


    @commands.command(  name = 'space_image',
                        help = 'The bot show the daily space image from NASA.',
                        brief = '- Shows the daily space image from NASA.')
    async def space_image_cmd(self, ctx):
        try:
            space_img_info = await self.get_space_img()
            explanation = ""
            # print(space_img_info[0], "|", space_img_info[1], "|", space_img_info[2])

            if len(space_img_info[2]) < 1024:
                explanation = space_img_info[2]
            else:
                explanation = "https://apod.nasa.gov/apod/astropix.html"
            
            embed = discord.Embed(title = space_img_info[1])
            embed.set_image(url = space_img_info[0])
            embed.add_field(name = "Description",
                            value = explanation,
                            inline = False)
            
            await ctx.send(embed = embed)
        except Exception as e:
            await ctx.send("[space_images] I broke down again")
            await ctx.send("https://tenor.com/view/serio-no-nop-robot-robot-down-gif-12270251")
            
            text_chan = self.bot.get_channel(548554244932894750)
            await text_chan.send(e)
            
            return
      
    @tasks.loop(time = time)
    async def good_morning_message(self):
        text_chan = self.bot.get_channel(337156974754136064)
        try:
            space_img_info = await self.get_space_img()
            explanation = ""
            # print(space_img_info[0], "|", space_img_info[1], "|", space_img_info[2])

            if len(space_img_info[2]) < 1024:
                explanation = space_img_info[2]
            else:
                explanation = "https://apod.nasa.gov/apod/astropix.html"
            
            embed = discord.Embed(title = space_img_info[1])
            embed.set_image(url = space_img_info[0])
            embed.add_field(name = "Description",
                            value = explanation,
                            inline = False)
            
            await text_chan.send(embed = embed)
        except Exception as e:
            await text_chan.send("[space_images] I broke down again")
            await text_chan.send("https://tenor.com/view/serio-no-nop-robot-robot-down-gif-12270251")
            
            text_chan = self.bot.get_channel(548554244932894750)
            await text_chan.send(e)
            
            return


    @commands.Cog.listener()
    async def on_ready(self):
        print("space_images module is loaded.")
        self.good_morning_message.start()

