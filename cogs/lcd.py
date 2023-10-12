import discord
import requests
import random
import time
import platform
from discord.ext import commands, tasks

if platform.system() == "Windows":
    async def setup(bot):
        # await bot.add_cog(lcd(bot))
        pass

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
        # await bot.add_cog(lcd(bot))
        pass


    class lcd(commands.Cog):
        def __init__(self, bot):
            self.bot = bot
        
        display = LCD()

        i_msg = ''
        weather = ''
        time = ''


        @commands.Cog.listener()
        async def on_ready(self):
            print("lcd module is loaded.")
            self.get_the_weather.start()
            self.refresh_lcd.start()


        @tasks.loop(seconds = 1)
        async def refresh_lcd(self):
            # Change the time every minute
            if time.strftime("%H:%M") == self.time:
                return

            # Put the day of the week on the first line
            if time.strftime("%H:%M") == "00:00":
                days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                self.i_msg = days_of_week[time.localtime().tm_wday]

            # Turn off the display at 23:30
            if time.strftime("%H:%M") == "23:30":
                self.display.backlight(turn_on = False)

            # Turn on the display at 07:00
            if time.strftime("%H:%M") == "07:00":
                self.display.backlight(turn_on = True)

            # Do not update the display if it is turned off
            if self.display.backlight_status == False:
                return

            self.time = str(time.strftime("%H:%M"))

            line1 = self.i_msg
            line2 = self.weather + ' ' + self.time

            try:
                self.display.text(f"{line1}", 1)
                self.display.text(f"{line2}", 2)
            except Exception as e:
                print(e)
            finally:
                pass


        @tasks.loop(minutes = 10)
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
               # weather_details = api_json["weather"]
               # weather_description = weather_details[0]["description"]

                self.weather = f'{current_temperature_celsiuis}({feels_like_temp_celsius})C'
                return
            else:
                print("Can't find the city you are looking for.")
                return


        @commands.command(  name = 'lcd',
                            help = 'The bot will print your message in undeadko\'s home. You have 16 symbols.',
                            brief = '- Prints your 16 symbol message on an LCD screen.')
        async def display_message(self, ctx, *args):
            # Do not update the display if it is turned off
            if self.display.backlight_status == False:
                await ctx.send(f"The Display is off.")
                return

            self.i_msg = ''
            for arg in args:
                self.i_msg += arg + " "

            if len(self.i_msg) > 16:
                await ctx.send(f"The message is longer than 16 symbols.")
                self.i_msg = self.i_msg[0:16]

            line1 = self.i_msg
            line2 = self.weather + ' ' + self.time

            try:
                self.display.text(f"{line1}", 1)
                self.display.text(f"{line2}", 2)

                # await ctx.message.delete()
                await ctx.send(f"The display currently shows:\n{line1}\n{line2}")
            except Exception as e:
                print(e)
            finally:
                pass


        @commands.command(  name = 'lcd_off',
                            help = 'Turns the LCD display off.',
                            brief = 'Turns the LCD display off.')
        async def turn_off_lcd(self, ctx):
            try:
                #Send command to turn off the display
                self.display.backlight(turn_on = False)

                await ctx.reply("LDC screen is off.")
            except Exception as e:
                print(e)


        @commands.command(  name = 'lcd_on',
                            help = 'Turns the LCD display on.',
                            brief = 'Turns the LCD display on.')
        async def turn_on_lcd(self, ctx):
            try:
                #Send command to turn on the display
                self.display.backlight(turn_on = True)

                await ctx.reply("LDC screen is on.")
            except Exception as e:
                print(e)
