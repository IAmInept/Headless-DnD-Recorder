from flask import Flask, send_file, send_from_directory

app = Flask(__name__)

@app.get("/")
def home():
    return send_file("frontend/dist/index.html")

@app.get("/<path:name>")
def public(name):
    return send_from_directory("frontend/dist/", name)

@app.get("/assets/<path:name>")
def assets(name):
    return send_from_directory("frontend/dist/assets/", name)

@app.get("/api/on")
def callScript():
    return "Success"

@app.get("/api/off")
def callScript():
    return "Success"