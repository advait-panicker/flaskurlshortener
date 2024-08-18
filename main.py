from flask import Flask, render_template, request, redirect
import json
from random import choice
from string import ascii_uppercase, ascii_lowercase, digits
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

url_chars = ascii_uppercase + ascii_lowercase + digits

def random_string(n):
    return ''.join([choice(url_chars) for _ in range(n)])

connection_string = os.getenv('MONGO_CONNECTION_STRING')
client = MongoClient(connection_string)
db = client['url_shortener']
collection = db['links']

collection.create_index([("shortened_link", 1)], unique=True)

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'GET':
        return render_template('index.html', new_link="", shown=False)
    new_link = random_string(6)
    while collection.find_one({'shortened_link': new_link}):
        new_link = random_string(6)
    collection.insert_one({'shortened_link': new_link, 'original_url': request.form['url']})
    return render_template('index.html', new_link=new_link, shown=True)

@app.route('/<link>', methods=["GET"])
def find(link):
    query = collection.find_one({'shortened_link': link})
    if query:
        return redirect(query['original_url'])
    return render_template('error.html')

if __name__ == '__main__':
    debug = os.getenv('DEBUG', 'False') == 'True'
    app.run(host='0.0.0.0', port=5000, debug=debug)