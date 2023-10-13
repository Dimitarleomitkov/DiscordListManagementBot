import discord
import datetime
import dateutil.tz as dateutils
import time as tim
from discord.ext import commands, tasks
import platform
import asyncio


if platform.system() != "Windows":
    import RPi.GPIO as GPIO

    GPIO.setwarnings(False)


async def setup(bot):
    if platform.system() != "Windows":
        await bot.add_cog(watering_plants(bot))
    else:
        pass


def get_the_time():
    if tim.localtime().tm_isdst:
        BG_tz = dateutils.tzoffset('UTC', 60 * 60 * 3)
    else:
        BG_tz = dateutils.tzoffset('UTC', 60 * 60 * 2)

    return datetime.time(hour = 8,\
                        minute = 00,\
                        second = 00,\
                        tzinfo = BG_tz)


class watering_plants(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    the_time = get_the_time()
    auto_time_ON_seconds = 15   # The amount of time the pump is on every morning


    @tasks.loop(time = the_time)
    async def auto_watering(self):
        await self.water_plant(15)

        self.the_time = get_the_time()
        self.auto_watering.change_interval(time = self.the_time)


    async def water_plant(self, seconds):
        # Pin Definitons:
        pump_GPIO = 23 # GPIO 23 PIN 16

        # Pin Setup:
        GPIO.setmode(GPIO.BCM) # BCM for naming BOARD for pin number
        GPIO.setup(pump_GPIO, GPIO.OUT) # pin 16 set as output

        # Pin control:
        GPIO.output(pump_GPIO, GPIO.HIGH)

        await asyncio.sleep(int(seconds))
        await self.pump_off()


    async def pump_off(self):
        # Pin Definitons:
        pump_GPIO = 23 # GPIO 23 PIN 16

        # Pin Setup:
        GPIO.setmode(GPIO.BCM) # BCM for naming BOARD for pin number
        GPIO.setup(pump_GPIO, GPIO.OUT) # pin 16 set as output

        # Pin control:
        GPIO.output(pump_GPIO, GPIO.LOW)


    @commands.Cog.listener()
    async def on_ready(self):
        print("watering_plants module is loaded.")


    @commands.command(  name = 'wpump_on',
                        help = 'Turns the water pump ON.',
                        brief = '- water pump ON!')
    async def pump_on_func (self, ctx, seconds):
        if ctx.author.name != "undeadko":
            ctx.reply("You do not have permission to do this.")
            ctx.reply("https://tenor.com/view/baka-anime-gif-12908346")
            return

        try:
            int_seconds = int(seconds)
        except Exception as e:
            print(e)

        if not isinstance(int_seconds, int):
            if seconds == None:
                seconds = 3
            else:
                await ctx.reply("Give me an integer for seconds.")
                return

        await ctx.send("I am watering the basil :potted_plant: :shower: ")
        await self.water_plant(seconds)



    @commands.command(  name = 'wpump_off',
                        help = 'Turns the water pump OFF.',
                        brief = '- water pump OFF!')
    async def pump_off_func(self, ctx):
        await self.pump_off()

        await ctx.send("The water pump is OFF.")


    @commands.command(  name = 'auto_water_length',
                        help = 'Change the amount of time the water pump is ON every morning.',
                        brief = '- Change the amount of time the water pump is ON every morning.')
    async def set_auto_water_duration_func(self, ctx, seconds):
        if ctx.author.name != "undeadko":
            ctx.reply("You do not have permission to do this.")
            ctx.reply("https://tenor.com/view/baka-anime-gif-12908346")
            return

        try:
            int_seconds = int(seconds)
        except Exception as e:
            print(e)

        if not isinstance(int_seconds, int):        
            await ctx.reply("Give me an integer for seconds.")
            return

        self.auto_time_ON_seconds = int_seconds

        await ctx.send(f"The morning automatic watering time was set to {self.auto_time_ON_seconds} seconds.")


