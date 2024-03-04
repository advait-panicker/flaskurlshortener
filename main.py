from flask import Flask, render_template, request, redirect
import json
from random import choice
from string import ascii_uppercase, ascii_lowercase, digits

app = Flask(__name__)

url_chars = ascii_uppercase + ascii_lowercase + digits

def random_string(n):
    return ''.join([choice(url_chars) for _ in range(n)])

with open('redirects.json', 'r') as f:
    links = json.loads(f.read())

@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'GET':
        return render_template('index.html', new_link="", shown=False)
    else:
        new_link = random_string(6)
        while links.get(new_link):
            new_link = random_string(6)
        links[new_link] = request.form['url']
        with open('redirects.json', 'w') as f:
            f.write(json.dumps(links))
        return render_template('index.html', new_link=new_link, shown=True)

@app.route('/<link>', methods=["GET"])
def find(link):
    if links.get(link):
        return redirect(links[link])
    else:
        return render_template('error.html')

if __name__ == '__main__':
    app.run(debug=True)