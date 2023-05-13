import discord
import requests
import json
import random
from discord.ext import commands


async def setup(bot):
    await bot.add_cog(rAPI(bot))


class rAPI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.animals_URL = 'https://api.animality.xyz/img/'
        self.options_animals = ("cat",
                                "dog",
                                "bird",
                                "panda",
                                "redpanda",
                                "koala",
                                "fox",
                                "whale",
                                "dolphin",
                                "kangaroo",
                                "bunny",
                                "lion",
                                "bear",
                                "frog",
                                "duck",
                                "penguin",
                                "axolotl",
                                "capybara")
        self.animal_facts_URL = 'https://api.animality.xyz/fact/'
        self.options_animal_facts = ("cat",
                                        "dog",
                                        "bird",
                                        "panda",
                                        "redpanda",
                                        "koala",
                                        "fox",
                                        "whale",
                                        "dolphin",
                                        "kangaroo",
                                        "bunny",
                                        "lion",
                                        "bear",
                                        "frog",
                                        "duck",
                                        "penguin",
                                        "axolotl",
                                        "capybara")


    def get_animal_img(self, animal_parameter):
        animal_img_url = requests.get(self.animals_URL + animal_parameter).json()["link"]

        return animal_img_url


    def get_animal_fact(self, animal_parameter):
        URL = self.animal_facts_URL

        animal_fact = requests.get(URL + animal_parameter).json()["fact"]

        return animal_fact


    @commands.Cog.listener()
    async def on_ready(self):
        print("rAPI module is loaded.")


    @commands.command(  name = 'ranimal',
                        help = 'The bot will get a random animal picture. Supports\
                                "cat", "dog", "bird", "panda", "redpanda", "koala",\
                                "fox", "whale", "dolphin", "kangaroo", "bunny",\
                                "lion", "bear", "frog", "duck", "penguin", "axolotl",\
                                "capybara"',
                        brief = '- Gets a random animal picture. Supports\
                                "cat", "dog", "bird", "panda", "redpanda", "koala",\
                                "fox", "whale", "dolphin", "kangaroo", "bunny",\
                                "lion", "bear", "frog", "duck", "penguin", "axolotl",\
                                "capybara"')
    async def animal_img(self, ctx, animal = None):
        if not animal in self.options_animals:
            await ctx.send(f"I can only give you pictures of {self.options_animals}")

        await ctx.message.delete()

        msg = ""

        if animal is None:
            animal = random.choice(self.options_animals)
            msg = f"{ctx.author.mention} requested a random animal picture. I chose {animal}:"
        else:
            msg = f"{ctx.author.mention} requested a picture of {animal}:"

        animal_img = self.get_animal_img(animal)
        text_chan = self.bot.get_channel(1066377134836285480)

        embed = discord.Embed()
        embed.set_image(url = animal_img)

        bot_msg = await text_chan.send(msg, embed = embed)

        if animal == "duck":
            await bot_msg.add_reaction("<:hueduck:973273982776279080>")


    @commands.command(  name = 'animal_fact',
                        help = 'The bot will get a random animal fact. Supports\
                                "cat", "dog", "bird", "panda", "redpanda", "koala",\
                                "fox", "whale", "dolphin", "kangaroo", "bunny",\
                                "lion", "bear", "frog", "duck", "penguin", "axolotl",\
                                "capybara"',
                        brief = '- Gets a random animal fact. Supports\
                                "cat", "dog", "bird", "panda", "redpanda", "koala",\
                                "fox", "whale", "dolphin", "kangaroo", "bunny",\
                                "lion", "bear", "frog", "duck", "penguin", "axolotl",\
                                "capybara"')
    async def animal_fact(self, ctx, animal = None):
        if not animal in self.options_animal_facts:
            await ctx.send(f"I can only give you facts about {self.options_animal_facts}")

        await ctx.message.delete()

        if animal is None:
            animal = random.choice(self.options_animal_facts)

        animal_fact = self.get_animal_fact(animal)
        text_chan = self.bot.get_channel(1066377134836285480)

        if animal == "fox":
            bot_msg = await text_chan.send(f"{ctx.author.mention}, a fun fact about {animal}es:\n{animal_fact}")
        elif animal == "bunny":
            bot_msg = await text_chan.send(f"{ctx.author.mention}, a fun fact about bunnies:\n{animal_fact}")
        elif animal == "axolotl":
            bot_msg = await text_chan.send(f"{ctx.author.mention}, a fun fact about axolots:\n{animal_fact}")
        else:
            bot_msg = await text_chan.send(f"{ctx.author.mention}, a fun fact about {animal}s:\n{animal_fact}")

        if animal == "duck":
            await bot_msg.add_reaction("<:hueduck:973273982776279080>")
