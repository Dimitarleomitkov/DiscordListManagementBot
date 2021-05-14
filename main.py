import os
import discord
import requests
import json
import random
from keep_alive import keep_alive
from replit import db

TOKEN = os.environ['TOKEN']

client = discord.Client();

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

  options = [];

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
    if ("Insults" in db.keys()):
      index = int(msg.split("$rminsult", 1)[1]);
      remove_insults(index);
    await message.channel.send(f"Insult with index {str(index)} was removed." );

  if (msg.startswith("$listinsults")):
    for index, each in enumerate(db["Insults"]):
      await message.channel.send(f"{str(index)}. {each}");

keep_alive();
client.run(TOKEN);