import discord
from discord.ext import commands


async def setup(bot):
    await bot.add_cog(spit(bot))


class spit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print("spit module is loaded.")


    # TODO: Make it spit on whatever I want. Not just @people
    @commands.command(name = 'spit')
    async def spitting(self, ctx, *target_people):
        await ctx.message.delete()

        if len(target_people) == 0:
            return
        
        for person in target_people:
            try:
                if person is self.bot.user:
                    await ctx.send("https://tenor.com/view/llama-mirada-gif-8834856")
                else:
                    await ctx.send(f"{person.mention}")
                    await ctx.send(f"https://tenor.com/view/the-rock-spit-gif-20218743")
            except Exception as e:
                await ctx.send(f"@{person}")
                await ctx.send(f"https://tenor.com/view/the-rock-spit-gif-20218743")