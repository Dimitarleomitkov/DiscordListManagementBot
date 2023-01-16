import discord
import random
from discord.ext import commands

async def setup(bot):
    await bot.add_cog(role_play(bot))

class role_play(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.rp_flag_1 = False
        self.random_n_for_rp = 0;

    @commands.Cog.listener()
    async def on_ready(self):
        print("role_play module is loaded.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if (str(message.author) != "LootRankBot#2623"):
            self.random_n_for_rp = random.randint(0, 5000)
            print(self.random_n_for_rp)
            self.random_n_for_rp = 1

        if (self.random_n_for_rp == 1):
            if (str(message.author) != "undeadko#6973"):
                self.rp_flag_1 = True
                undeadko_mention = '<@337156733774594048>'
                await message.channel.send(f"{message.author.mention} Sh-h-h... {undeadko_mention} is sleeping. \
I can do whatever I want now... :smiling_imp:")
                return

        msg = message.content.strip().lower()

        if (str(message.author) == "undeadko#6973" and\
            (msg.startswith("i am not") or\
            msg.startswith("i am here") or\
            msg.startswith("i am awake") or\
            msg.startswith("stop")) and\
            self.rp_flag_1 == True):
            await message.channel.send(":zipper_mouth:")
            await message.channel.send("https://tenor.com/view/penguin-hide-you-didnt-see-anything\
-penguins-of-madagascar-gif-15123878")
            
            self.rp_flag_1 = False
            self.random_n_for_rp = 0
            return


