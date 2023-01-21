import discord
from discord.ext import commands


async def setup(bot):
    await bot.add_cog(cogs(bot))


class cogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print("cogs module is loaded.")


    @commands.command(  name = 'load_cog',
                        help = 'The bot will load a cog.',
                        brief = '- The bot will load a cog.')
    async def load_cog_func(self, ctx, extension):
        await self.bot.load_extension(f"cogs.{extension}")
        await ctx.send(f"{extension} loaded.")


    @commands.command(  name = 'unload_cog',
                        help = 'The bot will unload a cog.',
                        brief = '- The bot will unload a cog.')
    async def unload_cog_func(self, ctx, extension):
        await self.bot.unload_extension(f"cogs.{extension}")
        await ctx.send(f"{extension} unloaded.")


    @commands.command(  name = 'reload_cog',
                        help = 'The bot will reload a cog.',
                        brief = '- The bot will reload a cog.')
    async def reload_cog_func(self, ctx, extension):
        await self.bot.unload_extension(f"cogs.{extension}")
        await self.bot.load_extension(f"cogs.{extension}")
        await ctx.send(f"{extension} reloaded.")
