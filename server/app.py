import os
from flask_cors import CORS
from threading import Thread
from flask import Flask, send_from_directory

app = Flask('Accounting Bot', static_folder='../frontend/dist')
# app.cli.add_command(create_tables)

CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/')
def home():
	return send_from_directory(app.static_folder, 'index.html')

def run():
	app.run(host='0.0.0.0',port=os.getenv('PORT', 8080))

def keep_alive():
	print("keep alive..")
	t = Thread(target=run)
	t.start()
