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
    ally_team = game_state.get("player", {}).get("team", "")
    enemy_team = "CHAOS" if ally_team == "ORDER" else "ORDER"
    tactical = game_state.get("tactical", {})

    dragon_kill_events = [event for event in events if event["event_name"] == "DragonKill"]
    baron_kill_events = [event for event in events if event["event_name"] == "BaronKill"]

    ally_dragons = _count_team_objectives(dragon_kill_events, ally_team)
    enemy_dragons = _count_team_objectives(dragon_kill_events, enemy_team)

    dragon = _build_recurring_objective(
        name="Dragon",
        game_time=game_time,
        kill_events=dragon_kill_events,
        first_spawn=DRAGON_FIRST_SPAWN,
        respawn=DRAGON_RESPAWN,
    )
    dragon["ally_stacks"] = ally_dragons
    dragon["enemy_stacks"] = enemy_dragons
    dragon["priority"] = _resolve_objective_priority(dragon, tactical)
    dragon["hint"] = _dragon_hint(dragon, tactical, ally_dragons, enemy_dragons)

    baron = _build_recurring_objective(
        name="Baron",
        game_time=game_time,
        kill_events=baron_kill_events,
        first_spawn=BARON_FIRST_SPAWN,
        respawn=BARON_RESPAWN,
    )
    baron["priority"] = _resolve_objective_priority(baron, tactical)
    baron["hint"] = _baron_hint(baron, tactical)

    return {
        "dragon": dragon,
        "baron": baron,
    }


def _build_recurring_objective(
    name: str,
    game_time: int,
    kill_events: List[Dict[str, Any]],
    first_spawn: int,
    respawn: int,
) -> Dict[str, Any]:
    """Build a recurring objective descriptor used by the overlay."""
    if game_time < first_spawn:
        return _objective_payload(
            name=name,
            status="spawning",
            seconds_until_spawn=first_spawn - game_time,
            is_alive=False,
        )

    if not kill_events:
        return _objective_payload(
            name=name,
            status="alive",
            seconds_until_spawn=0,
            is_alive=True,
        )

    next_spawn = kill_events[-1]["event_time"] + respawn
    if game_time >= next_spawn:
        return _objective_payload(
            name=name,
            status="alive",
            seconds_until_spawn=0,
            is_alive=True,
        )

    return _objective_payload(
        name=name,
        status="respawning",
        seconds_until_spawn=next_spawn - game_time,
        is_alive=False,
    )


def _objective_payload(
    name: str,
    status: str,
    seconds_until_spawn: int,
    is_alive: bool,
) -> Dict[str, Any]:
    """Create a uniform objective payload."""
    return {
        "name": name,
        "status": status,
        "is_alive": is_alive,
        "seconds_until_spawn": max(seconds_until_spawn, 0),
        "timer": "Disponible" if is_alive else _format_timer(seconds_until_spawn),
    }


def _resolve_objective_priority(
    objective: Dict[str, Any],
    tactical: Dict[str, Any],
) -> str:
    """Resolve an action priority for the current objective window."""
    if not objective.get("is_alive") and objective.get("seconds_until_spawn", 999) > 90:
        return "low"

    if tactical.get("enemy_jungler_dead") or tactical.get("alive_diff", 0) >= 1:
        return "high"

    if tactical.get("ally_jungler_dead") or tactical.get("fight_state") == "disadvantage":
        return "low"

    return "medium"


def _dragon_hint(
    dragon: Dict[str, Any],
    tactical: Dict[str, Any],
    ally_dragons: int,
    enemy_dragons: int,
) -> str:
    """Return a contextual dragon hint."""
    if dragon.get("is_alive") and tactical.get("enemy_jungler_dead"):
        return "Dragon gratis: jungla rival muerto, asegura vision y entra ya."
    if dragon.get("is_alive") and tactical.get("fight_state") in {"advantage", "slight_advantage"}:
        return "Dragon disponible: empuja bot y mid, entra primero a rio."
    if dragon.get("seconds_until_spawn", 999) <= 75:
        return f"Dragon en {dragon['timer']}: prepara reset, wards y prioridad de bot/mid."
    if enemy_dragons > ally_dragons:
        return "Vais por detras en dragons: evita ceder vision gratis antes del siguiente spawn."
    return "Controla rio inferior y no cedas entrada sin prioridad de oleadas."


def _baron_hint(baron: Dict[str, Any], tactical: Dict[str, Any]) -> str:
    """Return a contextual baron hint."""
    if baron.get("is_alive") and tactical.get("enemy_jungler_dead"):
        return "Baron abierto con jungla rival muerto: limpia wards y fuerza decision."
    if baron.get("is_alive") and tactical.get("fight_state") in {"advantage", "slight_advantage"}:
        return "Baron disponible: empuja mid, gana vision superior y amenaza start o turn."
    if baron.get("seconds_until_spawn", 999) <= 90:
        return f"Baron en {baron['timer']}: deja mid empujado y prepara control de rio superior."
    return "Baron sera importante tras minuto 20: guarda tempo para reset y vision superior."


def _count_team_objectives(events: List[Dict[str, Any]], team: str) -> int:
    """Count objective takedowns completed by one team."""
    return sum(1 for event in events if event.get("killer_team") == team)


def _format_timer(seconds: int) -> str:
    """Format seconds as mm:ss."""
    minutes, remainder = divmod(max(seconds, 0), 60)
    return f"{minutes:02d}:{remainder:02d}"
