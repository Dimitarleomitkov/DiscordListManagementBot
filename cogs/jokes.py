import discord
import datetime
import dateutil.tz as dateutils
import time as tim
from discord.ext import commands, tasks
from jokeapi import Jokes


async def setup(bot):
    await bot.add_cog(jokes(bot))


def get_the_time():
    if tim.localtime().tm_isdst:
        BG_tz = dateutils.tzoffset('UTC', 60 * 60 * 3)
    else:
        BG_tz = dateutils.tzoffset('UTC', 60 * 60 * 2)

    return datetime.time(hour = 8,\
                        minute = 00,\
                        second = 59,\
                        tzinfo = BG_tz)


class jokes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    the_time = get_the_time()


    async def get_jokes(self, *args):
        j = await Jokes()
        joke = await j.get_joke()

        return joke


    @tasks.loop(time = the_time)
    async def good_morning_joke(self):
        text_chan = self.bot.get_channel(337156974754136064)
        joke = await self.get_jokes()
        
        await text_chan.send(f"Daily joke:\n")
        if joke["type"] == "single":
            await text_chan.send(f"{joke['joke']}")
        else:
            await text_chan.send(f"{joke['setup']}\n{joke['delivery']}")

        self.the_time = get_the_time()
        self.good_morning_joke.change_interval(time = self.the_time)


    @commands.Cog.listener()
    async def on_ready(self):
        print("jokes module is loaded.")
        self.good_morning_joke.start()


    @commands.command(  name = 'joke',
                        help = 'The bot will get a random joke and print it.',
                        brief = '- Prints a random joke in the chat.')
    async def jokes(self, ctx, *args):
        joke = await self.get_jokes()
        if joke["type"] == "single":
            await ctx.send(f"{joke['joke']}")
        else:
            await ctx.send(f"{joke['setup']}\n{joke['delivery']}")
