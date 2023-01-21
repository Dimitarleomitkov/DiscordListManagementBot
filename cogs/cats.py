import discord
import requests
import json
from discord.ext import commands


async def setup(bot):
    await bot.add_cog(cats(bot))


class cats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.catURL = 'http://aws.random.cat/meow'


    def get_cat_img(self):
        response = requests.get(self.catURL)
        json_data = json.loads(response.content)
        cat_img = json_data["file"]

        return cat_img


    @commands.Cog.listener()
    async def on_ready(self):
        print("cats module is loaded.")


    @commands.command(  name = 'rcat',
                        help = 'The bot will get a random cat picture/gif.',
                        brief = '- Gets a random cat picture/gif.')
    async def cats(self, ctx):
        await ctx.message.delete()

        catze = self.get_cat_img()
        text_chan = self.bot.get_channel(1066377134836285480)

        embed = discord.Embed()
        embed.set_image(url = catze)

        await text_chan.send(f"{ctx.author.mention} requested:", embed = embed)
