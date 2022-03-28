import os
from flask import Flask, request
from threading import Thread
from database import add_expense, total

app = Flask('Accounting Bot')
# app.cli.add_command(create_tables)

@app.route('/')
def home():
	return "I'm alive"

def run():
	app.run(host='0.0.0.0',port=os.getenv('PORT', 8080))

def keep_alive():
	print("keep alive..")
	t = Thread(target=run)
	t.start()
