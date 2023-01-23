import discord
from animals import Animals
from discord.ext import commands


async def setup(bot):
    await bot.add_cog(animals(bot))


class animals(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    def get_animal_img(self, animal_parameter):
        animal = Animals(animal_parameter)

        return animal.image()


    def get_animal_fact(self, animal_parameter):
        animal = Animals(animal_parameter)

        return animal.fact()


    @commands.Cog.listener()
    async def on_ready(self):
        print("animals module is loaded.")


    @commands.command(  name = 'ranimal',
                        help = 'The bot will get a random animal picture.',
                        brief = '- Gets a random animal picture. Supports\
                        cat, dog, koala, fox, birb, red_panda, panda, racoon, kangaroo')
    async def animals_img(self, ctx, animal):
        await ctx.message.delete()

        animal_img = self.get_animal_img(animal)
        text_chan = self.bot.get_channel(1066377134836285480)

        embed = discord.Embed()
        embed.set_image(url = animal_img)

        await text_chan.send(f"{ctx.author.mention} requested:", embed = embed)


    @commands.command(  name = 'animal_fact',
                        help = 'The bot will get a random animal fact.',
                        brief = '- Gets a random animal fact. Supports\
                        cat, dog, koala, fox, birb, red_panda, panda, racoon, kangaroo')
    async def animals_fact(self, ctx, animal):
        await ctx.message.delete()

        animal_fact = self.get_animal_fact(animal)
        text_chan = self.bot.get_channel(1066377134836285480)

        await text_chan.send(f"{ctx.author.mention}, a fun fact about {animal}s:\n{animal_fact}")
