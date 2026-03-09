"""Objective timer calculations for Summoner's Rift."""

from __future__ import annotations

from typing import Any, Dict, List

SUMMONERS_RIFT_MAP_NUMBER = 11

DRAGON_FIRST_SPAWN = 5 * 60
DRAGON_RESPAWN = 5 * 60
BARON_FIRST_SPAWN = 20 * 60
BARON_RESPAWN = 6 * 60


def build_objectives(game_state: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """Calculate key objective timers from the normalized game state."""
    if game_state.get("map_number") != SUMMONERS_RIFT_MAP_NUMBER:
        return {}

    game_time = game_state.get("game_time_seconds", 0)
    events = game_state.get("events", [])

    dragon_kills = _extract_event_times(events, "dragon")
    baron_kills = _extract_event_times(events, "baron")

    return {
        "dragon": _build_recurring_objective(
            "Dragon",
            game_time,
            dragon_kills,
            DRAGON_FIRST_SPAWN,
            DRAGON_RESPAWN,
            "Prioriza vision de rio y prioridad de bot/mid.",
        ),
        "baron": _build_recurring_objective(
            "Baron",
            game_time,
            baron_kills,
            BARON_FIRST_SPAWN,
            BARON_RESPAWN,
            "Controla vision superior y empuja mid antes de empezar.",
        ),
    }


def _build_recurring_objective(
    name: str,
    game_time: int,
    kill_times: List[int],
    first_spawn: int,
    respawn: int,
    hint: str,
) -> Dict[str, Any]:
    """Build a recurring objective descriptor used by the overlay."""
    if game_time < first_spawn:
        return _objective_payload(
            name=name,
            status="spawning",
            seconds_until_spawn=first_spawn - game_time,
            is_alive=False,
            hint=hint,
        )

    if not kill_times:
        return _objective_payload(
            name=name,
            status="alive",
            seconds_until_spawn=0,
            is_alive=True,
            hint=hint,
        )

    next_spawn = kill_times[-1] + respawn
    if game_time >= next_spawn:
        return _objective_payload(
            name=name,
            status="alive",
            seconds_until_spawn=0,
            is_alive=True,
            hint=hint,
        )

    return _objective_payload(
        name=name,
        status="respawning",
        seconds_until_spawn=next_spawn - game_time,
        is_alive=False,
        hint=hint,
    )


def _objective_payload(
    name: str,
    status: str,
    seconds_until_spawn: int,
    is_alive: bool,
    hint: str,
) -> Dict[str, Any]:
    """Create a uniform objective payload."""
    return {
        "name": name,
        "status": status,
        "is_alive": is_alive,
        "seconds_until_spawn": max(seconds_until_spawn, 0),
        "timer": "Disponible" if is_alive else _format_timer(seconds_until_spawn),
        "hint": hint,
    }


def _extract_event_times(events: List[Dict[str, Any]], keyword: str) -> List[int]:
    """Extract event times matching an objective keyword."""
    keyword = keyword.lower()
    matching_times = []

    for event in events:
        event_name = str(event.get("event_name", "")).lower()
        if keyword in event_name:
            matching_times.append(int(event.get("event_time", 0)))

    return matching_times


def _format_timer(seconds: int) -> str:
    """Format seconds as mm:ss."""
    minutes, remainder = divmod(max(seconds, 0), 60)
    return f"{minutes:02d}:{remainder:02d}"
