from flask import Flask, send_file

app = Flask(__name__)

@app.route("/")
def mainPage():
    return send_file("src/index.html")