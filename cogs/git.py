import discord
from discord.ext import commands
import git as Git
import pathlib
import os
import cogs.lrlul_cogs as Cogs
import sys
import subprocess
import platform
import time


async def setup(bot):
    await bot.add_cog(git(bot))
    

class git(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print("Git module is loaded.")


    @commands.command(  name = 'server_update',
                        help = 'Pulls the code from the repo and reloads all cogs.',
                        brief = 'Pulls the code from the repo and reloads all cogs.')
    async def update_server(self, ctx):
        text_chan = self.bot.get_channel(548554244932894750)
        
        await self.git_pull_func(ctx)

        for filename in os.listdir(pathlib.Path(__file__).parent):
            if filename.endswith(".py"):
                # cut off the .py from the file name
                cog = f"{filename[:-3]}"
                # reload the cog
                await self.bot.unload_extension(f"cogs.{cog}")
                await self.bot.load_extension(f"cogs.{cog}")

        await text_chan.send("Update successful.")


    @commands.command(  name = 'server_restart',
                        help = 'Restarts the bot.',
                        brief = 'Restarts the bot.')
    async def restart_server(self, ctx):
        text_chan = self.bot.get_channel(548554244932894750)

        if platform.system() != "Windows":
            await text_chan.send("Booting a new instance of me...")
            await text_chan.send(f"Current path {pathlib.Path(__file__)}")

            
            try:
                subprocess.run(f"{pathlib.Path(__file__)}../boot.bash")
            except Exception as e:
                await text_chan.send(e)

            time.sleep(1)
            await text_chan.send("Turning off...")
            
        await text_chan.send("Restarting...")
        # sys.exit("Bye!")


    @commands.command(  name = 'git_pull',
                        help = 'Performs git pull.',
                        brief = 'Performs git pull.')
    async def git_pull_func (self, ctx):
        text_chan = self.bot.get_channel(548554244932894750)

        try:
            git_dir = pathlib.Path(__file__).parent.parent.resolve()
            g = Git.cmd.Git(git_dir)
            msg = g.pull()
            await text_chan.send(str(msg))
        except Exception as e:
            await text_chan.send(e)




