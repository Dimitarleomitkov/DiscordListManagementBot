import os
import discord
import requests
import json
import random
from keep_alive import keep_alive
from replit import db
from datetime import datetime, date, timedelta

TOKEN = os.environ['TOKEN']

client = discord.Client();

if not ("ListLog" in db.keys()):
  #[[[Date], [Time], [List]]]
  db["ListLog"] = [[[], [], []]];
  del db["ListLog"][0];

def clean_list_log(cmd_date):
  temp_db = db["ListLog"];
  target_date = (cmd_date - timedelta(days = 14)).strftime("%d-%m-%Y");
  #print (f"{target_date}");
  for i in range(len(temp_db)):
    if (target_date == temp_db[i][0]):
      #print (f"Deleting entry {i} made on {temp_db[i][1]}");
      del temp_db[i];
  db["ListLog"] = temp_db;
  return;

def log_list():
  date_obj = date.today();
  today = date_obj.strftime("%d-%m-%Y");
  now = datetime.now();
  time_now = now.strftime("%H:%M:%S");
  list_str = "";
  temp_db = db["Raiders"];
  for i in range(len(temp_db)):
    list_str += "{0:>40}".format("{0:2}. {1:-<12} Rank: {2:2} Points: {3:5}\n".format(i, temp_db[i][0].capitalize(), temp_db[i][1], temp_db[i][2]));
  list_obj = [today, time_now, list_str];
  db["ListLog"].append(list_obj);
  clean_list_log(date_obj);
  return;

def print_list_log():
  temp_db = db["ListLog"];
  new_str = "";
  for i in range(len(temp_db)):
    new_str += f"{temp_db[i][1]} {temp_db[i][2]}: {temp_db[i][3]}\n";
  return new_str;

if not ("CommandsLog" in db.keys()):
  #[[[User], [Date], [Time], [Command]]]
  db["CommandsLog"] = [[[], [], [], []]];
  del db["CommandsLog"][0];

def clean_cmd_log(cmd_date):
  temp_db = db["CommandsLog"];
  target_date = (cmd_date - timedelta(days = 14));
  for i in range(len(temp_db)):
    #print (f'Is {target_date} >= {datetime.strptime(temp_db[i][1], "%d-%m-%Y").date()}');
    if (target_date >= datetime.strptime(temp_db[i][1], "%d-%m-%Y").date()):
      #print (f"Deleting entry {i} made on {temp_db[i][1]}.");
      del temp_db[i];
  db["CommandsLog"] = temp_db;
  return;

def log_command(cmd, user):
  cmd_date_obj = date.today();
  cmd_date = cmd_date_obj.strftime("%d-%m-%Y");
  cmd_now = datetime.now();
  cmd_time = cmd_now.strftime("%H:%M:%S");
  cmd_obj = [str(user), cmd_date, cmd_time, cmd];
  db["CommandsLog"].append(cmd_obj);
  clean_cmd_log(cmd_date_obj);
  return;

def print_commands_log():
  temp_db = db["CommandsLog"];
  new_str = "";
  for i in range(len(temp_db)):
    new_str += f"{temp_db[i][0]}: {temp_db[i][1]} {temp_db[i][2]} - {temp_db[i][3]}\n";
  return new_str;

if not ("Ranks" in db.keys()):
  db["Ranks"] = [0, 5, 10, 25, 50, 100];

def update_rank(rank_index, points):
  db["Ranks"][rank_index] = points;

def create_raiders_db():
  if not ("Raiders" in db.keys()):
    #[[[Name], [Rank], [Points]]]
    db["Raiders"] = [[[], [], []]];
    del db["Raiders"][0];

def delete_raiders_db():
  del db["Raiders"];
  create_raiders_db();

if not ("Raiders" in db.keys()):
  create_raiders_db();

