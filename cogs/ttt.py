import discord
from discord.ui import Button, View
from discord.ext import commands, tasks


async def setup(bot):
    await bot.add_cog(ttt(bot))


class TTTView(View):
    player1 = None
    player2 = None
    p_turn = 1

    g_space = [-1, -2, -3, -4, -5, -6, -7, -8, -9]

    def __init__(self, p1, p2):
        super().__init__(timeout = 24 * 60 * 60)
        self.player1 = p1
        self.player2 = p2


    async def check_win(self, interaction):
        end = None

        if self.g_space[0] == self.g_space[1] == self.g_space[2] or\
        self.g_space[3] == self.g_space[4] == self.g_space[5] or\
        self.g_space[6] == self.g_space[7] == self.g_space[8]:
            end = True
        elif self.g_space[0] == self.g_space[3] == self.g_space[6] or\
        self.g_space[1] == self.g_space[4] == self.g_space[7] or\
        self.g_space[2] == self.g_space[5] == self.g_space[8]:
            end = True
        elif self.g_space[0] == self.g_space[4] == self.g_space[8] or\
        self.g_space[2] == self.g_space[4] == self.g_space[6]:
            end = True
        else:
            end = False

        if end == False:
            if self.p_turn == 1:
                await interaction.response.edit_message(content = f"Tic-Tac-Toe {self.player2.name} vs {self.player1.name}\n{self.player1.mention}'s turn.", view = self)
            elif self.p_turn == 2:
                await interaction.response.edit_message(content = f"Tic-Tac-Toe {self.player2.name} vs {self.player1.name}\n{self.player2.mention}'s turn.", view = self)
        elif end == True:
            for button in self.children:
                button.disabled = True

            if self.p_turn == 1:
                await interaction.response.edit_message(content = f"Winner {self.player2.name}!", view = self)
            elif self.p_turn == 2:
                await interaction.response.edit_message(content = f"Winner {self.player1.name}!", view = self)

            await interaction.followup.send(f"https://tenor.com/view/minions-gif-26254840")


    def p1_play(self, button, g_space):
        button.label = 'X'
        self.g_space[g_space - 1] = 1   # 1 for X
        button.disabled = True
        button.style = discord.ButtonStyle.red
        self.p_turn = 2


    def p2_play(self, button, g_space):
        button.label = 'O'
        self.g_space[g_space - 1] = 2   # 2 for O
        button.disabled = True
        button.style = discord.ButtonStyle.green
        self.p_turn = 1


    @discord.ui.button(label = '⠀', style = discord.ButtonStyle.grey, row = 0)
    async def btn1_callback(self, interaction: discord.Interaction, button: Button):
        if self.p_turn == 1 and interaction.user == self.player1:
            self.p1_play(button, 1)
        elif self.p_turn == 2 and interaction.user == self.player2:
            self.p2_play(button, 1)
        else:
            if self.p_turn == 1:
                await interaction.response.edit_message(content = f"Tic-Tac-Toe {self.player2.name} vs {self.player1.name}\n{str(self.player1.mention).upper()}'s turn.")
            elif self.p_turn == 2:
                await interaction.response.edit_message(content = f"Tic-Tac-Toe {self.player2.name} vs {self.player1.name}\n{str(self.player2.mention).upper()}'s turn.")
            return

        await self.check_win(interaction = interaction)


    @discord.ui.button(label = '⠀', style = discord.ButtonStyle.grey, row = 0)
    async def btn2_callback(self, interaction: discord.Interaction, button: Button):
        if self.p_turn == 1 and interaction.user == self.player1:
            self.p1_play(button, 2)
        elif self.p_turn == 2 and interaction.user == self.player2:
            self.p2_play(button, 2)
        else:
            if self.p_turn == 1:
                await interaction.response.edit_message(content = f"Tic-Tac-Toe {self.player2.name} vs {self.player1.name}\n{str(self.player1.mention).upper()}'s turn.")
            elif self.p_turn == 2:
                await interaction.response.edit_message(content = f"Tic-Tac-Toe {self.player2.name} vs {self.player1.name}\n{str(self.player2.mention).upper()}'s turn.")

        await self.check_win(interaction = interaction)


    @discord.ui.button(label = '⠀', style = discord.ButtonStyle.grey, row = 0)
    async def btn3_callback(self, interaction: discord.Interaction, button: Button):
        if self.p_turn == 1 and interaction.user == self.player1:
            self.p1_play(button, 3)
        elif self.p_turn == 2 and interaction.user == self.player2:
            self.p2_play(button, 3)
        else:
            if self.p_turn == 1:
                await interaction.response.edit_message(content = f"Tic-Tac-Toe {self.player2.name} vs {self.player1.name}\n{str(self.player1.mention).upper()}'s turn.")
            elif self.p_turn == 2:
                await interaction.response.edit_message(content = f"Tic-Tac-Toe {self.player2.name} vs {self.player1.name}\n{str(self.player2.mention).upper()}'s turn.")

        await self.check_win(interaction = interaction)


    @discord.ui.button(label = '⠀', style = discord.ButtonStyle.grey, row = 1)
    async def btn4_callback(self, interaction: discord.Interaction, button: Button):
        if self.p_turn == 1 and interaction.user == self.player1:
            self.p1_play(button, 4)
        elif self.p_turn == 2 and interaction.user == self.player2:
            self.p2_play(button, 4)
        else:
            if self.p_turn == 1:
                await interaction.response.edit_message(content = f"Tic-Tac-Toe {self.player2.name} vs {self.player1.name}\n{str(self.player1.mention).upper()}'s turn.")
            elif self.p_turn == 2:
                await interaction.response.edit_message(content = f"Tic-Tac-Toe {self.player2.name} vs {self.player1.name}\n{str(self.player2.mention).upper()}'s turn.")

        await self.check_win(interaction = interaction)


    @discord.ui.button(label = '⠀', style = discord.ButtonStyle.grey, row = 1)
    async def btn5_callback(self, interaction: discord.Interaction, button: Button):
        if self.p_turn == 1 and interaction.user == self.player1:
            self.p1_play(button, 5)
        elif self.p_turn == 2 and interaction.user == self.player2:
            self.p2_play(button, 5)
        else:
            if self.p_turn == 1:
                await interaction.response.edit_message(content = f"Tic-Tac-Toe {self.player2.name} vs {self.player1.name}\n{str(self.player1.mention).upper()}'s turn.")
            elif self.p_turn == 2:
                await interaction.response.edit_message(content = f"Tic-Tac-Toe {self.player2.name} vs {self.player1.name}\n{str(self.player2.mention).upper()}'s turn.")

        await self.check_win(interaction = interaction)


    @discord.ui.button(label = '⠀', style = discord.ButtonStyle.grey, row = 1)
    async def btn6_callback(self, interaction: discord.Interaction, button: Button):
        if self.p_turn == 1 and interaction.user == self.player1:
            self.p1_play(button, 6)
        elif self.p_turn == 2 and interaction.user == self.player2:
            self.p2_play(button, 6)
        else:
            if self.p_turn == 1:
                await interaction.response.edit_message(content = f"Tic-Tac-Toe {self.player2.name} vs {self.player1.name}\n{str(self.player1.mention).upper()}'s turn.")
            elif self.p_turn == 2:
                await interaction.response.edit_message(content = f"Tic-Tac-Toe {self.player2.name} vs {self.player1.name}\n{str(self.player2.mention).upper()}'s turn.")

        await self.check_win(interaction = interaction)


    @discord.ui.button(label = '⠀', style = discord.ButtonStyle.grey, row = 2)
    async def btn7_callback(self, interaction: discord.Interaction, button: Button):
        if self.p_turn == 1 and interaction.user == self.player1:
            self.p1_play(button, 7)
        elif self.p_turn == 2 and interaction.user == self.player2:
            self.p2_play(button, 7)
        else:
            if self.p_turn == 1:
                await interaction.response.edit_message(content = f"Tic-Tac-Toe {self.player2.name} vs {self.player1.name}\n{str(self.player1.mention).upper()}'s turn.")
            elif self.p_turn == 2:
                await interaction.response.edit_message(content = f"Tic-Tac-Toe {self.player2.name} vs {self.player1.name}\n{str(self.player2.mention).upper()}'s turn.")

        await self.check_win(interaction = interaction)


    @discord.ui.button(label = '⠀', style = discord.ButtonStyle.grey, row = 2)
    async def btn8_callback(self, interaction: discord.Interaction, button: Button):
        if self.p_turn == 1 and interaction.user == self.player1:
            self.p1_play(button, 8)
        elif self.p_turn == 2 and interaction.user == self.player2:
            self.p2_play(button, 8)
        else:
            if self.p_turn == 1:
                await interaction.response.edit_message(content = f"Tic-Tac-Toe {self.player2.name} vs {self.player1.name}\n{str(self.player1.mention).upper()}'s turn.")
            elif self.p_turn == 2:
                await interaction.response.edit_message(content = f"Tic-Tac-Toe {self.player2.name} vs {self.player1.name}\n{str(self.player2.mention).upper()}'s turn.")

        await self.check_win(interaction = interaction)


    @discord.ui.button(label = '⠀', style = discord.ButtonStyle.grey, row = 2)
    async def btn9_callback(self, interaction: discord.Interaction, button: Button):
        if self.p_turn == 1 and interaction.user == self.player1:
            self.p1_play(button, 9)
        elif self.p_turn == 2 and interaction.user == self.player2:
            self.p2_play(button, 9)
        else:
            if self.p_turn == 1:
                await interaction.response.edit_message(content = f"Tic-Tac-Toe {self.player2.name} vs {self.player1.name}\n{str(self.player1.mention).upper()}'s turn.")
            elif self.p_turn == 2:
                await interaction.response.edit_message(content = f"Tic-Tac-Toe {self.player2.name} vs {self.player1.name}\n{str(self.player2.mention).upper()}'s turn.")

        await self.check_win(interaction = interaction)


