"""Normalization helpers for raw Live Client API payloads."""

from __future__ import annotations

from typing import Any, Dict, List


def build_game_state(raw_data: Dict[str, Any], error: str | None = None) -> Dict[str, Any]:
    """Transform raw live data into the project's internal GameState shape."""
    if not raw_data:
        return _empty_state(error)

    game_data = raw_data.get("gameData") or {}
    active_player = raw_data.get("activePlayer") or {}
    raw_players = raw_data.get("allPlayers") or []
    players = [_normalize_player(player) for player in raw_players if isinstance(player, dict)]

    if not players:
        return _empty_state(error or "No active players were returned by the Live Client API.")

    active_player_name = (
        active_player.get("summonerName")
        or raw_data.get("activePlayerName")
        or players[0]["summoner_name"]
    )

    player = _find_player(players, active_player_name) or players[0]
    player = _enrich_active_player(player, active_player)

    ally_roster = [teammate for teammate in players if teammate["team"] == player["team"]]
    enemy_roster = [opponent for opponent in players if opponent["team"] != player["team"]]
    allies = [teammate for teammate in ally_roster if teammate["summoner_name"] != player["summoner_name"]]

    ally_totals = _team_totals(ally_roster)
    enemy_totals = _team_totals(enemy_roster)
    game_time_seconds = int(float(game_data.get("gameTime") or 0))
    map_number = int(game_data.get("mapNumber") or 0)

    return {
        "status": "in_game",
        "connection_error": error,
        "map": {
            "name": game_data.get("mapName", "Unknown map"),
            "mode": game_data.get("gameMode", "Unknown mode"),
            "number": map_number,
        },
        "map_number": map_number,
        "game_time": _format_timer(game_time_seconds),
        "game_time_seconds": game_time_seconds,
        "phase": _resolve_phase(game_time_seconds),
        "player": player,
        "allies": allies,
        "enemies": enemy_roster,
        "team_stats": {
            "allies": ally_totals,
            "enemies": enemy_totals,
            "kill_diff": ally_totals["kills"] - enemy_totals["kills"],
        },
        "events": _normalize_events(raw_data.get("events", {}).get("Events", [])),
    }


def _normalize_player(raw_player: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a raw player payload into a smaller internal representation."""
    scores = raw_player.get("scores") or {}
    items = raw_player.get("items") or []

    return {
        "summoner_name": raw_player.get("summonerName")
        or raw_player.get("riotIdGameName")
        or "Unknown",
        "champion_name": raw_player.get("championName", "Unknown"),
        "team": raw_player.get("team", ""),
        "level": int(raw_player.get("level") or 0),
        "is_alive": not bool(raw_player.get("isDead")),
        "respawn_timer": int(float(raw_player.get("respawnTimer") or 0)),
        "kills": int(scores.get("kills") or 0),
        "deaths": int(scores.get("deaths") or 0),
        "assists": int(scores.get("assists") or 0),
        "cs": int(scores.get("creepScore") or 0),
        "ward_score": int(scores.get("wardScore") or 0),
        "position": raw_player.get("position") or "",
        "items": [_normalize_item(item) for item in items if isinstance(item, dict)],
    }


def _normalize_item(raw_item: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize a single item payload."""
    return {
        "id": int(raw_item.get("itemID") or 0),
        "name": raw_item.get("displayName", "Unknown item"),
        "slot": int(raw_item.get("slot") or 0),
    }


def _enrich_active_player(
    player: Dict[str, Any], active_player: Dict[str, Any]
) -> Dict[str, Any]:
    """Attach active-player-only fields such as current gold and health."""
    champion_stats = active_player.get("championStats") or {}
    enriched_player = dict(player)
    enriched_player["current_gold"] = int(active_player.get("currentGold") or 0)
    enriched_player["health"] = {
        "current": int(float(champion_stats.get("currentHealth") or 0)),
        "max": int(float(champion_stats.get("maxHealth") or 0)),
    }
    enriched_player["resource"] = {
        "current": int(float(champion_stats.get("resourceValue") or 0)),
        "max": int(float(champion_stats.get("resourceMax") or 0)),
    }
    return enriched_player


def _find_player(players: List[Dict[str, Any]], summoner_name: str) -> Dict[str, Any] | None:
    """Locate the active player inside the normalized roster."""
    for player in players:
        if player["summoner_name"] == summoner_name:
            return player
    return None


def _team_totals(players: List[Dict[str, Any]]) -> Dict[str, int]:
    """Aggregate team combat and farm totals."""
    return {
        "kills": sum(player["kills"] for player in players),
        "deaths": sum(player["deaths"] for player in players),
        "assists": sum(player["assists"] for player in players),
        "cs": sum(player["cs"] for player in players),
    }


def _normalize_events(raw_events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Keep only the event fields required by the first assistant version."""
    normalized_events = []

    for event in raw_events:
        if not isinstance(event, dict):
            continue
        normalized_events.append(
            {
                "event_name": event.get("EventName", ""),
                "event_time": int(float(event.get("EventTime") or 0)),
                "killer_name": event.get("KillerName", ""),
                "victim_name": event.get("VictimName", ""),
                "dragon_type": event.get("DragonType", ""),
            }
        )

    return normalized_events


def _resolve_phase(game_time_seconds: int) -> str:
    """Split the match into coarse phases for rule-based coaching."""
    if game_time_seconds < 900:
        return "early"
    if game_time_seconds < 1800:
        return "mid"
    return "late"


def _format_timer(seconds: int) -> str:
    """Format seconds as mm:ss."""
    minutes, remainder = divmod(max(seconds, 0), 60)
    return f"{minutes:02d}:{remainder:02d}"


def _empty_state(error: str | None) -> Dict[str, Any]:
    """Return the API shape used when no match is active."""
    return {
        "status": "not_in_game",
        "connection_error": error or "Live Client API no disponible.",
        "map": {"name": "Unknown map", "mode": "Unknown mode", "number": 0},
        "map_number": 0,
        "game_time": "00:00",
        "game_time_seconds": 0,
        "phase": "waiting",
        "player": {},
        "allies": [],
        "enemies": [],
        "team_stats": {
            "allies": {"kills": 0, "deaths": 0, "assists": 0, "cs": 0},
            "enemies": {"kills": 0, "deaths": 0, "assists": 0, "cs": 0},
            "kill_diff": 0,
        },
        "events": [],
    }
