"""Enemy jungle tracking heuristics for v1.1 gank awareness."""

from __future__ import annotations

from typing import Any, Dict, List

from recommendations import find_team_jungler

SUMMONERS_RIFT_MAP_NUMBER = 11
DIAGONAL_THRESHOLD = 1000


def analyze_enemy_jungler(game_state: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze enemy jungler positioning to produce gank-awareness signals."""
    if game_state.get("status") != "in_game":
        return _empty_tracking()

    enemies = game_state.get("enemies", [])
    enemy_jungler = find_team_jungler(enemies)
    if not enemy_jungler:
        return _empty_tracking()

    game_time = int(game_state.get("game_time_seconds", 0))
    events = game_state.get("events", [])

    last_seen = _resolve_last_seen(enemy_jungler, events, game_time)
    predicted_side = _infer_side(last_seen.get("position"), game_state.get("map_number", 0))
    gank_window = _in_gank_window(game_time)
    gank_risk = _resolve_gank_risk(enemy_jungler, last_seen.get("age_seconds"), gank_window)
    hint = _build_hint(enemy_jungler, predicted_side, gank_risk, last_seen.get("age_seconds"), gank_window)

    return {
        "enemy_jungler": _player_glance(enemy_jungler),
        "last_seen_time": last_seen.get("time"),
        "last_seen_age": last_seen.get("age_seconds"),
        "last_seen_position": last_seen.get("position"),
        "last_seen_source": last_seen.get("source"),
        "predicted_side": predicted_side,
        "gank_window": gank_window,
        "gank_risk": gank_risk,
        "hint": hint,
    }


def _resolve_last_seen(
    enemy_jungler: Dict[str, Any],
    events: List[Dict[str, Any]],
    game_time: int,
) -> Dict[str, Any]:
    """Resolve the most recent known location for the enemy jungler."""
    map_position = _normalize_position(enemy_jungler.get("map_position"))
    if enemy_jungler.get("is_alive") and map_position:
        return {
            "time": game_time,
            "age_seconds": 0,
            "position": map_position,
            "source": "snapshot",
        }

    latest_event = None
    for event in events:
        if not _event_mentions(event, enemy_jungler):
            continue
        if latest_event is None or event["event_time"] > latest_event["event_time"]:
            latest_event = event

    if latest_event:
        position = _normalize_position(latest_event.get("position"))
        age = max(game_time - latest_event["event_time"], 0)
        return {
            "time": latest_event["event_time"],
            "age_seconds": age,
            "position": position,
            "source": "event" if position else "event_no_pos",
        }

    lane_position = enemy_jungler.get("position")
    if enemy_jungler.get("is_alive") and lane_position:
        return {
            "time": None,
            "age_seconds": None,
            "position": lane_position,
            "source": "role_hint",
        }

    return {"time": None, "age_seconds": None, "position": None, "source": "unknown"}


def _event_mentions(event: Dict[str, Any], enemy_jungler: Dict[str, Any]) -> bool:
    """Check whether the event references the given enemy jungler."""
    name_variants = _name_variants(enemy_jungler)
    if not name_variants:
        return False
    killer_name = event.get("killer_name", "")
    victim_name = event.get("victim_name", "")
    if killer_name in name_variants or victim_name in name_variants:
        return True
    killer_lower = killer_name.lower()
    victim_lower = victim_name.lower()
    return killer_lower in name_variants or victim_lower in name_variants


def _infer_side(position: Dict[str, int] | str | None, map_number: int) -> str:
    """Infer which side of the map the position indicates."""
    if map_number != SUMMONERS_RIFT_MAP_NUMBER or not position:
        return "unknown"

    if isinstance(position, dict):
        x = position.get("x")
        y = position.get("y")
        if x is None or y is None:
            return "unknown"
        if abs(x - y) <= DIAGONAL_THRESHOLD:
            return "mid"
        return "top" if x > y else "bot"

    if isinstance(position, str):
        lane = position.strip().upper()
        if lane in {"TOP"}:
            return "top"
        if lane in {"BOTTOM", "BOT"}:
            return "bot"
        if lane in {"MIDDLE", "MID"}:
            return "mid"
        if lane in {"UTILITY", "SUPPORT"}:
            return "bot"
        return "unknown"

    return "unknown"


def _in_gank_window(game_time: int) -> bool:
    """Return whether the match is in early gank-heavy windows."""
    return (180 <= game_time <= 270) or (330 <= game_time <= 420)


def _resolve_gank_risk(
    enemy_jungler: Dict[str, Any],
    last_seen_age: int | None,
    gank_window: bool,
) -> str:
    """Convert last-seen age into a coarse gank risk level."""
    if not enemy_jungler.get("is_alive", True):
        return "low"

    if last_seen_age is None:
        return "high" if gank_window else "medium"

    if last_seen_age >= 45:
        return "high"
    if last_seen_age >= 25:
        return "medium"
    return "low"


def _build_hint(
    enemy_jungler: Dict[str, Any],
    predicted_side: str,
    gank_risk: str,
    last_seen_age: int | None,
    gank_window: bool,
) -> str:
    """Create a short hint to accompany jungle tracking."""
    if not enemy_jungler.get("is_alive", True):
        return "Jungla rival muerto: hay ventana para vision profunda o objetivo."

    if gank_risk == "high":
        if predicted_side in {"top", "bot"}:
            return f"JG enemigo sin info: probable lado {predicted_side}, guarda ward y respeta oleada."
        return "JG enemigo sin info: juega seguro y no empujes sin vision."

    if gank_risk == "medium" and gank_window:
        return "Ventana de gank temprano: no des trade largo sin vision del rio."

    if predicted_side in {"top", "bot"} and last_seen_age is not None and last_seen_age <= 15:
        opposite = "bot" if predicted_side == "top" else "top"
        return f"JG visto {predicted_side}: puedes jugar mas agresivo en lado {opposite}."

    return ""


def _player_glance(player: Dict[str, Any]) -> Dict[str, Any]:
    """Return a trimmed view for UI consumption."""
    return {
        "summoner_name": player.get("summoner_name", ""),
        "riot_id_game_name": player.get("riot_id_game_name", ""),
        "champion_name": player.get("champion_name", ""),
        "is_alive": player.get("is_alive", True),
        "respawn_timer": player.get("respawn_timer", 0),
        "level": player.get("level", 0),
        "cs": player.get("cs", 0),
    }


def _normalize_position(raw_position: Any) -> Dict[str, int] | None:
    """Normalize a raw position payload into integer coordinates."""
    if not isinstance(raw_position, dict):
        return None

    x = raw_position.get("x")
    y = raw_position.get("y")
    if x is None or y is None:
        return None

    try:
        return {"x": int(float(x)), "y": int(float(y))}
    except (TypeError, ValueError):
        return None


def _name_variants(player: Dict[str, Any]) -> set[str]:
    """Return a set of known name variants for a player."""
    variants = set()
    for key in ("summoner_name", "riot_id_game_name"):
        value = player.get(key)
        if value:
            variants.add(value)
            variants.add(value.split("#", 1)[0])
            variants.add(value.lower())
            variants.add(value.split("#", 1)[0].lower())
    return {item for item in variants if item}


def _empty_tracking() -> Dict[str, Any]:
    """Return an empty jungle tracking payload."""
    return {
        "enemy_jungler": None,
        "last_seen_time": None,
        "last_seen_age": None,
        "last_seen_position": None,
        "last_seen_source": "unknown",
        "predicted_side": "unknown",
        "gank_window": False,
        "gank_risk": "unknown",
        "hint": "",
    }
