import discord
import requests
import json
from discord.ext import commands

# # If no tzinfo is given then UTC is assumed.
# BG_time_zone = dateutils.tzoffset('UTC', 60 * 60 * 2)
# time = datetime.time(hour = 8,\
#                      minute = 00,\
#                      second = 59,\
#                      tzinfo = BG_time_zone)


async def setup(bot):
    await bot.add_cog(dogs(bot))


class dogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    def get_dog_img(self):
        response = requests.get("https://dog.ceo/api/breeds/image/random")
        json_data = json.loads(response.text)
        dog_img = json_data["message"]

        return dog_img


#     @tasks.loop(time = time)
#     async def good_morning_joke(self):
#         text_chan = self.bot.get_channel(337156974754136064)
#         joke = self.get_joke()
        
#         await text_chan.send(f"Daily joke:\n")
#         if joke["type"] == "single":
#             await ctx.send(f"{joke['joke']}")
#         else:
#             await ctx.send(f"{joke['setup']}\n{joke['delivery']}")



    @commands.Cog.listener()
    async def on_ready(self):
        print("dogs module is loaded.")

    @commands.command(  name = 'rdog',
                        help = 'The bot will get a random dog picture.',
                        brief = '- Gets a random dog picture.')
    async def dogs(self, ctx, *args):
        await ctx.message.delete()
        
        doggy = self.get_dog_img()
        text_chan = self.bot.get_channel(1065691151052570634)

        await text_chan.send(doggy)
