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
                     second = 00,\
                     tzinfo = BG_time_zone)


async def setup(bot):
    await bot.add_cog(quotes(bot))


class quotes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    def get_quote(self):
        response = requests.get("https://zenquotes.io/api/random")
        json_data = json.loads(response.text)
        quote = json_data[0]['q'] + " - " + json_data[0]['a']
        return quote


    @tasks.loop(time = time)
    async def good_morning_message(self):
        text_chan = self.bot.get_channel(337156974754136064)
        quote = self.get_quote()
        
        await text_chan.send(f"Good Morning Everyone!")
        await text_chan.send(f"Here is your daily quote:\n{quote}")


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
