import discord
import random
from discord.ext import commands
from discord.ui import Button, View


async def setup(bot):
    await bot.add_cog(MinesweeperCog(bot))


class MinesweeperCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mines_left = 0


    @commands.Cog.listener()
    async def on_ready(self):
        print("Minesweeper module is loaded.")


    @commands.command(  name = 'minesw',
                        help = '>minesw r c',
                        brief = '- Start a new game of Minesweeper.')
    async def minesweeper(self, ctx, rows: int = 10, columns: int = 10):
        if rows < 1 or rows > 22 or columns < 1 or columns > 22:
            await ctx.send("Grid size should be between 1x1 and 22x22.")
            return

        total_cells = rows * columns
        total_mines = total_cells // 4

        if total_mines < 1:
            total_mines = 1

        try:
            view = ControlsView(rows, columns, total_mines)

            await ctx.send(f"Mine Field {total_mines} / {total_mines}:\n{view.print_game_space()}", view = view)
        except Exception as e:
            text_chan = self.bot.get_channel(548554244932894750)
            await text_chan.send(f"[Minesweeper]\n{e}")
            
            return


class ControlsView(View):
    def __init__(self, rows, columns, total_mines):
        super().__init__(timeout = 24 * 60 * 60)

        self.rows = rows
        self.columns = columns
        self.total_mines = total_mines
        self.mines_left = total_mines
        self.marker = [0, 0]
        self.mine_field = self.create_minefield(columns, rows, total_mines)
        self.gamespace = self.create_gamefield(columns, rows)


    @discord.ui.button(label = '\u200B', style = discord.ButtonStyle.grey, row = 0, disabled = True)
    async def ebtn1_callback(self, interaction: discord.Interaction, button: Button):
        return


    @discord.ui.button(custom_id = 'sweep_btn', emoji = '👆🏻', style = discord.ButtonStyle.grey, row = 0, disabled = False)
    async def btn1_callback(self, interaction: discord.Interaction, button: Button):
        try:
            button.style = discord.ButtonStyle.green

            for child in self.children:
                if child.custom_id == 'mark_btn':
                    child.style = discord.ButtonStyle.grey

            await interaction.response.edit_message(content = f"{self.print_game_space()}", view = self)
        except Exception as e:
            print(e)


    @discord.ui.button(custom_id = 'action_btn', emoji = '🔘', style = discord.ButtonStyle.grey, row = 0, disabled = False)
    async def btn2_callback(self, interaction: discord.Interaction, button: Button):
        try:
            self.reveal_all()

            await interaction.response.edit_message(content = f"{self.print_game_space()}", view = self)

            self.hide_all()
        except Exception as e:
            print(e)


    @discord.ui.button(custom_id = 'mark_btn', emoji = '🚩', style = discord.ButtonStyle.grey, row = 0, disabled = False)
    async def btn3_callback(self, interaction: discord.Interaction, button: Button):
        try:
            button.style = discord.ButtonStyle.green

            for child in self.children:
                if child.custom_id == 'sweep_btn':
                    child.style = discord.ButtonStyle.grey

            await interaction.response.edit_message(content = f"{self.print_game_space()}", view = self)
        except Exception as e:
            print(e)


    @discord.ui.button(label = '\u200B', style = discord.ButtonStyle.grey, row = 0, disabled = True)
    async def ebtn2_callback(self, interaction: discord.Interaction, button: Button):
        return


    @discord.ui.button(label = '\u200B', style = discord.ButtonStyle.grey, row = 1, disabled = True)
    async def ebtn3_callback(self, interaction: discord.Interaction, button: Button):
        return


    @discord.ui.button(label = '\u200B', style = discord.ButtonStyle.grey, row = 1, disabled = True)
    async def btn4_callback(self, interaction: discord.Interaction, button: Button):
        return


    @discord.ui.button(custom_id = 'up_btn', emoji = '🔼', style = discord.ButtonStyle.grey, row = 1, disabled = False)
    async def btn5_callback(self, interaction: discord.Interaction, button: Button):
        try:
            if self.marker[0] > 0:
                self.marker[0] -= 1

            await interaction.response.edit_message(content = f"{self.print_game_space()}", view = self)
        except Exception as e:
            print(e)


    @discord.ui.button(label = '\u200B', style = discord.ButtonStyle.grey, row = 1, disabled = True)
    async def btn6_callback(self, interaction: discord.Interaction, button: Button):
        return


    @discord.ui.button(label = '\u200B', style = discord.ButtonStyle.grey, row = 1, disabled = True)
    async def ebtn4_callback(self, interaction: discord.Interaction, button: Button):
        return


    @discord.ui.button(label = '\u200B', style = discord.ButtonStyle.grey, row = 2, disabled = True)
    async def ebtn5_callback(self, interaction: discord.Interaction, button: Button):
        return


    @discord.ui.button(custom_id = 'left_btn', emoji = '⬅', style = discord.ButtonStyle.grey, row = 2, disabled = False)
    async def btn7_callback(self, interaction: discord.Interaction, button: Button):
        try:
            if self.marker[1] > 0:
                self.marker[1] -= 1

            await interaction.response.edit_message(content = f"{self.print_game_space()}", view = self)
        except Exception as e:
            print(e)


    @discord.ui.button(custom_id = 'down_btn', emoji = '🔽', style = discord.ButtonStyle.grey, row = 2, disabled = False)
    async def btn8_callback(self, interaction: discord.Interaction, button: Button):
        try:
            if self.marker[0] < self.columns - 1:
                self.marker[0] += 1

            await interaction.response.edit_message(content = f"{self.print_game_space()}", view = self)
        except Exception as e:
            print(e)


    @discord.ui.button(custom_id = 'right_btn', emoji = '➡️', style = discord.ButtonStyle.grey, row = 2, disabled = False)
    async def btn9_callback(self, interaction: discord.Interaction, button: Button):
        try:
            if self.marker[1] < self.rows - 1:
                self.marker[1] += 1

            await interaction.response.edit_message(content = f"{self.print_game_space()}", view = self)
        except Exception as e:
            print(e)


    @discord.ui.button(label = '\u200B', style = discord.ButtonStyle.grey, row = 2, disabled = True)
    async def ebtn6_callback(self, interaction: discord.Interaction, button: Button):
        return


    def print_game_space(self):
        game_field = '```'

        for row in range(self.rows):
            for col in range(self.columns):
                if [row, col] == self.marker:
                    game_field += 'O '
                elif self.gamespace[row][col] == '■':
                    game_field += '■ '
                else:
                    game_field += self.mine_field[row][col] + ' '

            game_field += '\n'

        game_field += '```'

        return game_field


    def create_minefield(self, columns, rows, total_mines):
        grid = [['\u200B' for _ in range(columns)] for _ in range(rows)]

        result = random.randint(0, 4)

        if result == 0:
            grid[0][0] = '¤'
        elif result == 1:
            grid[0][1] = '¤'
        elif result == 2:
            grid[1][0] = '¤'
        elif result == 3:
            grid[1][1] = '¤'

        # Place mines randomly
        for _ in range(total_mines - 1):
            while True:
                row = random.randint(0, rows - 1)
                col = random.randint(0, columns - 1)
                if grid[row][col] != '¤':
                    grid[row][col] = '¤'
                    break

        # # Calculate numbers for adjacent cells
        for row in range(rows):
            for col in range(columns):
                if grid[row][col] != '¤':
                    count = 0
                    
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if 0 <= row + dr < rows and 0 <= col + dc < columns and grid[row + dr][col + dc] == '¤':
                                count += 1
                    
                    grid[row][col] = self.number_to_word(count)

        return grid


    def create_gamefield(self, columns, rows):
        grid = [['■' for _ in range(columns)] for _ in range(rows)]

        return grid


    def number_to_word(self, number):
        if number == 1:
            return '1'
        elif number == 2:
            return '2'
        elif number == 3:
            return '3'
        elif number == 4:
            return '4'
        elif number == 5:
            return '5'
        elif number == 6:
            return '6'
        elif number == 7:
            return '7'
        elif number == 8:
            return '8'
        else:
            return ' '


    def reveal_all(self):
        self.marker = [-1, -1]
        for row in range(self.rows):
            for col in range(self.columns):
                self.gamespace[row][col] = '#'


    def hide_all(self):
        self.marker = [0, 0]
        for row in range(self.rows):
            for col in range(self.columns):
                self.gamespace[row][col] = '■'