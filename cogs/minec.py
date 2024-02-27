import discord
import random
from discord.ui import Button, View
from discord.ext import commands, tasks


async def setup(bot):
    await bot.add_cog(minec(bot))


class minec(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


#     @commands.Cog.listener()
#     async def on_ready(self):
#         print("Mines Clear module is loaded.")


#     @commands.Cog.listener()
#     async def on_button_click(self, interaction):
#         if isinstance(interaction.component, MinesClearButton):
#             print("CLICKED!")
#             view = interaction.view
#             await view.button_callback(interaction.component, interaction)


#     @commands.command(  name = 'minec',
#                         help = '>minec @challenged',
#                         brief = '- Start a new game of Mines Clear with someone.')
#     async def minec_new_game(self, ctx, challenged: discord.User = None, rows: int = 5, cols: int = 5):
#         if challenged == None:
#             await ctx.send("You need to challenge someone.\n>minec @challenged")
#             return

#         if cols > 30 or rows > 30:
#             await ctx.send("Columns need to be maximum 30. Rows need to be maximum 30\n>minec @challenged 30 30")
#             return

#         await ctx.message.delete()
        
#         try:
#             embed1 = discord.Embed(title = f"{challenged.name} has been challenged to a Mines Clear game by {ctx.author.name}")
#             embed2 = discord.Embed()
#             embed1.set_image(url = f'{challenged.display_avatar}')
#             embed2.set_image(url = f'{ctx.author.display_avatar}')
#             # await ctx.send(embeds = [embed1, embed2])
#             # await ctx.send(f"https://tenor.com/view/corre-run-running-explosion-gif-13415443")
#             embed3 = discord.Embed(title = "Click me!", description = "This is a clickable box.", color = discord.Color.grey(), url = "http://a.co"
#         )

#         except Exception as e:
#             text_chan = self.bot.get_channel(548554244932894750)
#             await text_chan.send(f"[Mines Clear]\n{e}")
#             return
