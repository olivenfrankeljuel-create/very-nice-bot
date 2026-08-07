from flask import Flask, request
import nacl.signing
import requests
import os

app = Flask(__name__)

PUBLIC_KEY = "7c006fc3331bfd382594fe8c0e8af0cd2e5b7900ecf42137e5748300da0a8960"

@app.route("/", methods=["POST"])
def interactions():
    data = request.json

    # Discord ping test
    if data["type"] == 1:
        return {"type": 1}

    # Slash command
    if data["type"] == 2:
        command = data["data"]["name"]

        if command == "verynicecommand":
            return {
                "type": 4,
                "data": {
                    "content": "@everyone @here hej:)\n" * 20,
                    "allowed_mentions": {
                        "parse": ["everyone"]
                    }
                }
            }

    return {}

@app.route("/")
def home():
    return "Bot online"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)