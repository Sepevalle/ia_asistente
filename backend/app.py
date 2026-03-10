"""Flask API entrypoint for the live assistant."""

from __future__ import annotations

from flask import Flask, jsonify, request

from ai_coach import analyze_game
from game_state import build_game_state
from live_client import get_live_data
from objectives import build_objectives

app = Flask(__name__)


@app.after_request
def add_cors_headers(response):
    """Allow the local Electron overlay to fetch API responses."""
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response


@app.route("/health")
def healthcheck():
    """Expose a lightweight process health endpoint."""
    return jsonify({"status": "ok"})


@app.route("/game")
def game_state():
    """Return the current normalized game state and coaching suggestions."""
    use_demo = request.args.get("demo") == "1"
    raw_data, error, live_client_meta = get_live_data(use_demo=use_demo)

    state = build_game_state(raw_data, error=error)
    state["objectives"] = build_objectives(state)

    analysis = analyze_game(state)

    payload = {
        "status": state["status"],
        "source": "demo" if use_demo else "live_client",
        "connection_error": state.get("connection_error"),
        "map": state["map"],
        "phase": state["phase"],
        "game_time": state["game_time"],
        "game_time_seconds": state["game_time_seconds"],
        "player": state["player"],
        "allies": state["allies"],
        "enemies": state["enemies"],
        "team_stats": state["team_stats"],
        "event_summary": state["event_summary"],
        "team_context": state["team_context"],
        "tactical": state["tactical"],
        "objectives": state["objectives"],
        "summary": analysis["summary"],
        "signals": analysis["signals"],
        "suggestions": analysis["suggestions"],
        "live_client": live_client_meta,
    }

    return jsonify(payload)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
