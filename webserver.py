from flask import Flask, send_file, send_from_directory, jsonify
import main
import asyncio

app = Flask(__name__)
demo = main.HeadlessServer()

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
    demo.initBuffer()
    asyncio.run(demo.initBrowser())
    return jsonify({"Status": "Running"})

@app.get("/api/off")
def cancelScript():
    asyncio.run(demo.stopRecording())
    return jsonify({"Status": "Closed"})
