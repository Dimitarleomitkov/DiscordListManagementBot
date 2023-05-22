import discord
from discord.ext import commands, tasks


async def setup(bot):
    await bot.add_cog(ttt(bot))


class ttt(commands.Cog):
    player1 = None
    player2 = None
    game = ['᲼᲼', '᲼᲼', '᲼᲼', \
            '᲼᲼', '᲼᲼', '᲼᲼', \
            '᲼᲼', '᲼᲼', '᲼᲼', ]
    game_str = f"\n\n\
                |{game[0]}|{game[1]}|{game[2]}|᲼᲼᲼᲼᲼᲼᲼᲼|᲼1᲼|᲼2᲼|᲼3᲼|\n\
                |{game[3]}|{game[4]}|{game[5]}|᲼᲼᲼᲼᲼᲼᲼᲼|᲼4᲼|᲼5᲼|᲼6᲼|\n\
                |{game[6]}|{game[7]}|{game[8]}|᲼᲼᲼᲼᲼᲼᲼᲼|᲼7᲼|᲼8᲼|᲼9᲼|\n\
                \n\n\
            "

    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print("Tic-Tac-Toe module is loaded.")
        self.good_morning_message.start()


    async def place(self, player, field):
        pass


    async def check_win(self, player):
        pass


    @commands.command(  name = 'ttt_new',
                        help = '>ttt_new @challenged',
                        brief = '- Start a new game of Tic-Tac-Toe with someone.')
    async def ttt_new_game(self, ctx, challenged: discord.User = None):
        if challenged == None:
            await ctx.send("You need to challenge someone.\n >ttt_new @challenged")

            return

        await ctx.message.delete()
        
        try:
            self.player2 = ctx.author
            self.player1 = challenged
            
            await ctx.send(f"{self.player1.mention} has been challenged to a Tic-Tac-Toe game by {self.player2.mention}")
            avatar_embed1 = discord.Embed(title = " ", url = 'https://google.com').set_image(url = f"{self.player1.display_avatar}")
            avatar_embed2 = discord.Embed(title = " ", url = 'https://google.com').set_image(url = f"{self.player2.display_avatar}")
            avatar_embed3 = discord.Embed(title = " ", url = 'https://google.com')
            avatar_embed4 = discord.Embed(title = " ", url = 'https://google.com')
            await ctx.send(embed = [avatar_embed1, avatar_embed2, avatar_embed3, avatar_embed4])

            await ctx.send(f"https://tenor.com/view/yu-gi-oh-duel-yugi-anime-gif-7357665")
            embed = discord.Embed(title = f"Tic-Tac-Toe {self.player1.name} vs {self.player2.name}")
            embed.add_field(name = "Game:",
                            value = self.game_str + f"It is {self.player1.mention} turn.\nUse '>ttt <number>' to play.",
                            inline = False
                            )
            embed.set_thumbnail(url = "https://www.emulatorpc.com/wp-content/uploads/2023/02/tic-tac-toe-on-pc.jpg.webp")

            await ctx.send(embed = embed)
        except Exception as e:
            text_chan = self.bot.get_channel(548554244932894750)
            await text_chan.send(f"[Tic-Tac-Toe]\n{e}")
            
            return


    @commands.command( name = 'ttt',
                       help = '>ttt <field_number>',
                       brief = '- Makes a play in the field.')
    async def ttt_place(self, ctx, field):
        if ctx.author != self.player1 or ctx.author != self.player2:
            ctx.send(f"Other people are playing. Stop being rude!")
            ctx.send(f"https://tenor.com/view/really-dog-pup-puppy-head-shaking-gif-17699585")

            return

        await self.place(player, field)
        await self.check_win(player)