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
        self.animals_URL = 'https://some-random-api.ml/img/'
        self.options_animals = ("bird", "cat", "dog", "fox",\
                                "kangaroo", "koala", "panda",\
                                "pikachu", "raccoon", "red_panda",\
                                "whale")
        self.animal_facts_URL = 'https://some-random-api.ml/facts/'
        self.options_animal_facts = ("bird", "cat", "dog", "fox",\
                                    "kangaroo", "koala", "panda",\
                                    "raccoon", "red_panda")
        self.anime_gif_URL = 'https://some-random-api.ml/animu/'
        self.options_anime_cmds = ("face-palm", "hug", "pat", "wink")


    def get_animal_img(self, animal_parameter):
        animal_img_url = requests.get(self.animals_URL + animal_parameter).json()["link"]

        return animal_img_url


    def get_animal_fact(self, animal_parameter):
        URL = self.animal_facts_URL

        if animal_parameter == "kangaroo" or\
            animal_parameter == "raccoon" or\
            animal_parameter == "red_panda":
            URL = "https://some-random-api.ml/animal/"

        animal_fact = requests.get(URL + animal_parameter).json()["fact"]

        return animal_fact


    def get_anime_img(self, anime_parameter):
        anime_gif_URL = requests.get(self.anime_gif_URL + anime_parameter).json()["link"]

        return anime_gif_URL


    @commands.Cog.listener()
    async def on_ready(self):
        print("rAPI module is loaded.")


    @commands.command(  name = 'ranimal',
                        help = 'The bot will get a random animal picture. Supports\
                                "bird", "cat", "dog", "fox",\
                                "kangaroo", "koala", "panda",\
                                "pikachu", "raccoon", "red_panda",\
                                "whale".',
                        brief = '- Gets a random animal picture. Supports\
                                "bird", "cat", "dog", "fox",\
                                "kangaroo", "koala", "panda",\
                                "pikachu", "raccoon", "red_panda",\
                                "whale".')
    async def animal_img(self, ctx, animal = None):
        if not animal in self.options_animals:
            await ctx.send(f"I can only give you pictures of {self.options_animals}")

        await ctx.message.delete()

        if animal is None:
            animal = random.choice(self.options_animals)

        animal_img = self.get_animal_img(animal)
        text_chan = self.bot.get_channel(1066377134836285480)

        embed = discord.Embed()
        embed.set_image(url = animal_img)

        await text_chan.send(f"{ctx.author.mention} requested:", embed = embed)


    @commands.command(  name = 'animal_fact',
                        help = 'The bot will get a random animal fact. Supports\
                                "bird", "cat", "dog", "fox",\
                                "kangaroo", "koala", "panda",\
                                "raccoon", "red_panda"',
                        brief = '- Gets a random animal fact. Supports\
                                "bird", "cat", "dog", "fox",\
                                "kangaroo", "koala", "panda",\
                                "raccoon", "red_panda"')
    async def animal_fact(self, ctx, animal = None):
        if not animal in self.options_animal_facts:
            await ctx.send(f"I can only give you facts about {self.options_animal_facts}")

        await ctx.message.delete()

        if animal is None:
            animal = random.choice(self.options_animal_facts)

        animal_fact = self.get_animal_fact(animal)
        text_chan = self.bot.get_channel(1066377134836285480)

        if animal == "fox":
            await text_chan.send(f"{ctx.author.mention}, a fun fact about {animal}es:\n{animal_fact}")
        else:
            await text_chan.send(f"{ctx.author.mention}, a fun fact about {animal}s:\n{animal_fact}")


    @commands.command(  name = 'ranime',
                        help = 'The bot displays a random anime img/gif. Supports\
                                "face-palm", "hug", "pat", "wink"',
                        brief = 'The bot displays a random anime img/gif. Supports\
                                "face-palm", "hug", "pat", "wink"')
    async def anime_gif(self, ctx, cmd, target = None):
        if not cmd in self.options_anime_cmds:
            await ctx.send(f"I know only {self.options_anime_cmds}")
            return

        await ctx.message.delete()

        anime_img = self.get_anime_img(cmd)

        print(anime_img)

        embed = discord.Embed()
        embed.set_image(url = anime_img)

        if target is None:
            await ctx.send(f'{anime_img}')
        elif cmd == "face-palm":
            await ctx.send(f'{ctx.message.author.mention} {cmd}s at {target}', embed = embed)
        else:
            await ctx.send(f'{ctx.message.author.mention} {cmd}s {target}', embed = embed)