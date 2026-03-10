from flask import Flask, jsonify, render_template, request

from ai_assistant import AssistantEngine

app = Flask(__name__)
engine = AssistantEngine()


@app.route("/")
def home():
    return render_template("index.html")


@app.post("/api/chat")
def chat():
    payload = request.get_json(silent=True) or {}
    prompt = (payload.get("message") or "").strip()

    if not prompt:
        return jsonify({"error": "message is required"}), 400

    reply = engine.ask(prompt)
    return jsonify({"reply": reply, "history": [m.__dict__ for m in engine.history]})


@app.post("/api/clear")
def clear():
    engine.clear()
    return jsonify({"ok": True})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
