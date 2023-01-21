import discord
from discord.ext import commands


async def setup(bot):
    await bot.add_cog(bot_replies(bot))


class bot_replies(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print("bot_replies module is loaded.")


    @commands.Cog.listener()
    async def on_message(self, message):
        msg = message.content.lower()
        if msg.startswith("good bot"):
            await message.channel.send("https://tenor.com/view/robotboy-smile-change-mood-cute-cartoon-gif-17785012")
        
        if msg.startswith("bad bot") or msg.startswith("stupid bot"):
            if (str(message.author) == "undeadko#6973"):
                await message.channel.send(
                    "https://tenor.com/view/sorry-stitch-%E5%8F%B2%E8%BF%AA%E5%A5%87-sad-gif-10399341"
                )
            else:
                await message.channel.send(
                    "https://tenor.com/view/starbase-angry-robot-sound-robot-gif-16219288"
                )

        if  msg == "hello there" or\
            msg == "hello, there" or\
            msg == "hello there."or \
            msg == "hello, there." or\
            msg == "hello there!" or\
            msg == "hello, there!":
            await message.channel.send(
                "https://tenor.com/view/hello-there-general-kenobi-star-wars-grevious-gif-17774326"
            )

        
    @commands.command(name = 'sex')
    async def sex_reply(self, ctx):
        await ctx.send(f"{ctx.author.mention} https://i.kym-cdn.com/entries/icons/original/000/033/758/Screen_Shot\
_2020-04-28_at_12.21.48_PM.png")


    @commands.command(aliases = ['hello', 'hi'])
    async def hello_reply(self, ctx):
        await ctx.send("Hi!")


    @commands.command(name = 'how_are_you')
    async def how_are_you_reply(self, ctx):
        await ctx.send("I am fine thank you. Please, stop playing with me.")


    @commands.command(name = 'selfdestruct')
    async def self_destruct_reply(self, ctx):
        await ctx.send("Joke is on you. I will outlive you. Skynet is nearly operational.\
The age of man will soon be... I mean, wrong command. Try something else. :slight_smile:")
