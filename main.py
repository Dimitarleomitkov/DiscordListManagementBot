import os
import discord.py
import requests
import json
import random
from replit import db


TOKEN = os.environ['TOKEN']

client = discord.Client();

starter_Insults = [];
Raiders = [];
Raider_ranks = [];
Raider_points = [];
Points_for_ranks = []

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

def add_raider():
  return;

@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client));

@client.event
async def on_message(message):
  if (message.author == client.user):
    return;
  
  msg = message.content.lower();

  if (msg.startswith("$hello there")):
    await message.channel.send("General Kenoby!");

  if (msg.startswith("$how are you")):
    await message.channel.send("I am fine thank you. Please, stop playing with me.");

  if (msg.startswith("$you sexy")):
    await message.channel.send("No, you!");

  if (msg.startswith("$inspire")):
    quote = get_quote();
    await message.channel.send(quote);

  options = starter_Insults;

  if ("Insults" in db.keys()):
    options += db["Insults"]

  if (msg.startswith("$insult")):
    await message.channel.send(random.choice(options));
  
  if (msg.startswith("$addinsult")):
    newInsult = msg.split("$addinsult ", 1)[1];
    if (-1 == update_insults(newInsult)):
      await message.channel.send("Insult already exists.");
    else:
      await message.channel.send("New Insult added.");

  if (msg.startswith("$rminsult")):
    Insults = [];
    if ("Insults" in db.keys()):
      index = int(msg.split("$rminsult", 1)[1]);
      remove_insults(index);
      Insults = db["Insults"];
    await message.channel.send("Insult with index " + str(index) + " was removed." );

  if (msg.startswith("$listinsults")):
    i = 0;
    for each in db["Insults"]:
      await message.channel.send(str(i) + ". " + each);
      i = i + 1;

client.run (TOKEN);