from flask import Flask, render_template
from threading import Thread
app = Flask(__name__)

@app.route('/')
def index():
  return "Hello. I am alive!"

def run():
  app.run(host='0.0.0.0', port=8080)

def keep_alive():
    print ("This is Jimmy!")
    t = Thread(target=run)
    t.start()

#def ping_myself():
#    host = "https://DiscordListManagementBot.undeadko.repl.co"
#
#    ping = subprocess.Popen(
#        ["ping", "-c", "4", host],
#        stdout = subprocess.PIPE,
#        stderr = subprocess.PIPE
#    )

#    out, error = ping.communicate()



