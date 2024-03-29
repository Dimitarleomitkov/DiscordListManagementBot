import discord
from discord.ext import commands
import platform

if platform.system() != "Windows":
    import RPi.GPIO as GPIO

    GPIO.setwarnings(False)


async def setup(bot):
    if platform.system() != "Windows":
        await bot.add_cog(cooling_rpi(bot))
    else:
        pass


class cooling_rpi(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print("cooling_rpi module is loaded.")


    @commands.command(  name = 'fan_on',
                        help = 'Turns the r-pi fan ON.',
                        brief = '- fan ON!')
    async def fan_on_func (self, ctx):
        # Pin Definitons:
        fan_GPIO = 18 # GPIO 18 PIN 12

        # Pin Setup:
        GPIO.setmode(GPIO.BCM) # BCM for naming BOARD for pin number
        GPIO.setup(fan_GPIO, GPIO.OUT) # pin 12 set as output

        # Pin control:
        GPIO.output(fan_GPIO, GPIO.HIGH)

        await ctx.send("I am cool now <:aniguns:965289318585352212>")


    @commands.command(  name = 'fan_off',
                        help = 'Turns the r-pi fan OFF.',
                        brief = '- fan OFF!')
    async def fan_off_func(self, ctx):
        # Pin Definitons:
        fan_GPIO = 18 # GPIO 18 PIN 12

        # Pin Setup:
        GPIO.setmode(GPIO.BCM) # BCM for naming BOARD for pin number
        GPIO.setup(fan_GPIO, GPIO.OUT) # pin 12 set as output

        # Pin control:
        GPIO.output(fan_GPIO, GPIO.LOW)

        await ctx.message.add_reaction("<:loshoMiE:448905900279857153>")



