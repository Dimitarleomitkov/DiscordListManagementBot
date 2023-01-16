import discord
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

async def setup(bot):
    await bot.add_cog(quotes(bot))

class quotes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def good_morning_message():
        text_chan = bot.get_channel(337156974754136064)
        await text_chan.send("Good Morning Everyone!")

    @commands.Cog.listener()
    async def on_ready(self):
        print("quotes module is loaded.")

        #initializing scheduler
        scheduler = AsyncIOScheduler()

        #sends a good morning message every day
        scheduler.add_job(good_morning_message, CronTrigger(hour = '7', minute = '00', second = '00')) 

        #starting the scheduler
        scheduler.start()


    @commands.command(  name = 'quote',
                        help = 'The bot will get a random quote and print it.',
                        brief = '- Prints a random quote in the chat.')
    async def quotes(self, ctx, *args):
        undeadko_mention = '<@337156733774594048>'
        await ctx.send(f"{undeadko_mention} needs to fix me but he is too lazy to do so :kittendrink: ")


# def get_quote():
#     response = requests.get("https://zenquotes.io/api/random")
#     json_data = json.loads(response.text)
#     quote = json_data[0]['q'] + " - " + json_data[0]['a']
#     return (quote)