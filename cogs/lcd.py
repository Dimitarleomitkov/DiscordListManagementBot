import discord
import random
import time
import platform
from discord.ext import commands

if platform.system() == "Windows":
    async def setup(bot):
        await bot.add_cog(lcd(bot))

    class lcd(commands.Cog):
        def __init__(self, bot):
            self.bot = bot

        @commands.Cog.listener()
        async def on_ready(self):
            print("lcd module is loaded.")
else:
    from keys import weatherAPIKey
    from signal import signal, SIGTERM, SIGHUP, pause
    from rpi_lcd import LCD


    async def setup(bot):
        await bot.add_cog(lcd(bot))


    class lcd(commands.Cog):
        def __init__(self, bot):
            self.bot = bot
            self.refresh_lcd.start()
            self.get_the_weather.start()
        
        display = LCD()

        i_msg = ''
        weather = ''
        time = ''


        @commands.Cog.listener()
        async def on_ready(self):
            print("lcd module is loaded.")


        @tasks.loop(seconds = 60.0)
        async def refresh_lcd(self):
            time = time.strftime("%H:%M")

            line1 = self.i_msg[0:16]
            line2 = weather + time
            
            try:
                self.display.text(f"{line1}", 1)
                self.display.text(f"{line2}", 2)
            except Exception as e:
                print(e)
            finally:
                pass


        @tasks.loop(minutes = 30.0)
        async def get_the_weather(self):
            base_url = "http://api.openweathermap.org/data/2.5/weather?"
            language = "&lang=en"
            city_name = "Sofia"
            complete_url = base_url + "appid=" + weatherAPIKey + "&q=" + city_name + language
            response = requests.get(complete_url)
            api_json = response.json()

            if (api_json["cod"] != "404"):
                main_info = api_json["main"]
                current_temperature = main_info["temp"]
                current_temperature_celsiuis = str(round(current_temperature - 273.15))
                feels_like_temp = main_info["feels_like"]
                feels_like_temp_celsius = str(round(feels_like_temp - 273.15))
                weather_details = api_json["weather"]
                weather_description = weather_details[0]["description"]

                self.weather = f'{weather_description} {current_temperature_celsiuis}({feels_like_temp_celsius})'

                return
            else:
                print("Can't find the city you are looking for.")
                return


        @commands.command(  name = 'lcd',
                            help = 'The bot will print your message in undeadko\'s home. You have 16 symbols.',
                            brief = '- Prints your 16 symbol message on an LCD screen.')
        async def display_message(self, ctx, *args):
            for arg in args:
                self.i_msg += arg + " "
            
            if len(self.i_msg) > 16:
                await ctx.send(f"The message is longer than 16 symbols.")
                self.i_msg = self.i_msg[0:16]
            
            line1 = self.i_msg[0:16]
            line2 = weather + time
            
            try:
                self.display.text(f"{line1}", 1)
                self.display.text(f"{line2}", 2)
                
                await ctx.message.delete()
            except Exception as e:
                print(e)
            finally:
                pass
                

        @commands.command(  name = 'lcd_off',
                            help = 'Turns the LCD display off.',
                            brief = 'Turns the LCD display off.')
        async def turn_off_lcd(self, ctx):
            try:
                #Send command to turn off the display(0x08)
                self.display.command(0x08)

                await ctx.reply("LDC screen is off.")
            except Exception as e:
                print(e)
