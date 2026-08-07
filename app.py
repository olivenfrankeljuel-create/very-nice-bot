from flask import Flask, request, jsonify
import nacl.signing
import nacl.exceptions
import os

app = Flask(__name__)

PUBLIC_KEY = os.environ["DISCORD_PUBLIC_KEY"]


def verify_signature(req):
    signature = req.headers["X-Signature-Ed25519"]
    timestamp = req.headers["X-Signature-Timestamp"]

    body = req.data.decode("utf-8")

    verify_key = nacl.signing.VerifyKey(
        bytes.fromhex(PUBLIC_KEY)
    )

    try:
        verify_key.verify(
            (timestamp + body).encode(),
            bytes.fromhex(signature)
        )
        return True
    except nacl.exceptions.BadSignatureError:
        return False


@app.route("/", methods=["POST"])
def interactions():

    if not verify_signature(request):
        return "Invalid request", 401

    data = request.json

    # Discord verification
    if data["type"] == 1:
        return jsonify({
            "type": 1
        })


    # Slash command
    if data["type"] == 2:

        if data["data"]["name"] == "verynicecommand":

            return jsonify({
                "type": 4,
                "data": {
                    "content": "hej :)"
                }
            })


    return jsonify({})


@app.route("/")
def home():
    return "Discord app online"


app.run(
    host="0.0.0.0",
    port=int(os.environ.get("PORT",5000))
)