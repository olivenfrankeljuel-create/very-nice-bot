from flask import Flask, request, jsonify
import os
import nacl.signing
import nacl.exceptions

app = Flask(__name__)

PUBLIC_KEY = os.environ["DISCORD_PUBLIC_KEY"]


def verify_signature(req):
    signature = req.headers.get("X-Signature-Ed25519")
    timestamp = req.headers.get("X-Signature-Timestamp")

    if not signature or not timestamp:
        return False

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
def discord_interaction():

    # Tjek at request kommer fra Discord
    if not verify_signature(request):
        return "Invalid request", 401

    data = request.json

    # Discord endpoint verification
    if data["type"] == 1:
        return jsonify({
            "type": 1
        })

    # Slash command
    if data["type"] == 2:

        command_name = data["data"]["name"]

        if command_name == "verynicecommand":
            return jsonify({
                "type": 4,
                "data": {
                    "content": "@everyone @here hej:)",
                    "allowed_mentions": {
                        "parse": ["everyone"]
                    }
                }
            })

    return jsonify({})


@app.route("/", methods=["GET"])
def home():
    return "Discord user app is running!"


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )