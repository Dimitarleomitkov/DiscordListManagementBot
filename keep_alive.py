from flask import Flask, render_template
#import subprocess
app = Flask(__name__)

@app.route('/')
def index():
  return "Hello. I am alive!"

app.run(host='0.0.0.0', port=8080)

#def keep_alive():
#    t = Thread(target=run)
#    t.start()

#def ping_myself():
#    host = "https://DiscordListManagementBot.undeadko.repl.co"
#
#    ping = subprocess.Popen(
#        ["ping", "-c", "4", host],
#        stdout = subprocess.PIPE,
#        stderr = subprocess.PIPE
#    )

#    out, error = ping.communicate()



