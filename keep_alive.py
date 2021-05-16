from flask import Flask, render_template
from threading import Thread
import platform    # For getting the operating system name
import subprocess  # For executing a shell command
import time
app = Flask(__name__)

@app.route('/')
def index():
  return "Hello. I am alive!"

def run():
  app.run(host='0.0.0.0', port=8080)

def ping():
  while 1:
      host = "https://DiscordListManagementBot.undeadko.repl.co";

      # Building the command. Ex: "ping -c 1 google.com"
      command = ['ping', '/n', '1', host]

      debuf_stuff = subprocess.run(command, shell = True, stdout = subprocess.PIPE);

      print (f"{debuf_stuff}");
      time.sleep(5);

def keep_alive():
    t = Thread(target=run)
    t.start()
#    t2 = Thread(target=ping)
#    t2.start()
    