import discord
from discord.ext import commands, tasks


async def setup(bot):
    await bot.add_cog(ttt(bot))



class TTTView(discord.ui.View): # Create a class called TTTView that subclasses discord.ui.View
    @discord.ui.button(label = "Test", style = discord.ButtonStyle.primary, emoji="😎") # Create a button with the label "😎 Click me!" with color Blurple
    async def button_callback(self, button, interaction):
        await interaction.response.send_message("You clicked the button!") # Send a message when the button is clicked



class ttt(commands.Cog):
    player1 = None
    player2 = None


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

            embed1 = discord.Embed(title = f"{self.player1.name} has been challenged to a Tic-Tac-Toe game by {self.player2.name}",
                                    url = "https://google.com")
            embed2 = discord.Embed(url = "https://google.com")
            embed1.set_image(url = f'{self.player1.display_avatar}')
            embed2.set_image(url = f'{self.player2.display_avatar}')
            await ctx.send(embeds = [embed1, embed2])

            await ctx.send(f"https://tenor.com/view/yu-gi-oh-duel-yugi-anime-gif-7357665")
            await ctx.send(f"Tic-Tac-Toe {self.player1.name} vs {self.player2.name}", view = TTTView())
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