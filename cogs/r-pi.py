import discord
import datetime
import dateutil.tz as dateutils
import time as tim
import os
from discord.ext import commands, tasks

async def setup(bot):
  await bot.add_cog(rebooter(bot))


def get_reboot_time():
  #Adjust timezone for DST
  if tim.localtime().tm_isdst:
    BG_tz = dateutils.tzoffset('UTC', 60 * 60 * 3)
  else:
    BG_tz = dateutils.tzoffset('UTC', 60 * 60 * 2)

  # Set to 05:00 every Tuesday
  return datetime.time(hour = 5, minute = 0, second = 0, tzinfo = BG_tz)

class rebooter(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  reboot_time = get_reboot_time()

  @task.loop(time = reboot_time)
  async def weekly_reboot(self):
    # Only run on Tuesday (Python: Monday is 0, Tuesday is 1, ..., Sunday is 6)
    if datetime.datetime.now().weekday() == 1:
      text_chan = self.bot.get_channel(548554244932894750)
      await text_chan.send("Rebooting system...")
      os.system('sudo reboot')

    # Refresh reboot time in case of DST change
    self.reboot_time = get_reboot_time()
    self.weekly_reboot.change_interval(time = self.reboot_time)

  @commands.Cog.listener()
  async def on_ready(self):
    print("rebooter module is loaded.")
    self.weekly_reboot.start()

  @command.command(name = 'tnext_reboot',
                   help = 'Displays the time of the next scheduled reboot.',
                   brief = '- Prints the time of the next scheduled reboot.')
  async def get_next_reboot(self, ctx):
    await ctx.send("I am scheduled to reboot the system on " + str(self.weekly_reboot.next_iteration))