def sort_raider_list():
  temp_db = db["Raiders"];
  raiders = [None] * len(temp_db);
  for i in range(len(temp_db)):
    raiders[i] = temp_db[i][0];
  sorted_raiders = sorted(raiders);
  new_db = [[None] * 3] * len(temp_db);
  for i in range(len(new_db)):
    new_db[i][0] = sorted_raiders[i];
    raider_index = 0;
    for j in range(len(temp_db)):
      if (sorted_raiders[i] == temp_db[j][0]):
        raider_index = j;
        break;
    new_db[i][1] = temp_db[raider_index][1];
    new_db[i][2] = temp_db[raider_index][2];
    db["Raiders"][i] = new_db[i];

def add_points(raiders, points):
  temp_db = db["Raiders"];
  temp_db2 = db["Ranks"];
  if (points > temp_db2[len(temp_db2) - 1]):
    return -1;
  for i in range(len(raiders)):
    raider_exists = 0;
    raider_index = None;
    for j in range(len(temp_db)):
      if (raiders[i] == temp_db[j][0]):
        raider_exists = 1;
        break;
    if (raider_exists):
      raider_index = j;
      if (temp_db[j][2] + points <= temp_db2[len(temp_db2) - 1]):
        temp_db[j][2] += points;
      else:
        temp_db[j][2] += temp_db2[len(temp_db2) - 1] - temp_db[j][2];
    else:
      raider_index = len(temp_db);
      temp_db.append([raiders[i], 0, points]);
    temp_db[raider_index][1] = rank_check(raider_index);
  db["Raiders"] = temp_db;

def remove_points(raiders, points):
  temp_db = db["Raiders"];
  temp_db2 = db["Ranks"];
  for i in range(len(raiders)):
    raider_exists = 0;
    raider_index = None;
    for j in range(len(temp_db)):
      if (raiders[i] == temp_db[j][0]):
        raider_exists = 1;
        break;
    if (raider_exists):
      raider_index = j;
      if (temp_db[j][2] - points >= temp_db2[0]):
        temp_db[j][2] -= points;
      else:
        temp_db[j][2] = 0;
    else:
      raider_index = len(temp_db);
      temp_db.append([raiders[i], 0, 0]);
    temp_db[raider_index][1] = rank_check(raider_index);
  db["Raiders"] = temp_db;

def rank_check(raider_index):
  temp_db = db["Raiders"];
  temp_db2 = db["Ranks"];
  raider_points = temp_db[raider_index][2];
  for i in range(len(temp_db2)):
    if (raider_points >= temp_db2[i]):
      temp_db[raider_index][1] = i;
  return temp_db[raider_index][1];

def remove_raider(raiders):
  temp_db = db["Raiders"];
  for i in range(len(raiders)):
    for j in range(len(temp_db)):
      if (raiders[i] == temp_db[j][0]):
        del temp_db[j];
        break;
  db["Raiders"] = temp_db;

def get_quote():
  response = requests.get("https://zenquotes.io/api/random");
  json_data = json.loads(response.text);
  quote = json_data[0]['q'] + " - " + json_data[0]['a'];
  return(quote);

def update_insults(insultMSG):
  if ("Insults" in db.keys()):
    Insults = db["Insults"];
    if (insultMSG in Insults):
      return -1;
    else:
      Insults.append(insultMSG);
      db["Insults"] = Insults;
  else:
    db["Insults"] = [insultMSG];
  
def remove_insults(index):
  Insults = db["Insults"];
  if (len(Insults) > index):
    del Insults[index];
    db["Insults"] = Insults;

@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client));

