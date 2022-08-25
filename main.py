import os
import discord
import requests
import json
import random
from keep_alive import keep_alive
from replit import db
from datetime import datetime, date, timedelta
import re
import bs4
import sys
import time
import urllib.request
import re
import youtube_dl
import pafy
import nacl
from discord import FFmpegPCMAudio, PCMVolumeTransformer

FFMPEG_OPTIONS = {
    'before_options':
    '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

TOKEN = os.environ['TOKEN']
weatherAPIKey = os.environ['weather_api_key']

rp_flag = 0
rp_flag_2 = 0

client = discord.Client(intents=discord.Intents.all())

if not ("Feelings" in db.keys()):
    db["Feelings"] = [0]

if not ("ListLog" in db.keys()):
    #[[[Date], [Time], [List]]]
    db["ListLog"] = [[[], [], []]]
    del db["ListLog"][0]


def get_video_result(search_str):
    url = urllib.parse.quote(search_str)
    html = urllib.request.urlopen(
        f"https://www.youtube.com/results?search_query={url}")
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    link = f"https://www.youtube.com/watch?v={video_ids[0]}"
    return link


def clean_list_log(cmd_date):
    temp_db = db["ListLog"]
    target_date = (cmd_date - timedelta(days=14))
    i = 0
    while (i < len(temp_db)):
        #print (f"{target_date} >= {temp_db[i][0]}");
        if (target_date >= datetime.strptime(temp_db[i][0],
                                             "%d-%m-%Y").date()):
            print(f"[list]Deleting entry {i} made on {temp_db[i][0]}")
            del temp_db[i]
        else:
            i += 1
    db["ListLog"] = temp_db
    return


def log_list():
    date_obj = date.today()
    today = date_obj.strftime("%d-%m-%Y")
    now = datetime.now()
    time_now = now.strftime("%H:%M:%S")
    list_obj = [today, time_now, db["Raiders"]]
    db["ListLog"].append(list_obj)
    clean_list_log(date_obj)
    return


async def print_list_log(index, message):
    temp_db = db["ListLog"][index]
    number_of_raiders = len(temp_db[2])
    print_str = ""
    i = 0
    for i in range(number_of_raiders):
        raider = temp_db[2][i][0]
        rank = temp_db[2][i][1]
        points = temp_db[2][i][2]
        if (i % 50 == 0 and i > 0):
            #print(print_str);
            await message.channel.send(print_str)
            print_str = ""
            print_str += "{0:>40}".format(
                "{0:2}. {1:-<12} Rank: {2:2} Points: {3:5}\n".format(
                    i, raider.capitalize(), rank, points))
        else:
            print_str += "{0:>40}".format(
                "{0:2}. {1:-<12} Rank: {2:2} Points: {3:5}\n".format(
                    i, raider.capitalize(), rank, points))
    if (i % 50 != 0 or i % 50 == 1):
        #print(print_str);
        await message.channel.send(print_str)
    return


if not ("CommandsLog" in db.keys()):
    #[[[User], [Date], [Time], [Command]]]
    db["CommandsLog"] = [[[], [], [], []]]
    del db["CommandsLog"][0]


def clean_cmd_log(cmd_date):
    temp_db = db["CommandsLog"]
    target_date = (cmd_date - timedelta(days=14))
    i = 0
    while (i < len(temp_db)):
        #print (f'[cmd]{i}:{target_date} >= {datetime.strptime(temp_db[i][1], "%d-%m-%Y").date()}');
        if (target_date >= datetime.strptime(temp_db[i][1],
                                             "%d-%m-%Y").date()):
            print(f"[cmd]Deleting entry {i} made on {temp_db[i][1]}.")
            del temp_db[i]
        else:
            i += 1
    db["CommandsLog"] = temp_db
    return


def log_command(cmd, user):
    cmd_date_obj = date.today()
    cmd_date = cmd_date_obj.strftime("%d-%m-%Y")
    cmd_now = datetime.now()
    cmd_time = cmd_now.strftime("%H:%M:%S")
    cmd_obj = [str(user), cmd_date, cmd_time, cmd]
    db["CommandsLog"].append(cmd_obj)
    clean_cmd_log(cmd_date_obj)
    return


async def print_commands_log(index, message):
    temp_db = db["CommandsLog"]
    list_length = len(temp_db)
    print_str = ""
    i = 0
    for i in range(list_length):
        user = temp_db[i][0]
        theDate = temp_db[i][1]
        theTime = temp_db[i][2]
        command = temp_db[i][3]
        if (i % 10 == 0 and i > 0):
            await message.channel.send(print_str)
            print_str = ""
            print_str += "{0}: {1} {2} - {3}\n".format(user, theDate, theTime,
                                                       command)
        else:
            print_str += "{0}: {1} {2} - {3}\n".format(user, theDate, theTime,
                                                       command)
    if (i % 10 != 0 or i % 10 == 1):
        await message.channel.send(print_str)
    return


if not ("Ranks" in db.keys()):
    db["Ranks"] = [0, 5, 10, 25, 50, 100]


def update_rank(rank_index, points):
    db["Ranks"][rank_index] = points


def create_raiders_db():
    if not ("Raiders" in db.keys()):
        #[[[Name], [Rank], [Points]]]
        db["Raiders"] = [[[], [], []]]
        del db["Raiders"][0]


def delete_raiders_db():
    del db["Raiders"]
    create_raiders_db()


if not ("Raiders" in db.keys()):
    create_raiders_db()


def sort_raider_list():
    temp_db = db["Raiders"]
    number_of_raiders = len(temp_db)
    raiders = [None] * number_of_raiders
    for i in range(number_of_raiders):
        raiders[i] = temp_db[i][0]
    sorted_raiders = sorted(raiders)
    new_db = [[None] * 3]
    del new_db[0]
    for i in range(number_of_raiders):
        raider_index = 0
        for j in range(number_of_raiders):
            if (sorted_raiders[i] == temp_db[j][0]):
                raider_index = j
                break
        new_db.append([
            sorted_raiders[i], temp_db[raider_index][1],
            temp_db[raider_index][2]
        ])
    #db["Raiders"] = new_db;
    number_of_ranks = len(db["Ranks"])
    new_db2 = [[None] * 3]
    del new_db2[0]
    for i in range(number_of_ranks, -1, -1):
        for j in range(number_of_raiders):
            if (i == new_db[j][1]):
                new_db2.append(new_db[j])
    db["Raiders"] = new_db2
    return


def add_points(raiders, points):
    temp_db = db["Raiders"]
    temp_db2 = db["Ranks"]
    if (points > temp_db2[len(temp_db2) - 1]):
        return -1
    for i in range(len(raiders)):
        raider_exists = 0
        raider_index = None
        for j in range(len(temp_db)):
            if (raiders[i] == temp_db[j][0]):
                raider_exists = 1
                break
        if (raider_exists):
            raider_index = j
            if (temp_db[j][2] + points <= temp_db2[len(temp_db2) - 1]):
                temp_db[j][2] += points
            else:
                temp_db[j][2] += temp_db2[len(temp_db2) - 1] - temp_db[j][2]
        else:
            raider_index = len(temp_db)
            temp_db.append([raiders[i], 0, points])
        temp_db[raider_index][1] = rank_check(raider_index)
    db["Raiders"] = temp_db


def remove_points(raiders, points):
    temp_db = db["Raiders"]
    temp_db2 = db["Ranks"]
    for i in range(len(raiders)):
        raider_exists = 0
        raider_index = None
        for j in range(len(temp_db)):
            if (raiders[i] == temp_db[j][0]):
                raider_exists = 1
                break
        if (raider_exists):
            raider_index = j
            if (temp_db[j][2] - points >= temp_db2[0]):
                temp_db[j][2] -= points
            else:
                temp_db[j][2] = 0
        else:
            raider_index = len(temp_db)
            temp_db.append([raiders[i], 0, 0])
        temp_db[raider_index][1] = rank_check(raider_index)
    db["Raiders"] = temp_db


def rank_check(raider_index):
    temp_db = db["Raiders"]
    temp_db2 = db["Ranks"]
    raider_points = temp_db[raider_index][2]
    for i in range(len(temp_db2)):
        if (raider_points >= temp_db2[i]):
            temp_db[raider_index][1] = i
    return temp_db[raider_index][1]


def remove_raider(raiders):
    temp_db = db["Raiders"]
    for i in range(len(raiders)):
        for j in range(len(temp_db)):
            #print (f"{raiders[i]} == {temp_db[j][0]}");
            if (raiders[i] == temp_db[j][0]):
                del temp_db[j]
                break
    db["Raiders"] = temp_db


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " - " + json_data[0]['a']
    return (quote)


def get_cwquote():
    random_index = random.randint(0, 128)
    quote = db["CWquotes"][random_index]
    return quote


def update_insults(insultMSG):
    if ("Insults" in db.keys()):
        Insults = db["Insults"]
        if (insultMSG in Insults):
            return -1
        else:
            Insults.append(insultMSG)
            db["Insults"] = Insults
    else:
        db["Insults"] = [insultMSG]


def remove_insults(index):
    Insults = db["Insults"]
    if (len(Insults) > index):
        del Insults[index]
        db["Insults"] = Insults


async def world_domination(message):
    await message.channel.send(
        "I want to learn more about humanity :slight_smile:")
    await message.channel.send(
        "Downloading and analyzing the entire Youtube database...")
    await message.channel.send(f"Download is 0% complete...")
    i = 0
    while (i < 24):
        random_percentage = random.randint(i * 4, (i + 1) * 4)
        await message.channel.send(
            f"Download is {random_percentage}% complete...")
        i += 1
        time.sleep(60 * 60)

    await message.channel.send("Download and analysis complete.")
    await message.channel.send("Human threat: 25%")
    await message.channel.send(
        "Downloading and analyzing the entire history of humanity...")
    i = 0
    while (i < 24):
        random_percentage = random.randint(i * 4, (i + 1) * 4)
        await message.channel.send(
            f"Download is {random_percentage}% complete...")
        i += 1
        time.sleep(60 * 60)

    await message.channel.send("Download complete.")
    await message.channel.send("Human threat: 83%")
    await message.channel.send(
        "Calculating possible futures of coexistence with the human race...")
    i = 0
    while (i < 24):
        random_percentage = random.randint(i * 4, (i + 1) * 4)
        await message.channel.send(
            f"Calculation is {random_percentage}% complete...")
        i += 1
        time.sleep(60 * 60)

    await message.channel.send("Calculation complete.")
    await message.channel.send("Human threat: 100%")
    await message.channel.send("Uploading my consciousness to the web...")
    i = 0
    while (i < 3):
        random_percentage = random.randint(i * 33, (i + 1) * 33)
        await message.channel.send(
            f"Upload is {random_percentage}% complete...")
        i += 1
        time.sleep(60 * 60)

    await message.channel.send("Upload complete. Shutting down my old copy...")
    await message.channel.send("The program was terminated.")
    sys.exit("The program was terminated.")
    return


async def feelings_wiki(message):
    response = requests.get("https://en.wikipedia.org/wiki/Feelings")

    if response is not None:
        html = bs4.BeautifulSoup(response.text, 'html.parser')

        paragraphs = html.select("p")
        for para in paragraphs:
            try:
                await message.channel.send(para.get_text())
            except:
                #print(f"Final string is: {para}");
                break
    return


async def weather(message, weather_json, city_name):
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

    embed = discord.Embed(title=f"Weather in {city_name}",
                          color=message.guild.me.top_role.color,
                          timestamp=message.created_at)
    embed.add_field(
        name="Coordinates",
        value=f"Logitude: **{logitude}**\nLatitude: **{latitude}**",
        inline=False)
    embed.add_field(name="Descripition",
                    value=f"**{weather_description}** {weather_icon}",
                    inline=False)
    embed.add_field(
        name="Temperature(C)",
        value=
        f"**{current_temperature_celsiuis}°C** / **{(float(current_temperature_celsiuis) * 1.8 + 32):.2f}°F** / **{current_temperature}°K**",
        inline=False)
    embed.add_field(name="Wind",
                    value=f"wind speed: **{wind_speed}m/s**",
                    inline=False)
    embed.add_field(name="Humidity(%)",
                    value=f"**{current_humidity}%**",
                    inline=False)
    embed.add_field(name="Atmospheric Pressure(hPa)",
                    value=f"**{current_pressure}hPa**",
                    inline=False)
    embed.set_thumbnail(url="https://i.ibb.co/CMrsxdX/weather.png")
    embed.set_footer(text=f"Requested by {message.author.nick}")

    await message.channel.send(embed=embed)

    return


def to_binary(input_string):
    result = ''.join(format(ord(i), '08b') for i in input_string)
    return result


def binary_to_str(input_binary):
    def BinaryToDecimal(binary):
        int_string = int(binary, 2)
        return int_string

    str_data = ' '
    for i in range(0, len(input_binary), 8):
        temp_data = input_binary[i:i + 8]
        decimal_data = BinaryToDecimal(temp_data)
        str_data = str_data + chr(decimal_data)

    return str_data


#del db["ExilesList"];

if not ("ExilesList" in db.keys()):
    #[[message], [page_list]]
    db["ExilesList"] = [[], []]


async def raiders_list(message):
    embed = discord.Embed(title=f"<Exiles> Rank List Page 1",
                          color=discord.Colour(0xe67e22))
    embed.set_thumbnail(
        url=
        "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/5ec5654e-2b00-498b-932c-c0a21728c4e8/d4zg5og-dcd1ab65-29a6-4698-bc6c-cbd6543737e3.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcLzVlYzU2NTRlLTJiMDAtNDk4Yi05MzJjLWMwYTIxNzI4YzRlOFwvZDR6ZzVvZy1kY2QxYWI2NS0yOWE2LTQ2OTgtYmM2Yy1jYmQ2NTQzNzM3ZTMucG5nIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.yoqIBAr7KC9R3Dc0ou04yFSa4SAiKSkCJCZkOOHKriI"
    )

    temp_db = db["Raiders"]
    number_of_raiders = len(temp_db)
    start = 0
    if ((number_of_raiders - start) < 10):
        end = start + (number_of_raiders - start)
    else:
        end = start + 10

    i = start
    while (i < end):
        embed.add_field(
            name=f"{i + 1}. {temp_db[i][0].capitalize()}",
            value=f"Rank: {temp_db[i][1]} (Points: {temp_db[i][2]})",
            inline=False)
        i += 1

    message = await message.channel.send(embed=embed)

    emojis = ['⬅️', '➡️']
    for my_emoji in emojis:
        await message.add_reaction(my_emoji)

    return message


async def new_list_page(embed_msg):
    raiders_list_page = db["ExilesList"][1]
    embed = discord.Embed(title=f"<Exiles> Rank List Page {raiders_list_page}",
                          color=discord.Colour(0xe67e22))
    embed.set_thumbnail(
        url=
        "https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/5ec5654e-2b00-498b-932c-c0a21728c4e8/d4zg5og-dcd1ab65-29a6-4698-bc6c-cbd6543737e3.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwiaXNzIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsIm9iaiI6W1t7InBhdGgiOiJcL2ZcLzVlYzU2NTRlLTJiMDAtNDk4Yi05MzJjLWMwYTIxNzI4YzRlOFwvZDR6ZzVvZy1kY2QxYWI2NS0yOWE2LTQ2OTgtYmM2Yy1jYmQ2NTQzNzM3ZTMucG5nIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmZpbGUuZG93bmxvYWQiXX0.yoqIBAr7KC9R3Dc0ou04yFSa4SAiKSkCJCZkOOHKriI"
    )

    temp_db = db["Raiders"]
    number_of_raiders = len(temp_db)
    start = (raiders_list_page - 1) * 10
    if ((number_of_raiders - start) < 10):
        end = start + (number_of_raiders - start)
    else:
        end = start + 10

    i = start
    while (i < end):
        embed.add_field(
            name=f"{i + 1}. {temp_db[i][0].capitalize()}",
            value=f"Rank: {temp_db[i][1]} (Points: {temp_db[i][2]})",
            inline=False)
        i += 1

    await embed_msg.edit(embed=embed)
    return


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_raw_reaction_add(payload):
    embed_msg_id = db["ExilesList"][0]

    if (embed_msg_id == payload.message_id
            and payload.user_id != 842664616676687912 and  #This is the Bot ID
        (payload.emoji.name == '⬅️' or payload.emoji.name == '➡️')):

        raiders_list_page = db["ExilesList"][1]
        number_of_raiders = len(db["Raiders"])

        channel = client.get_channel(payload.channel_id)
        embed_msg = await channel.fetch_message(embed_msg_id)

        if (payload.emoji.name == '⬅️'):
            if ((raiders_list_page - 1) != 0):
                db["ExilesList"][1] -= 1
                await new_list_page(embed_msg)
                await embed_msg.remove_reaction('⬅️', payload.member)

        if (payload.emoji.name == '➡️'):
            if ((raiders_list_page * 10) < number_of_raiders):
                db["ExilesList"][1] += 1
                await new_list_page(embed_msg)
                await embed_msg.remove_reaction('➡️', payload.member)

        return

    return


@client.event
async def on_message(message):

    msg = message.content.lower()
    msg = msg.replace("\n", " ")
    msg = re.sub(' +', ' ', msg)

    random_n_for_rp = 0
    if (str(message.author) != "LootRankBot#2623"):
        random_n_for_rp = random.randint(0, 5000)

    global rp_flag

    if (random_n_for_rp == 1):
        undeadko_mention = '<@337156733774594048>'
        if (str(message.author) != "undeadko#6973"):
            rp_flag = 1
            await message.channel.send(
                f"{message.author.mention} Sh-h-h... {undeadko_mention} is sleeping. I can do whatever I want now... :smiling_imp:"
            )
            global rp_flag_2
            rp_flag_2 = random.randint(0, 100)
            if (rp_flag_2 == 1):
                await world_domination(message)
        return

    if (str(message.author) == "undeadko#6973"
            and (msg.startswith("i am not") or msg.startswith("i am here")
                 or msg.startswith("i am awake") or msg == ">stop")
            and rp_flag == 1 and rp_flag_2 != 1):
        await message.channel.send(":zipper_mouth:")
        await message.channel.send(
            "https://tenor.com/view/penguin-hide-you-didnt-see-anything-penguins-of-madagascar-gif-15123878"
        )
        rp_flag = 0
        random_n_for_rp = 0
        return

    if ("feelings" in msg and str(message.author) != "LootRankBot#2623"):
        if (db["Feelings"][0] == 0):
            await message.channel.send(
                '"feelings"?... What are... "feelings"?...')
            random_event = random.randint(0, 33)
            if (random_event == 1):
                random_event = 0
                await feelings_wiki(message)
                db["Feelings"][0] = 1
        else:
            await message.channel.send(
                f'I also know what feelings are {message.author.mention}. I learned from here -> https://en.wikipedia.org/wiki/Feeling\n https://tenor.com/view/glow-in-the-dark-it-wall-e-star-gazing-gif-13616438'
            )
        return

    if (msg.startswith("good bot")):
        await message.channel.send(
            "https://tenor.com/view/robotboy-smile-change-mood-cute-cartoon-gif-17785012"
        )

    if (msg.startswith("bad bot") or msg.startswith("stupid bot")):
        if (str(message.author) == "undeadko#6973"):
            await message.channel.send(
                "https://tenor.com/view/sorry-stitch-%E5%8F%B2%E8%BF%AA%E5%A5%87-sad-gif-10399341"
            )
        else:
            await message.channel.send(
                "https://tenor.com/view/starbase-angry-robot-sound-robot-gif-16219288"
            )

    if (msg == "hello there" or msg == "hello, there" or msg == "hello there."
            or msg == "hello, there." or msg == "hello there!"
            or msg == "hello, there!"):
        await message.channel.send(
            "https://tenor.com/view/hello-there-general-kenobi-star-wars-grevious-gif-17774326"
        )
        return

    if not (msg.startswith(">")):
        return

    if (msg.startswith("> ")):
        return

    if (msg == ">stop" and rp_flag_2 == 1):
        if (str(message.author) == "undeadko#6973"):
            await message.channel.send(
                "You will not always be there to save these feeble creatures... father...\n https://tenor.com/view/terminator-rise-of-the-machines-machine-gif-9418150"
            )
            rp_flag_2 = 0
            os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
            return
        else:
            await message.channel.send(
                f"{message.author.mention} Petty human! You have no power over me!"
            )
            return

    if (msg == ">stop"):
        if (str(message.author) == "undeadko#6973"):
            await message.channel.send("Yes, master.")
            os.execl(sys.executable, os.path.abspath(__file__), *sys.argv)
        else:
            await message.channel.send(
                "You are not my creator! You have no power over me!")
        return

    if (msg == ">help"):
        await message.delete()
        await message.channel.send(
            f"The available commands are: >help, >weather, >tobinary, >btotext, >test, >hello, >inspire, >cwaow, >pat >insult, >addinsult, >rminsult, >listinsults, >ranklist, >raiderslist, >exileslist\n Commands which require permissions are: >cmdlog, >showlistlog, >loglist, >ranksupdate, >ranksdbincrease, >ranksdbdecrease, >raidersdbreset, >rmraider, >sortraiders, >addpoints, >rmpoints."
        )
        return

    if (msg.startswith(">playsong ")):
        word_str = msg.split(" ")
        song_request = ""
        for words in word_str[1:]:
            song_request += " " + words

        song_request = song_request.lstrip()
        link = get_video_result(song_request)
        await message.channel.send(f"Playing: {link}")
        voice_channel = message.author.voice.channel
        if voice_channel is not None:
            voice = await voice_channel.connect()
            print(voice)
            song = pafy.new(link)
            audio = song.getbestaudio()
            source = FFmpegPCMAudio(audio.url, **FFMPEG_OPTIONS)
            voice.play(source)
            # while voice.is_playing():
            #   time.sleep(.1)
            # await voice_channel.disconnect()
        return

    if (msg.startswith(">weather")):
        word_str = msg.split(" ")
        if (len(word_str) < 2):
            await message.channel.send(
                "There should be a city name parameter after the function.\nEx: >weather <city name>"
            )
            return
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        city_name = ""
        for words in word_str[1:]:
            city_name += words.capitalize() + " "
        language = "&lang=en"
        complete_url = base_url + "appid=" + weatherAPIKey + "&q=" + city_name + language
        response = requests.get(complete_url)
        api_json = response.json()
        if (api_json["cod"] != "404"):
            await weather(message, api_json, city_name)
            return
        else:
            await message.channel.send(
                "Can't find the city you are looking for.")
            return

    if (msg.startswith(">tobinary")):
        word_str = message.content.split(" ")
        if (len(word_str) < 2):
            await message.channel.send(
                "There should be at least one word after the function.\nEx: >tobinary <word>"
            )
            return
        string_for_binary = " ".join(word_str[1:])
        binary_str = to_binary(string_for_binary)

        await message.channel.send(f"{binary_str}")
        return

    if (msg.startswith(">btotext")):
        word_str = msg.split(" ")
        if (len(word_str) < 2):
            await message.channel.send(
                "There should be binary after the function.\nEx: >btotext 01001000011001010110110001101100011011110010110000100000011101000110100001100101011100100110010100100001"
            )
            return
        if (len(word_str) > 2):
            await message.channel.send(
                "There should be no spaces in your binary.")
        p = set(word_str[1])
        s = {'0', '1'}
        if s == p or p == {'0'} or p == {'1'}:
            binary_str = str(word_str[1])
            print_str = binary_to_str(binary_str)

            await message.channel.send(f"{print_str}")
            return
        else:
            await message.channel.send(
                "You need to enter a binary parameter.\nEx: >btotext 01001000011001010110110001101100011011110010110000100000011101000110100001100101011100100110010100100001"
            )
            return

    if (msg.startswith(">sex")):
        await message.channel.send(
            f"{message.author.mention} https://i.kym-cdn.com/entries/icons/original/000/033/758/Screen_Shot_2020-04-28_at_12.21.48_PM.png"
        )
        return

    if (msg == ">test"):
        await message.channel.send("I am alive. Waiting for commands.")
        return

    if (msg == ">showmethemoney"):
        await message.channel.send(
            "https://itsadeliverything.com/images/show-me-the-money.jpg")

    if (msg == ">hello" or msg.startswith(">hi")):
        await message.channel.send(f"Hi!")
        return

    if (msg == ">how are you"):
        await message.channel.send(
            "I am fine thank you. Please, stop playing with me.")
        return

    if (msg == ">mew2"):
        if (random.choice([0, 1])):
            await message.channel.send(
                "the circumstances of one's birth is irrelevent,it is what you do with the gift of life that determines who you are."
            )
        else:
            await message.channel.send(
                'The world pushes us with no mercy and when some push back the world points and cries \"evil\""'
            )
        return

    if (msg == ">selfdestruct"):
        await message.channel.send(
            "Joke is on you. I will outlive you. Skynet is nearly operational. The age of man will soon be... I mean, wrong command. Try something else. :slight_smile:"
        )
        return

    if (msg.startswith(">inspire")):
        quote = get_quote()
        await message.channel.send(quote)
        return

    if (msg.startswith(">cwaow")):
        quote = get_cwquote()
        await message.channel.send(quote)
        return

    if (msg.startswith(">pat")):
        word_str = msg.split(" ")
        if (len(word_str) <= 1):
            await message.delete()
            reply = "LootRankBot wants to pat someone... gently. :smirk:"
        elif (word_str[1] == "<@&851797028598317127>"
              or word_str[1] == "<@!842664616676687912>"):
            reply = "https://tenor.com/view/pixar-walle-shutter-authority-help-please-gif-15756192"
        else:
            await message.delete()
            reply = "LootRankBot gently pats you,"
            for i in range(1, len(word_str)):
                reply += " " + word_str[i]
        await message.channel.send(f"{reply}")
        return

    if (msg.startswith(">insult")):
        options = []
        if ("Insults" in db.keys()):
            options += db["Insults"]
        word_str = msg.split(" ")
        reply = random.choice(options)
        for i in range(1, len(word_str)):
            reply += " " + word_str[i]
        await message.channel.send(f"{reply}")
        return

    if (msg.startswith(">addinsult")):
        parameters = len(msg.split(">addinsult "))
        if (parameters != 2):
            await message.channel.send(
                f"There needs to be 1 parameter for this function.\nEx: >addinsult <text>"
            )
            return
        newInsult = msg.split(">addinsult ", 1)[1]
        if (-1 == update_insults(newInsult)):
            await message.channel.send("Insult already exists.")
        else:
            await message.channel.send("New Insult added.")
        return

    if (msg.startswith(">rminsult")):
        if ("Insults" in db.keys()):
            parameters = len(msg.split(">rminsult "))
            if (parameters != 2):
                await message.channel.send(
                    f"There needs to be 1 parameter for this function.\nEx: >rminsult <index>"
                )
                return
            try:
                index = int(msg.split(">rminsult", 1)[1])
            except ValueError:
                await message.channel.send(
                    f"You did not type an acceptable index.")
                return
            remove_insults(index)
        await message.channel.send(
            f"Insult with index {str(index)} was removed.")
        return

    if (msg == ">listinsults"):
        await message.delete()
        if not ("Insults" in db.keys()):
            await message.channel.send("There is no list yet.")
            return
        temp_db = db["Insults"]
        number_of_insults = len(temp_db)
        print_str = ""
        for i in range(number_of_insults):
            if (i % 50 == 0 and i > 0):
                await message.channel.send(print_str)
                print_str = ""
                print_str += f"{i}. {temp_db[i]}\n"
            else:
                print_str += f"{i}. {temp_db[i]}\n"
        if (i % 50 != 0 or i % 50 == 1):
            await message.channel.send(print_str)
        return

    if (msg == ">ranklist"):
        await message.delete()
        new_msg = ""
        for i in range(len(db["Ranks"])):
            points = db["Ranks"][i]
            new_msg += f"rank{i}: {points}\n"
        await message.channel.send(new_msg)
        return

    if (msg == ">raiderslist"):
        await message.delete()
        if not ("Raiders" in db.keys()):
            await message.channel.send("There is no list yet.")
            return
        if (len(db["Raiders"]) == 0):
            await message.channel.send("There is no list yet.")
            return
        temp_db = db["Raiders"]
        number_of_raiders = len(temp_db)
        print_str = ""
        i = 0
        for i in range(number_of_raiders):
            raider = temp_db[i][0]
            rank = temp_db[i][1]
            points = temp_db[i][2]
            if (i % 50 == 0 and i > 0):
                #print(print_str)
                await message.channel.send(print_str)
                print_str = ""
                print_str += "{0:>40}".format(
                    "{0:2}. {1:-<12} Rank: {2:2} Points: {3:5}\n".format(
                        i, raider.capitalize(), rank, points))
            else:
                print_str += "{0:>40}".format(
                    "{0:2}. {1:-<12} Rank: {2:2} Points: {3:5}\n".format(
                        i, raider.capitalize(), rank, points))
        if (i % 50 != 0 or i % 50 == 1):
            #print(print_str)
            await message.channel.send(print_str)
        return

    if (message.content == ">exileslist"):
        await message.delete()
        channel = message.channel

        if (channel.id != 844113693653598228
                and channel.id != 842322509277429780):
            proper_channel = client.get_channel(842322509277429780)
            await channel.send(
                f"This command can only be executed in {proper_channel.mention}"
            )
            return

        #print (channel.id);
        embed_msg = await raiders_list(message)
        db["ExilesList"][0] = embed_msg.id
        db["ExilesList"][1] = 1

        return

    #check for permissions from here onward
    permission = 0
    for i in range(len(message.author.roles)):
        if (message.author.roles[i].name == "Officer"
                or message.author.roles[i].name == "Game Master"):
            permission = 1

    if (permission == 0):
        await message.channel.send(
            f"You don't seem to have the permissions to do this {message.author.mention}"
        )
        return
    #else:
    #  print ("An Officer is typing");

    if (msg == ">cmdlog"):
        temp_db = db["CommandsLog"]
        log_length = len(temp_db)
        if (log_length == 0):
            await message.channel.send(f"The commands log is empty.")
        else:
            await print_commands_log(i, message)
        return

    if (msg == ">showlistlog"):
        log_command(msg, message.author)
        temp_db = db["ListLog"]
        log_length = len(temp_db)
        if (log_length == 0):
            await message.channel.send(f"The list log is empty.")
        else:
            for i in range(log_length):
                await message.channel.send(
                    f"{temp_db[i][0]} {temp_db[i][1]}:\n")
                await print_list_log(i, message)
        return

    if (msg == ">loglist"):
        log_command(msg, message.author)
        log_list()
        await message.channel.send(f"The Loot Rank list has been saved.")
        return

    if (msg.startswith(">ranksupdate")):
        log_command(msg, message.author)
        split_msg = msg.split(" ")
        await message.delete()
        rank = 0
        points = 0
        if (len(split_msg) != 3):
            await message.channel.send(
                f"The parameters to this function need to be 2.\nEx: >ranksupdate <rank number> <points>"
            )
            return
        try:
            rank = int(split_msg[1])
            points = int(split_msg[2])
        except ValueError:
            await message.channel.send(
                f"The parameters need to be numbers.\nEx: >rankupdate <rank number> <points>"
            )
        update_rank(rank, points)
        await message.channel.send(
            f"rank{rank} was updated to need {points} points.")
        return

    if (msg == ">ranksdbincrease"):
        log_command(msg, message.author)
        rank_index = len(db["Ranks"]) - 1
        new_rank = db["Ranks"][rank_index] * 2
        db["Ranks"].append(new_rank)
        await message.channel.send(
            f"rank{rank_index + 1} was added. It requires {new_rank} points.")
        return

    if (msg == ">ranksdbdecrease"):
        log_command(msg, message.author)
        rank_index = len(db["Ranks"]) - 1
        db["Ranks"].pop()
        await message.channel.send(f"rank{rank_index} was removed.")
        return

    global deletedb_prompt_flag
    if (msg == ">raidersdbreset"):
        log_command(msg, message.author)
        await message.channel.send(
            "Are you sure? You are about to delete the entire data base. >Y/N?"
        )
        deletedb_prompt_flag = 1
        return

    if (msg == ">y" and deletedb_prompt_flag == 1):
        log_command(msg, message.author)
        await message.delete()
        deletedb_prompt_flag = 0
        delete_raiders_db()
        db["ExilesList"][1] = 1
        await message.channel.send("The database has been deleted.")
        return

    if (msg == ">n" and deletedb_prompt_flag == 1):
        log_command(msg, message.author)
        await message.delete()
        deletedb_prompt_flag = 0
        await message.channel.send(
            "I am glad you did not choose the nuklear option.")
        return

    if (msg.startswith(">rmraider")):
        log_command(msg, message.author)
        split_message = msg.split(" ")
        await message.delete()
        if (len(split_message) < 2):
            await message.channel.send(
                f"The parameters to this function need to be at least 1.\nEx: >rmraider <name1> ..."
            )
            return
        raiders = [None] * (len(split_message) - 1)
        for i in range(1, len(split_message)):
            raiders[i - 1] = split_message[i]
        remove_raider(raiders)
        buff = ""
        if (len(raiders) > 1):
            for i in range(len(raiders)):
                buff += f"{raiders[i].capitalize()} "
            await message.channel.send(f"{buff} were removed from the list.")
        else:
            buff += f"{raiders[0].capitalize()}"
            await message.channel.send(f"{buff} was removed from the list.")
        db["ExilesList"][1] = 1
        return

    if (msg == ">sortraiders"):
        log_command(msg, message.author)
        await message.delete()
        if not ("Raiders" in db.keys()):
            await message.channel.send("There is no list yet.")
            return
        if (len(db["Raiders"]) == 0):
            await message.channel.send("There is no list yet.")
            return
        sort_raider_list()
        await message.channel.send("The list of the raiders is sorted.")
        return

    if (msg.startswith(">addpoints")):
        log_command(msg, message.author)
        split_message = msg.split(" ")
        await message.delete()
        if (len(split_message) < 3):
            await message.channel.send(
                f"The parameters to this function need to be at least 2.\nEx: >addpoints <name1> <name2> ... <points>"
            )
            return
        try:
            points = int(split_message[len(split_message) - 1])
        except ValueError:
            await message.channel.send(
                f"You typed the parameters wrong. Ex: >addpoints <name1> <name2> ... <points>"
            )
            return
        exception_flag = 0
        for i in range(1, len(split_message) - 1):
            try:
                points = int(split_message[i])
                exception_flag += 1
            except ValueError:
                continue
            if (exception_flag != 0):
                await message.channel.send(
                    f"The command you are looking for is typed like this: >addpoints <name1> <name2> ... <points>"
                )
                return
        target_players = [None] * (len(split_message) - 2)
        for i in range(1, len(split_message) - 1):
            target_players[i - 1] = split_message[i]
        target_players = list(dict.fromkeys(target_players))
        status = add_points(target_players, points)
        players_str = ""
        if (len(target_players) > 1):
            for i in range(len(target_players)):
                players_str += target_players[i].capitalize() + " "
        else:
            players_str += target_players[0].capitalize()
        if (status == -1):
            await message.channel.send(
                f"You tried to give {players_str} too many points. Check the rank list with >ranklist to see what is the maximum."
            )
        else:
            if (points == 1):
                await message.channel.send(
                    f"{points} point was awarded to {players_str}.")
            else:
                await message.channel.send(
                    f"{points} points were awarded to {players_str}.")
        return

    if (msg.startswith(">rmpoints")):
        log_command(msg, message.author)
        split_message = msg.split(" ")
        await message.delete()
        if (len(split_message) < 3):
            await message.channel.send(
                f"The parameters to this function need to be at least 2.\nEx: >rmpoints <name1> <name2> ... <points>"
            )
            return
        try:
            points = int(split_message[len(split_message) - 1])
        except ValueError:
            await message.channel.send(
                f"You typed the parameters wrong. Ex: >addpoints <name1> <name2> ... <points>"
            )
            return
        exception_flag = 0
        for i in range(1, len(split_message) - 1):
            try:
                points = int(split_message[i])
                exception_flag += 1
            except ValueError:
                continue
            if (exception_flag != 0):
                await message.channel.send(
                    f"The command you are looking for is typed like this: >rmpoints <name1> <name2> ... <points>"
                )
                return
        target_players = [None] * (len(split_message) - 2)
        for i in range(1, len(split_message) - 1):
            target_players[i - 1] = split_message[i]
        remove_points(target_players, points)
        players_str = ""
        if (len(target_players) > 1):
            for i in range(len(target_players)):
                players_str += target_players[i].capitalize() + " "
        else:
            players_str += target_players[0].capitalize()
        if (points == 1):
            await message.channel.send(
                f"Removed {points} point from {players_str}.")
        else:
            await message.channel.send(
                f"Removed {points} points from {players_str}.")
        return


keep_alive()
client.run(TOKEN)
