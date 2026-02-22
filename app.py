import os
from typing import Any

import requests
from flask import Flask, jsonify, render_template, request


app = Flask(__name__)
RASA_ENDPOINT = os.getenv("RASA_ENDPOINT", "http://127.0.0.1:5005/webhooks/rest/webhook")
RASA_TIMEOUT_SECONDS = int(os.getenv("RASA_TIMEOUT_SECONDS", "20"))
WEB_PORT = int(os.getenv("WEB_PORT", "8010"))


@app.get("/")
def home() -> str:
    return render_template("index.html")


@app.get("/health")
def health() -> Any:
    rasa_ok = False
    try:
        status_resp = requests.get("http://127.0.0.1:5005/status", timeout=2)
        rasa_ok = status_resp.ok
    except requests.RequestException:
        rasa_ok = False

    return jsonify(
        {
            "status": "ok",
            "rasa_endpoint": RASA_ENDPOINT,
            "rasa_online": rasa_ok,
        }
    )


@app.post("/api/chat")
def api_chat() -> Any:
    payload = request.get_json(silent=True) or {}
    message = str(payload.get("message", "")).strip()
    sender = str(payload.get("sender", "web-user")).strip() or "web-user"

    if not message:
        return jsonify({"error": "Message is required."}), 400

    try:
        response = requests.post(
            RASA_ENDPOINT,
            json={"sender": sender, "message": message},
            timeout=RASA_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
    except requests.RequestException:
        return (
            jsonify(
                {
                    "error": "Rasa server is offline. Start it with: python -m rasa run --enable-api --cors \"*\""
                }
            ),
            502,
        )

    data = response.json()
    messages = []
    for item in data:
        messages.append(
            {
                "text": item.get("text"),
                "image": item.get("image"),
                "buttons": item.get("buttons", []),
            }
        )

    if not messages:
        messages = [{"text": "No reply from model.", "image": None, "buttons": []}]

    return jsonify({"messages": messages})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=WEB_PORT, debug=False, use_reloader=False)
