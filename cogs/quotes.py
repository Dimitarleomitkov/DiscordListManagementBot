import discord
import requests
import json
import datetime
import dateutil.tz as dateutils
import time as tim
from discord.ext import commands, tasks


async def setup(bot):
    await bot.add_cog(quotes(bot))


def get_the_time():
    if tim.localtime().tm_isdst:
        BG_tz = dateutils.tzoffset('UTC', 60 * 60 * 3)
    else:
        BG_tz = dateutils.tzoffset('UTC', 60 * 60 * 2)

    return datetime.time(hour = 8,\
                        minute = 0,\
                        second = 0,\
                        tzinfo = BG_tz)


class quotes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    the_time = get_the_time()


    def get_quote(self):
        response = requests.get("https://zenquotes.io/api/random")
        json_data = json.loads(response.text)
        quote = json_data[0]['q'] + " - " + json_data[0]['a']
        return quote


    @tasks.loop(time = the_time)
    async def good_morning_message(self):
        text_chan = self.bot.get_channel(1411602053167321138)
        quote = self.get_quote()
 
        await text_chan.send(f"Good Morning Everyone!")
        await text_chan.send(f"Here is your daily quote:\n{quote}")
            
        self.the_time = get_the_time()
        self.good_morning_message.change_interval(time = self.the_time)
        

    @commands.Cog.listener()
    async def on_ready(self):
        print("quotes module is loaded.")
        self.good_morning_message.start()


    @commands.command(  name = 'quote',
                        help = 'The bot will get a random quote and print it.',
                        brief = '- Prints a random quote in the chat.')
    async def quotes(self, ctx):
        quote = self.get_quote()
        await ctx.send(quote)


    @commands.command(  name = 'tnext_quote',
                        help = 'The bot will print the time of the next scheduled quote.',
                        brief = '- Prints the time of the next scheduled quote.')
    async def get_next_iteration(self, ctx):
        await ctx.send("I am scheduled to give you the next quote on " +\
                        str(self.good_morning_message.next_iteration))
