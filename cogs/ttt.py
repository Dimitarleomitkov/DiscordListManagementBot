import discord
from discord.ui import Button, View
from discord.ext import commands, tasks


async def setup(bot):
    await bot.add_cog(ttt(bot))


class TTTView(View):
    player1 = None
    player2 = None
    p_turn = 1

    g_space1 = -1
    g_space2 = -2
    g_space3 = -3
    g_space4 = -4
    g_space5 = -5
    g_space6 = -6
    g_space7 = -7
    g_space8 = -8
    g_space9 = -9

    def __init__(self, p1, p2):
        super().__init__()
        self.player1 = p1
        self.player2 = p2


    def check_win(self):
        if self.g_space1 == self.g_space2 == self.g_space3 or\
        self.g_space4 == self.g_space5 == self.g_space6 or\
        self.g_space7 == self.g_space8 == self.g_space9:
            return True
        elif self.g_space1 == self.g_space4 == self.g_space7 or\
        self.g_space2 == self.g_space5 == self.g_space8 or\
        self.g_space3 == self.g_space6 == self.g_space9:
            return True
        elif self.g_space1 == self.g_space5 == self.g_space9 or\
        self.g_space2 == self.g_space5 == self.g_space7:
            return True

        return False


    @discord.ui.button(label = '⠀', style = discord.ButtonStyle.grey, row = 0)
    async def btn1_callback(self, interaction: discord.Interaction, button: Button):
        if self.p_turn == 1 and interaction.user == self.player1:
            button.label = "X"
            self.g_space1 = 1
            button.disabled = True
            button.style = discord.ButtonStyle.red
            self.p_turn = 2
        elif self.p_turn == 2 and interaction.user == self.player2:
            button.label = "O"
            self.g_space1 = 2
            button.disabled = True
            button.style = discord.ButtonStyle.green
            self.p_turn = 1
        else:
            if self.p_turn == 1:
                await interaction.response.edit_message(content = f"Tic-Tac-Toe {self.player2.name} vs {self.player1.name}\n{str(self.player1.name).upper()}'s turn.")
            elif self.p_turn == 2:
                await interaction.response.edit_message(content = f"Tic-Tac-Toe {self.player2.name} vs {self.player1.name}\n{str(self.player2.name).upper()}'s turn.")
            return

        end = self.check_win()

        if end == False:
            if self.p_turn == 1:
                await interaction.response.edit_message(content = f"Tic-Tac-Toe {self.player2.name} vs {self.player1.name}\n{self.player1.name}'s turn.", view = self)
            elif self.p_turn == 2:
                await interaction.response.edit_message(content = f"Tic-Tac-Toe {self.player2.name} vs {self.player1.name}\n{self.player2.name}'s turn.", view = self)
        else:
            for button in self.children:
                button.disabled = True

            if self.p_turn == 1:
                await interaction.response.edit_message(content = f"Winner {self.player2.name}!", view = self)
            elif self.p_turn == 2:
                await interaction.response.edit_message(content = f"Winner {self.player1.name}!", view = self)

            await interaction.followup.send(f"https://tenor.com/view/minions-gif-26254840")


    @discord.ui.button(label = '⠀', style = discord.ButtonStyle.grey, row = 0)
    async def btn2_callback(self, interaction: discord.Interaction, button: Button):
        if self.p_turn == 1 and interaction.user == self.player1:
            button.label = "X"
            self.g_space2 = 1
            button.disabled = True
            button.style = discord.ButtonStyle.red
            self.p_turn = 2
        elif self.p_turn == 2 and interaction.user == self.player2:
            button.label = "O"
            self.g_space2 = 2
            button.disabled = True
            button.style = discord.ButtonStyle.green
            self.p_turn = 1
        else:
            if self.p_turn == 1:
                await interaction.response.edit_message(content = f"Tic-Tac-Toe {self.player2.name} vs {self.player1.name}\n{str(self.player1.name).upper()}'s turn.")
            elif self.p_turn == 2:
                await interaction.response.edit_message(content = f"Tic-Tac-Toe {self.player2.name} vs {self.player1.name}\n{str(self.player2.name).upper()}'s turn.")

        end = self.check_win()

        if end == False:
            if self.p_turn == 1:
                await interaction.response.edit_message(content = f"Tic-Tac-Toe {self.player2.name} vs {self.player1.name}\n{self.player1.name}'s turn.", view = self)
            elif self.p_turn == 2:
                await interaction.response.edit_message(content = f"Tic-Tac-Toe {self.player2.name} vs {self.player1.name}\n{self.player2.name}'s turn.", view = self)
        else:
            for button in self.children:
                button.disabled = True

            if self.p_turn == 1:
                await interaction.response.edit_message(content = f"Winner {self.player2.name}!", view = self)
            elif self.p_turn == 2:
                await interaction.response.edit_message(content = f"Winner {self.player1.name}!", view = self)

            await interaction.followup.send(f"https://tenor.com/view/minions-gif-26254840")

    @discord.ui.button(label = '⠀', style = discord.ButtonStyle.grey, row = 0)
    async def btn3_callback(self, interaction: discord.Interaction, button: Button):
        if self.p_turn == 1 and interaction.user == self.player1:
            button.label = "X"
            self.g_space3 = 1
            button.disabled = True
            button.style = discord.ButtonStyle.red
        elif self.p_turn == 2 and interaction.user == self.player2:
            button.label = "O"
            self.g_space3 = 2
            button.disabled = True
            button.style = discord.ButtonStyle.green
        else:
            if self.p_turn == 1:
                await interaction.response.edit_message(content = f"Tic-Tac-Toe {self.player2.name} vs {self.player1.name}\n{str(self.player1.name).upper()}'s turn.")
            elif self.p_turn == 2:
                await interaction.response.edit_message(content = f"Tic-Tac-Toe {self.player2.name} vs {self.player1.name}\n{str(self.player2.name).upper()}'s turn.")

        end = self.check_win()

        if end == False:
            if self.p_turn == 1:
                await interaction.response.edit_message(content = f"Tic-Tac-Toe {self.player2.name} vs {self.player1.name}\n{self.player1.name}'s turn.", view = self)
            elif self.p_turn == 2:
                await interaction.response.edit_message(content = f"Tic-Tac-Toe {self.player2.name} vs {self.player1.name}\n{self.player2.name}'s turn.", view = self)
        else:
            for button in self.children:
                button.disabled = True

            if self.p_turn == 1:
                await interaction.response.edit_message(content = f"Winner {self.player2.name}!", view = self)
            elif self.p_turn == 2:
                await interaction.response.edit_message(content = f"Winner {self.player1.name}!", view = self)

            await interaction.followup.send(f"https://tenor.com/view/minions-gif-26254840")

    @discord.ui.button(label = '⠀', style = discord.ButtonStyle.grey, row = 1)
    async def btn4_callback(self, interaction: discord.Interaction, button: Button):
        if self.p_turn == 1 and interaction.user == self.player1:
            button.label = "X"
            self.g_space4 = 1
            button.disabled = True
            button.style = discord.ButtonStyle.red
        elif self.p_turn == 2 and interaction.user == self.player2:
            button.label = "O"
            self.g_space4 = 2
            button.disabled = True
            button.style = discord.ButtonStyle.green
        else:
            if self.p_turn == 1:
                await interaction.response.edit_message(content = f"Tic-Tac-Toe {self.player2.name} vs {self.player1.name}\n{str(self.player1.name).upper()}'s turn.")
            elif self.p_turn == 2:
                await interaction.response.edit_message(content = f"Tic-Tac-Toe {self.player2.name} vs {self.player1.name}\n{str(self.player2.name).upper()}'s turn.")

        end = self.check_win()

        if end == False:
            if self.p_turn == 1:
                await interaction.response.edit_message(content = f"Tic-Tac-Toe {self.player2.name} vs {self.player1.name}\n{self.player1.name}'s turn.", view = self)
            elif self.p_turn == 2:
                await interaction.response.edit_message(content = f"Tic-Tac-Toe {self.player2.name} vs {self.player1.name}\n{self.player2.name}'s turn.", view = self)
        else:
            for button in self.children:
                button.disabled = True

            if self.p_turn == 1:
                await interaction.response.edit_message(content = f"Winner {self.player2.name}!", view = self)
            elif self.p_turn == 2:
                await interaction.response.edit_message(content = f"Winner {self.player1.name}!", view = self)

            await interaction.followup.send(f"https://tenor.com/view/minions-gif-26254840")

    @discord.ui.button(label = '⠀', style = discord.ButtonStyle.grey, row = 1)
    async def btn5_callback(self, interaction: discord.Interaction, button: Button):
        if self.p_turn == 1 and interaction.user == self.player1:
            button.label = "X"
            self.g_space5 = 1
            button.disabled = True
            button.style = discord.ButtonStyle.red
        elif self.p_turn == 2 and interaction.user == self.player2:
            button.label = "O"
            self.g_space5 = 2
            button.disabled = True
            button.style = discord.ButtonStyle.green
        else:
            if self.p_turn == 1:
                await interaction.response.edit_message(content = f"Tic-Tac-Toe {self.player2.name} vs {self.player1.name}\n{str(self.player1.name).upper()}'s turn.")
            elif self.p_turn == 2:
                await interaction.response.edit_message(content = f"Tic-Tac-Toe {self.player2.name} vs {self.player1.name}\n{str(self.player2.name).upper()}'s turn.")

        end = self.check_win()

        if end == False:
            if self.p_turn == 1:
                await interaction.response.edit_message(content = f"Tic-Tac-Toe {self.player2.name} vs {self.player1.name}\n{self.player1.name}'s turn.", view = self)
            elif self.p_turn == 2:
                await interaction.response.edit_message(content = f"Tic-Tac-Toe {self.player2.name} vs {self.player1.name}\n{self.player2.name}'s turn.", view = self)
        else:
            for button in self.children:
                button.disabled = True

            if self.p_turn == 1:
                await interaction.response.edit_message(content = f"Winner {self.player2.name}!", view = self)
            elif self.p_turn == 2:
                await interaction.response.edit_message(content = f"Winner {self.player1.name}!", view = self)

            await interaction.followup.send(f"https://tenor.com/view/minions-gif-26254840")

    @discord.ui.button(label = '⠀', style = discord.ButtonStyle.grey, row = 1)
    async def btn6_callback(self, interaction: discord.Interaction, button: Button):
        if self.p_turn == 1 and interaction.user == self.player1:
            button.label = "X"
            self.g_space6 = 1
            button.disabled = True
            button.style = discord.ButtonStyle.red
        elif self.p_turn == 2 and interaction.user == self.player2:
            button.label = "O"
            self.g_space6 = 2
            button.disabled = True
            button.style = discord.ButtonStyle.green
        else:
            if self.p_turn == 1:
                await interaction.response.edit_message(content = f"Tic-Tac-Toe {self.player2.name} vs {self.player1.name}\n{str(self.player1.name).upper()}'s turn.")
            elif self.p_turn == 2:
                await interaction.response.edit_message(content = f"Tic-Tac-Toe {self.player2.name} vs {self.player1.name}\n{str(self.player2.name).upper()}'s turn.")

        end = self.check_win()

        if end == False:
            if self.p_turn == 1:
                await interaction.response.edit_message(content = f"Tic-Tac-Toe {self.player2.name} vs {self.player1.name}\n{self.player1.name}'s turn.", view = self)
            elif self.p_turn == 2:
                await interaction.response.edit_message(content = f"Tic-Tac-Toe {self.player2.name} vs {self.player1.name}\n{self.player2.name}'s turn.", view = self)
        else:
            for button in self.children:
                button.disabled = True

            if self.p_turn == 1:
                await interaction.response.edit_message(content = f"Winner {self.player2.name}!", view = self)
            elif self.p_turn == 2:
                await interaction.response.edit_message(content = f"Winner {self.player1.name}!", view = self)

            await interaction.followup.send(f"https://tenor.com/view/minions-gif-26254840")

    @discord.ui.button(label = '⠀', style = discord.ButtonStyle.grey, row = 2)
    async def btn7_callback(self, interaction: discord.Interaction, button: Button):
        if self.p_turn == 1 and interaction.user == self.player1:
            button.label = "X"
            self.g_space7 = 1
            button.disabled = True
            button.style = discord.ButtonStyle.red
        elif self.p_turn == 2 and interaction.user == self.player2:
            button.label = "O"
            self.g_space7 = 2
            button.disabled = True
            button.style = discord.ButtonStyle.green
        else:
            if self.p_turn == 1:
                await interaction.response.edit_message(content = f"Tic-Tac-Toe {self.player2.name} vs {self.player1.name}\n{str(self.player1.name).upper()}'s turn.")
            elif self.p_turn == 2:
                await interaction.response.edit_message(content = f"Tic-Tac-Toe {self.player2.name} vs {self.player1.name}\n{str(self.player2.name).upper()}'s turn.")

        end = self.check_win()

        if end == False:
            if self.p_turn == 1:
                await interaction.response.edit_message(content = f"Tic-Tac-Toe {self.player2.name} vs {self.player1.name}\n{self.player1.name}'s turn.", view = self)
            elif self.p_turn == 2:
                await interaction.response.edit_message(content = f"Tic-Tac-Toe {self.player2.name} vs {self.player1.name}\n{self.player2.name}'s turn.", view = self)
        elif end == True:
            for button in self.children:
                button.disabled = True

            if self.p_turn == 1:
                await interaction.response.edit_message(content = f"Winner {self.player2.name}!", view = self)
            elif self.p_turn == 2:
                await interaction.response.edit_message(content = f"Winner {self.player1.name}!", view = self)

            await interaction.followup.send(f"https://tenor.com/view/minions-gif-26254840")

    @discord.ui.button(label = '⠀', style = discord.ButtonStyle.grey, row = 2)
    async def btn8_callback(self, interaction: discord.Interaction, button: Button):
        if self.p_turn == 1 and interaction.user == self.player1:
            button.label = "X"
            self.g_space8 = 1
            button.disabled = True
            button.style = discord.ButtonStyle.red
        elif self.p_turn == 2 and interaction.user == self.player2:
            button.label = "O"
            self.g_space8 = 2
            button.disabled = True
            button.style = discord.ButtonStyle.green
        else:
            if self.p_turn == 1:
                await interaction.response.edit_message(content = f"Tic-Tac-Toe {self.player2.name} vs {self.player1.name}\n{str(self.player1.name).upper()}'s turn.")
            elif self.p_turn == 2:
                await interaction.response.edit_message(content = f"Tic-Tac-Toe {self.player2.name} vs {self.player1.name}\n{str(self.player2.name).upper()}'s turn.")

        end = self.check_win()

        if end == False:
            if self.p_turn == 1:
                await interaction.response.edit_message(content = f"Tic-Tac-Toe {self.player2.name} vs {self.player1.name}\n{self.player1.name}'s turn.", view = self)
            elif self.p_turn == 2:
                await interaction.response.edit_message(content = f"Tic-Tac-Toe {self.player2.name} vs {self.player1.name}\n{self.player2.name}'s turn.", view = self)
        else:
            for button in self.children:
                button.disabled = True

            if self.p_turn == 1:
                await interaction.response.edit_message(content = f"Winner {self.player2.name}!", view = self)
            elif self.p_turn == 2:
                await interaction.response.edit_message(content = f"Winner {self.player1.name}!", view = self)

            await interaction.followup.send(f"https://tenor.com/view/minions-gif-26254840")

    @discord.ui.button(label = '⠀', style = discord.ButtonStyle.grey, row = 2)
    async def btn9_callback(self, interaction: discord.Interaction, button: Button):
        if self.p_turn == 1 and interaction.user == self.player1:
            button.label = "X"
            self.g_space9 = 1
            button.disabled = True
            button.style = discord.ButtonStyle.red
        elif self.p_turn == 2 and interaction.user == self.player2:
            button.label = "O"
            self.g_space9 = 2
            button.disabled = True
            button.style = discord.ButtonStyle.green
        else:
            if self.p_turn == 1:
                await interaction.response.edit_message(content = f"Tic-Tac-Toe {self.player2.name} vs {self.player1.name}\n{str(self.player1.name).upper()}'s turn.")
            elif self.p_turn == 2:
                await interaction.response.edit_message(content = f"Tic-Tac-Toe {self.player2.name} vs {self.player1.name}\n{str(self.player2.name).upper()}'s turn.")

        end = self.check_win()

        if end == False:
            if self.p_turn == 1:
                await interaction.response.edit_message(content = f"Tic-Tac-Toe {self.player2.name} vs {self.player1.name}\n{self.player1.name}'s turn.", view = self)
            elif self.p_turn == 2:
                await interaction.response.edit_message(content = f"Tic-Tac-Toe {self.player2.name} vs {self.player1.name}\n{self.player2.name}'s turn.", view = self)
        else:
            for button in self.children:
                button.disabled = True

            if self.p_turn == 1:
                await interaction.response.edit_message(content = f"Winner {self.player2.name}!", view = self)
            elif self.p_turn == 2:
                await interaction.response.edit_message(content = f"Winner {self.player1.name}!", view = self)

            await interaction.followup.send(f"https://tenor.com/view/minions-gif-26254840")

class ttt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print("Tic-Tac-Toe module is loaded.")
        self.good_morning_message.start()


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
            view = TTTView()

            embed1 = discord.Embed(title = f"{self.player1.name} has been challenged to a Tic-Tac-Toe game by {self.player2.name}",
                                    url = "https://google.com")
            embed2 = discord.Embed(url = "https://google.com")
            embed1.set_image(url = f'{self.player1.display_avatar}')
            embed2.set_image(url = f'{self.player2.display_avatar}')
            await ctx.send(embeds = [embed1, embed2])

            await ctx.send(f"https://tenor.com/view/yu-gi-oh-duel-yugi-anime-gif-7357665")
            await ctx.send(f"Tic-Tac-Toe {self.player1.name} vs {self.player2.name}", view = view)
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