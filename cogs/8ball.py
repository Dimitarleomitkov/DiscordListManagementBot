import discord
import random
from discord.ext import commands


async def setup(bot):
    await bot.add_cog(ball8(bot))


class ball8(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print("8ball module is loaded.")


    @commands.command(  name = '8ball',
                        help = 'The bot will respond with a magical 8 ball answer.',
                        brief = '- Prints your question and the magical 8 ball answer.')
    async def ball8(self, ctx, *args):
        question = ""
        for arg in args:
            question += arg + ' '

        question = question.strip()
        responses = ["As I see it, yes.", "Ask again later.", "Better not tell you now.", "Cannot predict now.",
                    "Concentrate and ask again.", "Don't count on it.", "It is certain.", "It is decidedly so.",
                    "Most likely.", "My reply is no.", "My sources say no.", "Outlook not so good.", "Outlook good.",
                    "Reply hazy, try again.", "Signs point to yes.", "Very doubtful.", "Without a doubt.", "Yes.",
                    "Yes - definitely", "You may rely on it."]
    
        await ctx.send(f"**Question:** {question}\n\
**Answer:** {random.choice(responses)}")