import discord
import os
import asyncio
import sys
import traceback
from keep_alive import *
from keys import TOKEN, COGS
from discord.ext import commands

INTENTS = discord.Intents.all()
INTENTS.members = True
bot = commands.Bot(command_prefix = '>', intents = INTENTS, case_insensitive = True)

# keep_alive()

@bot.event
async def on_command_error(ctx, error):
    text_chan = self.bot.get_channel(548554244932894750)

    await text_chan.send('Ignoring exception in command {}:'.format(ctx.command), file = sys.stderr)
    traceback.print_exception(type(error), error, error.__traceback__, file = sys.stderr)


async def load_extensions():
    for filename in os.listdir(COGS):
        if filename.endswith(".py"):
            # cut off the .py from the file name
            await bot.load_extension(f"cogs.{filename[:-3]}")


async def main():
    await load_extensions()
    await bot.start(TOKEN)

    # text_chan = self.bot.get_channel(548554244932894750)
    # await text_chan.send("I have powered up.")

asyncio.run(main())
