import discord
import random
from discord.ext import commands


async def setup(bot):
    await bot.add_cog(temp_c(bot))


class temp_c(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print("temp_conversion module is loaded.")


    @commands.command(  name = 't_ftoc',
                        help = 'The bot will convert Fahrenheit to Celsius.',
                        brief = '- Prints the degrees in Celsius.')
    async def far_to_cel(self, ctx, temperature):
        temperature = float(temperature)
        target_temp = (temperature - 32) * 5 / 9

        await ctx.reply(f"{temperature}°F is {target_temp:.2f}°C.")


    @commands.command(  name = 't_ftok',
                        help = 'The bot will convert Fahrenheit to Kelvin.',
                        brief = '- Prints the degrees in Kelvin.')
    async def far_to_kel(self, ctx, temperature):
        temperature = float(temperature)
        target_temp = ((temperature - 32) * 5 / 9) + 273.15

        await ctx.reply(f"{temperature}°F is {target_temp:.2f}°K.")


    @commands.command(  name = 't_ctof',
                        help = 'The bot will convert Celsius to Fahrenheit.',
                        brief = '- Prints the degrees in Fahrenheit.')
    async def cel_to_far(self, ctx, temperature):
        temperature = float(temperature)
        target_temp = (temperature * 9 / 5) + 32

        await ctx.reply(f"{temperature}°C is {target_temp:.2f}°F.")


    @commands.command(  name = 't_ctok',
                        help = 'The bot will convert Celsius to Kelvin.',
                        brief = '- Prints the degrees in Kelvin.')
    async def cel_to_kel(self, ctx, temperature):
        temperature = float(temperature)
        target_temp = temperature + 273.15

        await ctx.reply(f"{temperature}°C is {target_temp:.2f}°K.")


    @commands.command(  name = 't_ktof',
                        help = 'The bot will convert Kelvin to Fahrenheit.',
                        brief = '- Prints the degrees in Fahrenheit.')
    async def kel_to_far(self, ctx, temperature):
        temperature = float(temperature)
        target_temp = ((temperature - 273.15) * 9 / 5) + 32

        await ctx.reply(f"{temperature}°K is {target_temp:.2f}°F.")


    @commands.command(  name = 't_ktoc',
                        help = 'The bot will convert Kelvin to Celsius.',
                        brief = '- Prints the degrees in Celsius.')
    async def kel_to_cel(self, ctx, temperature):
        temperature = float(temperature)
        target_temp = temperature - 273.15

        await ctx.reply(f"{temperature}°K is {target_temp:.2f}°C.")