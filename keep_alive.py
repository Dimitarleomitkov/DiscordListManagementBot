from flask import Flask, render_template
from threading import Thread
#import subprocess
#import platform
#import time
app = Flask(__name__)

@app.route('/')
def index():
  return "Hello. I am alive!";

def run():
  app.run(host='0.0.0.0', port=8080);

def keep_alive():
    t = Thread(target=run)
    t.start()
    