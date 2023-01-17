import discord
from discord.ext import commands


async def setup(bot):
    await bot.add_cog(binary_conversion(bot))


class binary_conversion(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print("binary_conversion module is loaded.")


    @commands.command(  name = 'to_binary',
                        help = 'Converts the message to binary and prints it.',
                        brief = '- Converts the message to binary and prints it.')
    async def to_binary_func(self, ctx, *args):
        input_string = " ".join(args)
        result = ''.join(format(ord(i), '08b') for i in input_string)

        await ctx.send(result)


    @commands.command(  name = 'binary_to_text',
                        help = 'Converts the message from binary to text and prints it.',
                        brief = '- Converts the message from binary to text and prints it.')
    async def bibnary_to_text(self, ctx, input_binary):
        def BinaryToDecimal(binary):
            int_string = int(binary, 2)
            return int_string

        str_data = ''
        for i in range(0, len(input_binary), 8):
            temp_data = input_binary[i:i + 8]
            decimal_data = BinaryToDecimal(temp_data)
            str_data = str_data + chr(decimal_data)
        
        await ctx.send(str_data)



