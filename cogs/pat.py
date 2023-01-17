import discord
from discord.ext import commands


async def setup(bot):
    await bot.add_cog(pat(bot))


class pat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print("pat module is loaded.")


    @commands.command(name = 'pat')
    async def pat_reply(self, ctx, *target_people: discord.User):
        await ctx.message.delete()

        if len(target_people) == 0:
            await ctx.send(f"{self.bot.user.mention} wants to pat someone... gently. :smirk:")
        
        for person in target_people:
            if person is self.bot.user:
                await ctx.send("https://tenor.com/view/pixar-walle-shutter-authority-help-please-gif-15756192")
            else:
                await ctx.send(f"{self.bot.user.mention} gently pats you, {person.mention}")
