import discord
from discord.ext import commands


async def setup(bot):
    await bot.add_cog(cooling_rpi(bot))


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

        await ctx.send("I am cool now <:aniguns:965289318585352212>")


    @commands.command(  name = 'fan_off',
                        help = 'Turns the r-pi fan OFF.',
                        brief = '- fan OFF!')
    async def fan_off_func(self, ctx):

        await ctx.send("<:loshoMiE:448905900279857153>")



