import discord
# import requests
# import json
# import datetime
# import dateutil.tz as dateutils
from discord.ext import commands


async def setup(bot):
    await bot.add_cog(food(bot))


class food(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        print("food module is loaded.")


    @commands.command(  name = 'food',
                        help = 'To be implemented.',
                        brief = '- To be implemented.')
    async def food(self, ctx, *args):
        await ctx.send("I do not know what to do. Undeadko still develops this. Tell him to finish it.")
        await ctx.send("The API is https://world.openfoodfacts.org/")




#         base_url = "http://api.openfoodmap.org/data/2.5/food?"
#         language = "&lang=en"
#         city_name = ""

#         for arg in args:
#         	city_name += arg.capitalize() + " "

#         complete_url = base_url + "appid=" + foodAPIKey + "&q=" + city_name + language
#         response = requests.get(complete_url)
#         api_json = response.json()

#         if (api_json["cod"] != "404"):
#             await food_func(ctx, api_json)
#             return
#         else:
#             await ctx.send("Can't find the city you are looking for.")
#             return


# async def food_func(ctx, food_json):
#     main_info = food_json["main"]
#     current_temperature = main_info["temp"]
#     current_temperature_celsiuis = str(round(current_temperature - 273.15))
#     feels_like_temp = main_info["feels_like"]
#     feels_like_temp_celsius = str(round(feels_like_temp - 273.15))
#     current_pressure = main_info["pressure"]
#     current_humidity = main_info["humidity"]
#     # sea_level = main_info["sea_level"]
#     # grnd_level = main_info["grnd_level"]
#     food_details = food_json["food"]
#     food_description = food_details[0]["description"]
#     json_icon = food_details[0]["icon"]
#     city_name = food_json["name"]
#     sys_info = food_json["sys"]
#     country = sys_info["country"]

#     BG_time_zone = dateutils.tzoffset('UTC', 60 * 60 * 2)
#     sunrise_time = datetime.datetime.fromtimestamp(sys_info["sunrise"], tz = BG_time_zone).strftime('%Y-%m-%d %H:%M:%S')
#     sunset_time = datetime.datetime.fromtimestamp(sys_info["sunset"], tz = BG_time_zone).strftime('%Y-%m-%d %H:%M:%S')

#     if (json_icon.startswith("01")):
#         food_icon = ":sunny:"
#     elif (json_icon.startswith("02")):
#         food_icon = ":white_sun_small_cloud:"
#     elif (json_icon.startswith("03")):
#         food_icon = ":white_sun_cloud:"
#     elif (json_icon.startswith("04")):
#         food_icon = ":cloud:"
#     elif (json_icon.startswith("09")):
#         food_icon = ":cloud_rain:"
#     elif (json_icon.startswith("10")):
#         food_icon = ":white_sun_rain_cloud:"
#     elif (json_icon.startswith("11")):
#         food_icon = ":thunder_cloud_rain:"
#     elif (json_icon.startswith("13")):
#         food_icon = ":snowflake:"
#     elif (json_icon.startswith("50")):
#         food_icon = ":fog:"
#     else:
#         food_icon = ":boom:"

#     logitude = food_json["coord"]["lon"]
#     latitude = food_json["coord"]["lat"]

#     wind_speed = food_json["wind"]["speed"]
    
#     embed = discord.Embed(title = f"Weather in {city_name}, {country}",
#                           color = ctx.guild.me.top_role.color,
#                           timestamp = ctx.message.created_at)
#     embed.add_field(name = "Coordinates",
#                     value = f"Logitude: **{logitude}**\n\
#                                 Latitude: **{latitude}**",
#                     inline = False)

#     embed.add_field(name = "Descripition",
#                     value = f"**{food_description}** {food_icon}\n\
#                     **sunrise** at :sunrise:: {sunrise_time}\n\
#                     **sunset** at :city_dusk:: {sunset_time}",
#                     inline = False)

#     embed.add_field(name = "Temperature (feels like)",
#                     value = f"**{current_temperature_celsiuis}({feels_like_temp_celsius})°C** \
#                             / **{(float(current_temperature_celsiuis) * 1.8 + 32):.2f}({(float(feels_like_temp_celsius) * 1.8 + 32):.2f})°F** \
#                             / **{current_temperature}({feels_like_temp})°K**",
#                     inline = False)

#     embed.add_field(name = "Wind",
#                     value = f"wind speed: **{wind_speed}m/s**",
#                     inline = False)

#     embed.add_field(name = "Humidity(%)",
#                     value = f"**{current_humidity}%**",
#                     inline = False)

#     embed.add_field(name = "Atmospheric Pressure(hPa)",
#                     value = f"**{current_pressure}hPa**",
#                     inline = False)

#     embed.set_thumbnail(url = "https://i.ibb.co/CMrsxdX/food.png")
#     embed.set_footer(text = f"Requested by {ctx.author.name}")

#     await ctx.send(embed = embed)
