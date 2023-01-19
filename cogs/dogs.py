import discord
import requests
import json
from discord.ext import commands


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


    @commands.Cog.listener()
    async def on_ready(self):
        print("dogs module is loaded.")


    @commands.command(  name = 'rdog',
                        help = 'The bot will get a random dog picture.',
                        brief = '- Gets a random dog picture.')
    async def dogs(self, ctx):
        await ctx.message.delete()

        doggy = self.get_dog_img()
        text_chan = self.bot.get_channel(1065691151052570634)

        embed = discord.Embed()
        embed.set_image(url = doggy)

        await text_chan.send(f"{ctx.author.mention} requested:", embed = embed)
