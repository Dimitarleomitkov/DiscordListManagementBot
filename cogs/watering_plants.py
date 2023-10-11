import discord
from discord.ext import commands
import platform

if platform.system() != "Windows":
    import RPi.GPIO as GPIO

    GPIO.setwarnings(False)


async def setup(bot):
    if platform.system() != "Windows":
        await bot.add_cog(watering_plants(bot))
    else:
        pass


class watering_plants(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print("watering_plants module is loaded.")


    @commands.command(  name = 'wpump_on',
                        help = 'Turns the water pump ON.',
                        brief = '- water pump ON!')
    async def pump_on_func (self, ctx):
        if ctx.author != "undeadko#0":
            return

        # Pin Definitons:
        pump_GPIO = 23 # GPIO 23 PIN 16

        # Pin Setup:
        GPIO.setmode(GPIO.BCM) # BCM for naming BOARD for pin number
        GPIO.setup(pump_GPIO, GPIO.OUT) # pin 16 set as output

        # Pin control:
        GPIO.output(pump_GPIO, GPIO.HIGH)

        await ctx.send("I am watering the basil :potted_plant: :shower: ")
        await asyncio.sleep(2)
        await self.pump_off_func(ctx)



    @commands.command(  name = 'wpump_off',
                        help = 'Turns the water pump OFF.',
                        brief = '- water pump OFF!')
    async def pump_off_func(self, ctx):
        # Pin Definitons:
        pump_GPIO = 23 # GPIO 23 PIN 16

        # Pin Setup:
        GPIO.setmode(GPIO.BCM) # BCM for naming BOARD for pin number
        GPIO.setup(pump_GPIO, GPIO.OUT) # pin 16 set as output

        # Pin control:
        GPIO.output(pump_GPIO, GPIO.LOW)

        await ctx.send("The water pump is OFF.")