class ttt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print("Tic-Tac-Toe module is loaded.")


    @commands.command(  name = 'ttt',
                        help = '>ttt @challenged',
                        brief = '- Start a new game of Tic-Tac-Toe with someone.')
    async def ttt_new_game(self, ctx, challenged: discord.User = None):
        if challenged == None:
            await ctx.send("You need to challenge someone.\n>ttt_new @challenged")

            return

        await ctx.message.delete()
        
        try:
            view = TTTView(challenged, ctx.author)

            embed1 = discord.Embed(title = f"{challenged.name} has been challenged to a Tic-Tac-Toe game by {ctx.author.name}",
                                    url = "https://google.com")
            embed2 = discord.Embed(url = "https://google.com")
            embed1.set_image(url = f'{challenged.display_avatar}')
            embed2.set_image(url = f'{ctx.author.display_avatar}')
            await ctx.send(embeds = [embed1, embed2])
            await ctx.send(f"https://tenor.com/view/yu-gi-oh-duel-yugi-anime-gif-7357665")

            await ctx.send(f"Tic-Tac-Toe {ctx.author.name} vs {challenged.name}\n{challenged.mention}'s turn.", view = view)
        except Exception as e:
            text_chan = self.bot.get_channel(548554244932894750)
            await text_chan.send(f"[Tic-Tac-Toe]\n{e}")
            
            return


    @commands.command(  name = 'ttt_test',
                        help = '>ttt_new @challenged',
                        brief = '- Start a new game of Tic-Tac-Toe with someone.')
    async def ttt_test_func(self, ctx, challenged: discord.User = None):
        if challenged == None:
            # await ctx.send("You need to challenge someone.\n >ttt_new @challenged")
            challenged = self.bot.user

            # return

        await ctx.message.delete()
        
        try:
            view = TTTView(challenged, ctx.author)

            await ctx.send(f"Tic-Tac-Toe {ctx.author.name} vs {challenged.name}\n{challenged.name}'s turn.", view = view)
        except Exception as e:
            text_chan = self.bot.get_channel(548554244932894750)
            await text_chan.send(f"[Tic-Tac-Toe]\n{e}")
            
            return