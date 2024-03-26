import discord
import datetime
import dateutil.tz as dateutils
import time as tim
from discord.ext import commands, tasks


async def setup(bot):
    await bot.add_cog(g_chatd(bot))


def get_the_time():
    if tim.localtime().tm_isdst:
        BG_tz = dateutils.tzoffset('UTC', 60 * 60 * 3)
    else:
        BG_tz = dateutils.tzoffset('UTC', 60 * 60 * 2)

    return datetime.time(hour = 4,\
                        minute = 00,\
                        second = 00,\
                        tzinfo = BG_tz)


class g_chatd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    the_time = get_the_time()


    @tasks.loop(time = the_time)
    async def delete_after_7_days(self):
        donjons = self.bot.get_channel(1196777525225996318)
        messages = donjons.history(limit = 1000)
        today = datetime.datetime.now(datetime.timezone.utc)

        async for message in messages:
            if (today - message.created_at).days >= 7:
                await message.delete()


    @commands.Cog.listener()
    async def on_ready(self):
        print("g_chatd module is loaded.")
        self.delete_after_7_days.start()


    # @commands.command(  name = 'purge_test',
    #                     help = 'asd',
    #                     brief = '- qwe')
    # async def testing_purge(self, ctx):
    #     try:
    #         await self.delete_after_7_days()
    #         await ctx.send(f"I checked the messages.")
    #     except Exception as e:
    #         await ctx.send(f"[PURGE] {e}")


    @commands.command(  name = 'tnext_purge_donjons',
                        help = 'The bot will print the time of the next purge of #donjons.',
                        brief = '- Prints the time of the next purge of #donjons.')
    async def get_next_iteration(self, ctx):
        await ctx.send("I am scheduled to delete the messages older than a week on " +\
                        str(self.delete_after_7_days.next_iteration))