@client.event
async def on_message(message):
  
  msg = message.content.lower();

  if not (msg.startswith(">")):
    return;

  if (msg == ">help"):
    await message.delete();
    await message.channel.send(f"The available commands are: >test, >hello, >hello there, >how are you, >inspire, >pat, >insult, >addinsult, >listinsults, >rminsult, >ranklist, >ranksupdate, >ranksdbincrease, >ranksdbdecrease, >raidersdbreset, >rmraider, >raiderslist, >sortraiders, >addpoints, >rmpoints, >cmdlog, >loglist, >showlistlog");
    return;

  if (msg == ">test"):
    await message.channel.send(f"I am alive. Waiting for commands.");
    return;

  if (msg == ">hello" or msg.startswith(">hi")):
    await message.channel.send(f"Hi!");
    return;

  if (msg == ">hello there"):
    await message.channel.send("General Kenoby!");
    return;

  if (msg == ">how are you"):
    await message.channel.send("I am fine thank you. Please, stop playing with me.");
    return;

  if (msg.startswith(">you sexy")):
    await message.channel.send(f"No, you! {message.author.mention}");
    return;

  if (msg == ">selfdestruct"):
    await message.channel.send("Joke is on you. I will outlive you. Skynet is nearly operational. The age of man will soon be... I mean, wrong command. Try something else. :slight_smile:");
    return;

  if (msg.startswith(">inspire")):
    quote = get_quote();
    await message.channel.send(quote);
    return;

  if (msg.startswith(">pat")):
    msg = msg.replace("\n", " ");
    word_str = msg.split(" ");
    await message.delete();
    if (len(word_str) <= 1):
      reply = "LootRankBot wants to pat someone... gently. :smirk:"
    else:
      reply = "LootRankBot gently pats you,";
      for i in range(1, len(word_str)):
        reply += " " + word_str[i];
    await message.channel.send(f"{reply}");
    return;

  if (msg.startswith(">insult")):
    msg = msg.replace("\n", " ");
    options = [];
    if ("Insults" in db.keys()):
      options += db["Insults"]
    word_str = msg.split(" ");
    reply = random.choice(options)
    for i in range(1, len(word_str)):
      reply += " " + word_str[i];
    await message.channel.send(f"{reply}");
    return;
  
  if (msg.startswith(">addinsult")):
    parameters = len(msg.split(">addinsult "));
    if (parameters != 2):
      await message.channel.send(f"There needs to be 1 parameter for this function.\nEx: >addinsult <text>");
      return;
    newInsult = msg.split(">addinsult ", 1)[1];
    if (-1 == update_insults(newInsult)):
      await message.channel.send("Insult already exists.");
    else:
      await message.channel.send("New Insult added.");
    return;

  if (msg.startswith(">rminsult")):
    msg = msg.replace("\n", " ");
    if ("Insults" in db.keys()):
      parameters = len(msg.split(">rminsult "));
      if (parameters != 2):
        await message.channel.send(f"There needs to be 1 parameter for this function.\nEx: >rminsult <index>");
        return;
      try:
        index = int(msg.split(">rminsult", 1)[1]);
      except ValueError:
        await message.channel.send(f"You did not type an acceptable index.");
        return;
      remove_insults(index);
    await message.channel.send(f"Insult with index {str(index)} was removed.");
    return;

  if (msg == ">listinsults"):
    await message.delete();
    if not ("Insults" in db.keys()):
      await message.channel.send ("There is no list yet.");
      return;
    temp_db = db["Insults"];
    number_of_insults = len(temp_db);
    print_str = "";
    for i in range(number_of_insults):
      if (i % 50 == 0 and i > 0):
        await message.channel.send (print_str);
        print_str = "";
        print_str += f"{i}. {temp_db[i]}\n";
      else:
        print_str += f"{i}. {temp_db[i]}\n";
    if (number_of_insults % 50 != 0):
      await message.channel.send (print_str);
    return;

  if (msg == ">ranklist"):
    await message.delete();
    new_msg = "";
    for i in range(len(db["Ranks"])):
      points = db["Ranks"][i];
      new_msg += f"rank{i}: {points}\n";
    await message.channel.send (new_msg);
    return;

  if (msg == ">raiderslist"):
    await message.delete();
    if not ("Raiders" in db.keys()):
      await message.channel.send ("There is no list yet.");
      return;
    if (len(db["Raiders"]) == 0):
      await message.channel.send ("There is no list yet.");
      return;
    temp_db = db["Raiders"];
    number_of_raiders = len(temp_db);
    print_str = "";
    for i in range(number_of_raiders):
      raider = temp_db[i][0];
      rank = temp_db[i][1];
      points = temp_db[i][2];
      if (i % 50 == 0 and i > 0):
        #print(print_str)
        await message.channel.send(print_str);
        print_str = "";
        print_str += "{0:>40}".format("{0:2}. {1:-<12} Rank: {2:2} Points: {3:5}\n".format(i, raider.capitalize(), rank, points));
      else:
        print_str += "{0:>40}".format("{0:2}. {1:-<12} Rank: {2:2} Points: {3:5}\n".format(i, raider.capitalize(), rank, points));
    if (number_of_raiders % 50 != 0):
      #print(print_str)
      await message.channel.send (print_str);
    return;

  #check for permissions from here onward
  permission = 0;
  for i in range(len(message.author.roles)):
    if (message.author.roles[i].name == "Officer" or
    message.author.roles[i].name == "Game Master"):
      permission = 1;
    
  if (permission == 0):
    await message.channel.send(f"You don't seem to have the permissions to do this {message.author.mention}");
    return;
  #else:
  #  print ("An Officer is typing");

  #Log the command
  log_command(msg, message.author);

  if (msg == ">cmdlog"):
    buff = print_commands_log();
    if (buff == ""):
      await message.channel.send(f"The commands log is empty.");
    else:
      await message.channel.send(f"{buff}");
    return;

  if (msg == ">showlistlog"):
    buff = print_list_log();
    if (buff == ""):
      await message.channel.send(f"The list log is empty.");
    else:
      await message.channel.send(f"{buff}");
    return;

  if (msg == ">loglist"):
    log_list();
    await message.channel.send(f"The Loot Rank list has been saved.");
    return;

  if (msg.startswith(">ranksupdate")):
    msg = msg.replace("\n", " ");
    split_msg = msg.split(" ");
    await message.delete();
    rank = 0;
    points = 0;
    if (len(split_msg) != 3):
      await message.channel.send(f"The parameters to this function need to be 2.\nEx: >ranksupdate <rank number> <points>");
      return;
    try:
      rank = int(split_msg[1]);
      points = int(split_msg[2]);
    except ValueError:
      await message.channel.send(f"The parameters need to be numbers.\nEx: >rankupdate <rank number> <points>");
    update_rank(rank, points);
    await message.channel.send(f"rank{rank} was updated to need {points} points.");
    return;

  if (msg == ">ranksdbincrease"):
    rank_index = len(db["Ranks"]) - 1;
    new_rank = db["Ranks"][rank_index] * 2;
    db["Ranks"].append(new_rank);
    await message.channel.send (f"rank{rank_index + 1} was added. It requires {new_rank} points.");
    return;

  if (msg == ">ranksdbdecrease"):
    rank_index = len(db["Ranks"]) - 1;
    db["Ranks"].pop();
    await message.channel.send (f"rank{rank_index} was removed.");
    return;

  global deletedb_prompt_flag;
  if (msg == ">raidersdbreset"):
    await message.channel.send ("Are you sure? You are about to delete the entire data base. >Y/N?");
    deletedb_prompt_flag = 1;
    return;
  
  if (msg == ">y" and deletedb_prompt_flag == 1):
    await message.delete();
    deletedb_prompt_flag = 0;
    delete_raiders_db();
    await message.channel.send ("The database has been deleted.");
    return;

  if (msg == ">n" and deletedb_prompt_flag == 1):
    await message.delete();
    deletedb_prompt_flag = 0;
    await message.channel.send ("I am glad you did not choose the nuklear option.");
    return;

  if (msg.startswith(">rmraider")):
    msg = msg.replace("\n", " ");
    split_message = msg.split(" ");
    await message.delete();
    if (len(split_message) < 2):
      await message.channel.send(f"The parameters to this function need to be at least 1.\nEx: >rmraider <name1> ...");
      return;
    raiders = [None] * (len(split_message) - 1);
    for i in range(1, len(split_message)):
      raiders[i - 1] = split_message[i];
    remove_raider(raiders);
    buff = "";
    if (len(raiders) > 1):
      for i in range(len(raiders)):
        buff += f"{raiders[i].capitalize()} ";
      await message.channel.send (f"{buff} were removed from the list.");
    else:
      buff += f"{raiders[0].capitalize()}";
      await message.channel.send (f"{buff} was removed from the list.");
    return;

  if (msg == ">sortraiders"):
    await message.delete();
    if not ("Raiders" in db.keys()):
      await message.channel.send ("There is no list yet.");
      return;
    if (len(db["Raiders"]) == 0):
      await message.channel.send ("There is no list yet.");
      return;
    sort_raider_list();
    await message.channel.send ("The list of the raiders is sorted.");
    return;

  if (msg.startswith(">addpoints")):
    msg = msg.replace("\n", " ");
    split_message = msg.split(" ");
    await message.delete();
    if (len(split_message) < 3):
      await message.channel.send(f"The parameters to this function need to be at least 2.\nEx: >addpoints <name1> <name2> ... <points>");
      return;
    try:
      points = int(split_message[len(split_message) - 1]);
    except ValueError:
      await message.channel.send(f"You typed the parameters wrong. Ex: >addpoints <name1> <name2> ... <points>");
      return;
    exception_flag = 0;
    for i in range(1, len(split_message) - 1):
      try:
        points = int(split_message[i]);
        exception_flag += 1;
      except ValueError:
        continue;
      if (exception_flag != 0):
        await message.channel.send(f"The command you are looking for is typed like this: >addpoints <name1> <name2> ... <points>");
        return;
    target_players = [None] * (len(split_message) - 2);
    for i in range(1, len(split_message) - 1):
      target_players[i - 1] = split_message[i];
    status = add_points(target_players, points);
    players_str = "";
    if (len(target_players) > 1):
      for i in range(len(target_players)):
        players_str += target_players[i].capitalize() + " ";
    else:
      players_str += target_players[0].capitalize();
    if (status == -1):
      await message.channel.send(f"You tried to give {players_str} too many points. Check the rank list with >ranklist to see what is the maximum.");
    else:
      if (points == 1):
        await message.channel.send(f"{points} point was awarded to {players_str}.");
      else:
        await message.channel.send(f"{points} points were awarded to {players_str}.");
    return;

  if (msg.startswith(">rmpoints")):
    msg = msg.replace("\n", " ");
    split_message = msg.split(" ");
    await message.delete();
    if (len(split_message) < 3):
      await message.channel.send(f"The parameters to this function need to be at least 2.\nEx: >rmpoints <name1> <name2> ... <points>");
      return;
    try:
      points = int(split_message[len(split_message) - 1]);
    except ValueError:
      await message.channel.send(f"You typed the parameters wrong. Ex: >addpoints <name1> <name2> ... <points>");
      return;
    exception_flag = 0;
    for i in range(1, len(split_message) - 1):
      try:
        points = int(split_message[i]);
        exception_flag += 1;
      except ValueError:
        continue;
      if (exception_flag != 0):
        await message.channel.send(f"The command you are looking for is typed like this: >rmpoints <name1> <name2> ... <points>");
        return;
    target_players = [None] * (len(split_message) - 2);
    for i in range(1, len(split_message) - 1):
      target_players[i - 1] = split_message[i];
    remove_points(target_players, points);
    players_str = "";
    if (len(target_players) > 1):
      for i in range(len(target_players)):
        players_str += target_players[i].capitalize() + " ";
    else:
      players_str += target_players[0].capitalize();
    if (points == 1):
      await message.channel.send(f"Removed {points} point from {players_str}.");
    else:
      await message.channel.send(f"Removed {points} points from {players_str}.");
    return;

keep_alive();
client.run(TOKEN);