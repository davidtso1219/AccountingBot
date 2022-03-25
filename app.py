import os
from flask import Flask
from threading import Thread

app = Flask('accounting bot')

@app.route('/')
def home():
	return "I'm alive"

def run():
	app.run(host='0.0.0.0',port=os.getenv('PORT', 8080))

def keep_alive():
	print("keep alive..")
	t = Thread(target=run)
	t.start()
