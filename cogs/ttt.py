import discord
from discord.ext import commands, tasks


async def setup(bot):
    await bot.add_cog(ttt(bot))


class ttt(commands.Cog):
    player1 = None
    player2 = None

    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print("Tic-Tac-Toe module is loaded.")
        self.good_morning_message.start()


    @commands.command(  name = 'ttt_new',
                        help = '>ttt_new @challenged',
                        brief = '- Start a new game of Tic-Tac-Toe with someone.')
    async def ttt_new_game(self, ctx, challenged):
        self.player2 = ctx.author
        self.player1 = challenged

        try:
            ctx.send(f"{self.player2.mention} has been challenged to a Tic-Tac-Toe game by {self.player1.mention}")
            ctx.send(f"https://tenor.com/view/yu-gi-oh-duel-yugi-anime-gif-7357665")
            embed = discord.Embed(title = f"Tic-Tac-Toe {self.player1.mention} vs {self.player2.mention}")
            embed = discord.add_field(f"\
                                        | | | |        |1|2|3|\
                                        | | | |        |4|5|6|\
                                        | | | |        |7|8|9|\
                                        \n\n\
                                        It is {self.player1.mention} turn. Use '>ttt <number>' to play.\
                                    ")
            embed.set_thumbnail(url = "https://e7.pngegg.com/pngimages/923/206/png-clipart-tictactoe-tic-tac-toe-oxo-tac-tic-toe-computer-icons-games-buttons-game-logo-thumbnail.png")

        except Exception as e:
            text_chan = self.bot.get_channel(548554244932894750)
            await text_chan.send(["[Tic-Tac-Toe]"], e)
            
            return


    @commands.command( name = 'ttt',
                       help = '>ttt <field_number>',
                       brief = 'Makes a play in the field.')
    async def ttt_place(self, ctx, field):
        print(self.player1, self.player2)
        ctx.send(self.player1, self.player2)
        # if ctx.author != self.player1 || ctx.author != self.player2:
        #     ctx.send(f"Other people are playing. Stop being rude!")
        #     ctx.send(f"https://tenor.com/view/really-dog-pup-puppy-head-shaking-gif-17699585")

        #     return

        # place()
        # check_win()