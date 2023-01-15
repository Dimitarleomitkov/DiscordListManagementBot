import discord
import platform
from discord.ext import commands

async def setup(bot):
    await bot.add_cog(test(bot))

class test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("test module is loaded.")

    @commands.command(  name = 'ping',
                        help = 'The bot will respond with its latency.',
                        brief = '- Prints latency.')
    async def ping_func(self, ctx):
        await ctx.send(f"{round(self.bot.latency * 1000)}ms")

    @commands.command(  name = 'test',
                        help = 'The bot will respond.',
                        brief = '- Response.')
    async def test_func(self, ctx):
        await ctx.send(f"[{platform.system()}] I am alive. Waiting for commands.")
