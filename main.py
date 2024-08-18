from flask import Flask, render_template, request, redirect
import json
from random import choice
from string import ascii_uppercase, ascii_lowercase, digits
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv(override=True)

app = Flask(__name__)

url_chars = ascii_uppercase + ascii_lowercase + digits

def random_string(n):
    return ''.join([choice(url_chars) for _ in range(n)])

connection_string = os.getenv('MONGO_CONNECTION_STRING', 'mongodb://localhost:27017/')

client = MongoClient(connection_string)
db = client['url_shortener']
collection = db['links']

collection.create_index([("shortened_link", 1)], unique=True)

@app.route('/', methods=["GET", "POST"])
def index():
    app.logger.debug(f"Request method: {request.form}")
    if request.method == 'GET':
        return render_template('index.html', new_link="", shown=False)
    app.logger.debug(f"Generating new link")
    new_link = random_string(6)
    while collection.find_one({'shortened_link': new_link}):
        app.logger.debug(f"Link {new_link} already exists, generating new link")
        new_link = random_string(6)
    app.logger.debug(f"Generated new link: {new_link}")
    collection.insert_one({'shortened_link': new_link, 'original_url': request.form['url']})
    app.logger.debug(f"Inserted new link into database")
    return render_template('index.html', new_link=new_link, shown=True)

@app.route('/<link>', methods=["GET"])
def find(link):
    app.logger.debug(f"Finding link {link}")
    query = collection.find_one({'shortened_link': link})
    if query:
        app.logger.debug(f"Link found, redirecting to {query['original_url']}")
        return redirect(query['original_url'])
    app.logger.debug(f"Link not found")
    return render_template('error.html')

if __name__ == '__main__':
    debug = os.getenv('DEBUG', 'False') == 'True'

    print(f"Connecting to {connection_string}")
    print(f"Debug mode: {debug}")
    
    app.run(host='0.0.0.0', port=5000, debug=debug)