import discord
import datetime
import dateutil.tz as dateutils
from discord.ext import commands, tasks
from jokeapi import Jokes

# If no tzinfo is given then UTC is assumed.
BG_time_zone = dateutils.tzoffset('UTC', 60 * 60 * 2)
time = datetime.time(hour = 8,\
                     minute = 00,\
                     second = 59,\
                     tzinfo = BG_time_zone)


async def setup(bot):
    await bot.add_cog(jokes(bot))


class jokes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    async def get_joke(self, *args):
        j = await Jokes()
        joke = await j.get_joke()

        return joke


    @tasks.loop(time = time)
    async def good_morning_joke(self):
        text_chan = self.bot.get_channel(337156974754136064)
        joke = self.get_joke()
        
        await text_chan.send(f"Daily joke:\n")
        if joke["type"] == "single":
            await ctx.send(f"{joke['joke']}")
        else:
            await ctx.send(f"{joke['setup']}\n{joke['delivery']}")



    @commands.Cog.listener()
    async def on_ready(self):
        print("jokes module is loaded.")
        self.good_morning_message.start()


    @commands.command(  name = 'joke',
                        help = 'The bot will get a random joke and print it.',
                        brief = '- Prints a random joke in the chat.')
    async def jokes(self, ctx, *args):
        joke = await self.get_joke()
        if joke["type"] == "single":
            await ctx.send(f"{joke['joke']}")
        else:
            await ctx.send(f"{joke['setup']}\n{joke['delivery']}")
