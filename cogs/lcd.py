import discord
import random
from discord.ext import commands
from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD

async def setup(bot):
    await bot.add_cog(lcd(bot))


class lcd(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    display = LCD()


    @commands.Cog.listener()
    async def on_ready(self):
        print("lcd module is loaded.")


    @commands.command(  name = 'lcd',
                        help = 'The bot will print your message in undeadko\'s home. You have 32 symbols.',
                        brief = '- Prints your 32 symbol message on an LCD screen.')
    async def display_message(self, ctx, *args):
        i_msg = ''
        for arg in args:
            i_msg += arg + " "
        
        if len(i_msg) > 32:
            await ctx.send(f"The message is longer than 32 symbols.")
            i_msg = i_msg[0:32]
        
        line1 = i_msg[0:16]
        line2 = i_msg[16:32]
        
        try:
            self.display.text(f"{line1}", 1)
            self.display.text(f"{line2}", 2)
            
            await ctx.message.delete()
            await ctx.reply(f"undeadko has your message.")
        except Exception as e:
            print(e)
        finally:
            pass
            
        