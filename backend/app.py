from flask import Flask, jsonify
from live_client import get_live_data
from ai_coach import analyze_game

app = Flask(__name__)

@app.route("/game")
def game_state():
    data = get_live_data()
    analysis = analyze_game(data)
    return jsonify(analysis)

if __name__ == "__main__":
    app.run(port=5000)