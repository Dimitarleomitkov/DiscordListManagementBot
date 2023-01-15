import discord
import requests
import json
from discord.ext import commands
from keys import weatherAPIKey


async def setup(bot):
    await bot.add_cog(weather(bot))

class weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("weather module is loaded.")

    @commands.command(  name = 'weather',
                        help = 'The bot will display the weather at the given location.',
                        brief = '- Displays at the weather at the given locationency.')
    async def weather(self, ctx, *args):
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        language = "&lang=en"
        city_name = ""

        for arg in args:
        	city_name += arg.capitalize() + " "

        complete_url = base_url + "appid=" + weatherAPIKey + "&q=" + city_name + language
        response = requests.get(complete_url)
        api_json = response.json()

        if (api_json["cod"] != "404"):
            await weather_func(ctx, api_json, city_name)
            return
        else:
            await ctx.send("Can't find the city you are looking for.")
            return


async def weather_func(ctx, weather_json, city_name):
    main_info = weather_json["main"]
    current_temperature = main_info["temp"]
    current_temperature_celsiuis = str(round(current_temperature - 273.15))
    current_pressure = main_info["pressure"]
    current_humidity = main_info["humidity"]
    weather_details = weather_json["weather"]
    weather_description = weather_details[0]["description"]
    json_icon = weather_details[0]["icon"]

    if (json_icon.startswith("01")):
        weather_icon = ":sunny:"
    elif (json_icon.startswith("02")):
        weather_icon = ":white_sun_small_cloud:"
    elif (json_icon.startswith("03")):
        weather_icon = ":white_sun_cloud:"
    elif (json_icon.startswith("04")):
        weather_icon = ":cloud:"
    elif (json_icon.startswith("09")):
        weather_icon = ":cloud_rain:"
    elif (json_icon.startswith("10")):
        weather_icon = ":white_sun_rain_cloud:"
    elif (json_icon.startswith("11")):
        weather_icon = ":thunder_cloud_rain:"
    elif (json_icon.startswith("13")):
        weather_icon = ":snowflake:"
    elif (json_icon.startswith("50")):
        weather_icon = ":fog:"
    else:
        weather_icon = ":boom:"

    logitude = weather_json["coord"]["lon"]
    latitude = weather_json["coord"]["lat"]

    wind_speed = weather_json["wind"]["speed"]
    
    embed = discord.Embed(title = f"Weather in {city_name}",
                          color = ctx.guild.me.top_role.color,
                          timestamp = ctx.message.created_at)
    embed.add_field(name = "Coordinates",
                    value = f"Logitude: **{logitude}**\n\
                                Latitude: **{latitude}**",
                    inline = False)

    embed.add_field(name = "Descripition",
                    value = f"**{weather_description}** {weather_icon}",
                    inline = False)

    embed.add_field(name = "Temperature(C)",
                    value = f"**{current_temperature_celsiuis}°C** \
                            / **{(float(current_temperature_celsiuis) * 1.8 + 32):.2f}°F** \
                            / **{current_temperature}°K**",
                    inline = False)

    embed.add_field(name = "Wind",
                    value = f"wind speed: **{wind_speed}m/s**",
                    inline = False)

    embed.add_field(name = "Humidity(%)",
                    value = f"**{current_humidity}%**",
                    inline = False)

    embed.add_field(name = "Atmospheric Pressure(hPa)",
                    value = f"**{current_pressure}hPa**",
                    inline = False)

    embed.set_thumbnail(url = "https://i.ibb.co/CMrsxdX/weather.png")
    embed.set_footer(text = f"Requested by {ctx.author.name}")

    await ctx.send(embed = embed)
