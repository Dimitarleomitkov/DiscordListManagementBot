import discord
import requests
import json
import datetime
import pytz
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
                        brief = '- Displays the weather at the given location.')
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
            await weather_func(ctx, api_json)
            return
        else:
            await ctx.send("Can't find the city you are looking for.")
            return


    @commands.command(  name = 'weather_compare',
                        help = 'The bot will display the weather comparison between Sofia, Plovdiv and Dimitrovgrad.',
                        brief = '- Displays the weather comparison between Sofia, Plovdiv and Dimitrovgrad.')
    async def weather_comp(self, ctx):
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        language = "&lang=en"
        city_name = ["Dimitrovgrad,BG", "Plovdiv", "Sofia"]

        api_jsons = []
        for city in city_name:
            complete_url = base_url + "appid=" + weatherAPIKey + "&q=" + city + language
            response = requests.get(complete_url)
            api_jsons.append(response.json())

        if (api_jsons[0]["cod"] != "404" and api_jsons[1]["cod"] != "404" and api_jsons[2]["cod"] != "404"):
            await weather_comp_func(ctx, api_jsons)
            return
        else:
            await ctx.send("Something went wrong :(")
            return


async def weather_func(ctx, weather_json):
    main_info = weather_json["main"]
    current_temperature = main_info["temp"]
    current_temperature_celsiuis = str(round(current_temperature - 273.15))
    feels_like_temp = main_info["feels_like"]
    feels_like_temp_celsius = str(round(feels_like_temp - 273.15))
    current_pressure = main_info["pressure"]
    current_humidity = main_info["humidity"]
    # sea_level = main_info["sea_level"]
    # grnd_level = main_info["grnd_level"]
    weather_details = weather_json["weather"]
    weather_description = weather_details[0]["description"]
    json_icon = weather_details[0]["icon"]
    city_name = weather_json["name"]
    sys_info = weather_json["sys"]
    country = sys_info["country"]

    BG_time_zone = pytz.timezone("Europe/Sofia")
    sunrise_time = datetime.datetime.fromtimestamp(sys_info["sunrise"], tz = BG_time_zone).strftime('%Y-%m-%d %H:%M:%S')
    sunset_time = datetime.datetime.fromtimestamp(sys_info["sunset"], tz = BG_time_zone).strftime('%Y-%m-%d %H:%M:%S')

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
    
    embed = discord.Embed(title = f"Weather in {city_name}, {country}",
                          color = ctx.guild.me.top_role.color,
                          timestamp = ctx.message.created_at)
    embed.add_field(name = "Coordinates",
                    value = f"Logitude: **{logitude}**\n\
                                Latitude: **{latitude}**",
                    inline = False)

    embed.add_field(name = "Descripition",
                    value = f"**{weather_description}** {weather_icon}\n\
                    **sunrise** at :sunrise:: {sunrise_time}\n\
                    **sunset** at :city_dusk:: {sunset_time}",
                    inline = False)

    embed.add_field(name = "Temperature (feels like)",
                    value = f"**{current_temperature_celsiuis}({feels_like_temp_celsius})°C** \
                            / **{(float(current_temperature_celsiuis) * 1.8 + 32):.2f}({(float(feels_like_temp_celsius) * 1.8 + 32):.2f})°F** \
                            / **{current_temperature}({feels_like_temp})°K**",
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

async def weather_comp_func(ctx, weather_jsons):
    temps = []
    fl_temps = []
    humidities = []
    descriptions = []
    icons = []
    city_names = []
    wind_speeds = []


    for weather_json in weather_jsons:
        main_info = weather_json["main"]

        current_temperature = main_info["temp"]
        temps.append(str(round(current_temperature - 273.15)))

        feels_like_temp = main_info["feels_like"]
        fl_temps.append((round(feels_like_temp - 273.15)))

        humidities.append(main_info["humidity"])

        weather_details = weather_json["weather"]

        descriptions.append(weather_details[0]["description"])

        city_names.append(weather_json["name"])

        wind_speeds.append(weather_json["wind"]["speed"])

        json_icon = weather_details[0]["icon"]

        if (json_icon.startswith("01")):
            icons.append(":sunny:")
        elif (json_icon.startswith("02")):
            icons.append(":white_sun_small_cloud:")
        elif (json_icon.startswith("03")):
            icons.append(":white_sun_cloud:")
        elif (json_icon.startswith("04")):
            icons.append(":cloud:")
        elif (json_icon.startswith("09")):
            icons.append(":cloud_rain:")
        elif (json_icon.startswith("10")):
            icons.append(":white_sun_rain_cloud:")
        elif (json_icon.startswith("11")):
            icons.append(":thunder_cloud_rain:")
        elif (json_icon.startswith("13")):
            icons.append(":snowflake:")
        elif (json_icon.startswith("50")):
            icons.append(":fog:")
        else:
            icons.append(":boom:")

    
    embed = discord.Embed(title = f"{city_names[0]} / {city_names[1]} / {city_names[2]}, BG",
                          color = ctx.guild.me.top_role.color,
                          timestamp = ctx.message.created_at)

    embed.add_field(name = "Descripition",
                    value = f"**{descriptions[0]}** {icons[0]} / **{descriptions[1]}** {icons[1]} / **{descriptions[2]}** {icons[2]}",
                    inline = False)

    embed.add_field(name = "Temperature (feels like)",
                    value = f"**{temps[0]}({fl_temps[0]})°C / {temps[1]}({fl_temps[1]})°C / {temps[2]}({fl_temps[2]})°C**",
                    inline = False)

    embed.add_field(name = "Wind speeds",
                    value = f"**{wind_speeds[0]}m/s / {wind_speeds[1]}m/s / {wind_speeds[2]}m/s**",
                    inline = False)

    embed.set_thumbnail(url = "https://i.ibb.co/CMrsxdX/weather.png")
    embed.set_footer(text = f"Requested by {ctx.author.name}")

    await ctx.send(embed = embed)