import discord
import random
from discord.ext import commands

async def setup(bot):
    await bot.add_cog(movie_quotes(bot))

class movie_quotes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("movie_quotes module is loaded.")

    @commands.command(name = 'showmethemoney')
    async def show_me_the_money_reply(self, ctx):
        await ctx.send("https://itsadeliverything.com/images/show-me-the-money.jpg")

    @commands.command(name = 'mew2')
    async def mew2_reply(self, ctx):
        if (random.choice([0, 1])):
            await ctx.send("the circumstances of one's birth is irrelevent, \
it is what you do with the gift of life that determines who you are.")
        else:
            await ctx.send('The world pushes us with no mercy and when some push back \
the world points and cries \"evil\".')
