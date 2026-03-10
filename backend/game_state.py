"""Normalization helpers for raw Live Client API payloads."""

from __future__ import annotations

from typing import Any, Dict, List

from recommendations import (
    find_team_jungler,
    has_jungle_item,
    has_smite,
    has_support_item,
    infer_player_role,
    spell_names,
)


def build_game_state(raw_data: Dict[str, Any], error: str | None = None) -> Dict[str, Any]:
    """Transform raw live data into the project's internal GameState shape."""
    if not raw_data:
        return _empty_state(error)

    game_data = raw_data.get("gameData") or {}
    active_player = raw_data.get("activePlayer") or {}
    active_player_abilities = raw_data.get("activePlayerAbilities") or {}
    raw_players = raw_data.get("allPlayers") or []
    players = [_normalize_player(player) for player in raw_players if isinstance(player, dict)]

    if not players:
        return _empty_state(error or "No active players were returned by the Live Client API.")

    for normalized_player in players:
        normalized_player["role"] = infer_player_role(normalized_player)

    active_player_name = (
        raw_data.get("activePlayerName")
        or active_player.get("summonerName")
        or players[0]["summoner_name"]
    )

    player = _find_player(players, active_player_name) or players[0]
    player = _enrich_active_player(player, active_player, active_player_abilities)

    ally_roster = [teammate for teammate in players if teammate["team"] == player["team"]]
    enemy_roster = [opponent for opponent in players if opponent["team"] != player["team"]]
    allies = [teammate for teammate in ally_roster if teammate["summoner_name"] != player["summoner_name"]]

    game_time_seconds = int(float(game_data.get("gameTime") or 0))
    map_number = int(game_data.get("mapNumber") or 0)

    ally_totals = _team_totals(ally_roster)
    enemy_totals = _team_totals(enemy_roster)

    if ally_totals["kills"] > 0:
        player["kill_participation"] = round(
            (player["kills"] + player["assists"]) / ally_totals["kills"], 2
        )
    else:
        player["kill_participation"] = 0.0

    player_lookup = _build_player_lookup(players)
    events = _normalize_events(raw_data.get("events", {}).get("Events", []), player_lookup)

    team_context = _build_team_context(player, ally_roster, enemy_roster)
    event_summary = _summarize_events(events, game_time_seconds, player["team"])
    tactical = _build_tactical_state(player, ally_totals, enemy_totals, team_context, event_summary)

    return {
        "status": "in_game",
        "connection_error": error,
        "map": {
            "name": game_data.get("mapName", "Unknown map"),
            "mode": game_data.get("gameMode", "Unknown mode"),
            "number": map_number,
            "terrain": game_data.get("mapTerrain", ""),
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
            "cs_diff": ally_totals["cs"] - enemy_totals["cs"],
            "avg_level_diff": round(ally_totals["avg_level"] - enemy_totals["avg_level"], 2),
            "alive_diff": ally_totals["alive_count"] - enemy_totals["alive_count"],
            "ward_score_diff": ally_totals["ward_score"] - enemy_totals["ward_score"],
            "item_diff": ally_totals["item_count"] - enemy_totals["item_count"],
        },
        "events": events,
        "event_summary": event_summary,
        "team_context": team_context,
        "tactical": tactical,
    }


def _normalize_player(raw_player: Dict[str, Any]) -> Dict[str, Any]:
    """Convert a raw player payload into a compact internal representation."""
    scores = raw_player.get("scores") or {}
    raw_items = raw_player.get("items") or []
    items = [_normalize_item(item) for item in raw_items if isinstance(item, dict)]
    raw_spells = raw_player.get("summonerSpells") or {}
    raw_position = raw_player.get("position")
    map_position = _normalize_position(raw_position)

    return {
        "summoner_name": raw_player.get("summonerName")
        or raw_player.get("riotIdGameName")
        or "Unknown",
        "riot_id_game_name": raw_player.get("riotIdGameName") or "",
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
        "position": raw_position or "",
        "map_position": map_position,
        "items": items,
        "item_count": len(items),
        "boots_owned": any(_is_boots_item(item["name"]) for item in items),
        "summoner_spells": spell_names(raw_spells),
        "has_smite": has_smite(raw_spells),
        "support_item_owned": has_support_item(items),
        "jungle_item_owned": has_jungle_item(items),
    }


def _normalize_item(raw_item: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize a single item payload."""
    return {
        "id": int(raw_item.get("itemID") or 0),
        "name": raw_item.get("displayName", "Unknown item"),
        "slot": int(raw_item.get("slot") or 0),
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


def _enrich_active_player(
    player: Dict[str, Any],
    active_player: Dict[str, Any],
    raw_abilities: Dict[str, Any],
) -> Dict[str, Any]:
    """Attach active-player-only fields such as gold, health, stats, and abilities."""
    champion_stats = active_player.get("championStats") or {}
    enriched_player = dict(player)
    health_current = int(float(champion_stats.get("currentHealth") or 0))
    health_max = int(float(champion_stats.get("maxHealth") or 0))
    resource_current = int(float(champion_stats.get("resourceValue") or 0))
    resource_max = int(float(champion_stats.get("resourceMax") or 0))

    enriched_player["current_gold"] = int(active_player.get("currentGold") or 0)
    enriched_player["health"] = {
        "current": health_current,
        "max": health_max,
        "ratio": round(health_current / health_max, 2) if health_max else 0.0,
    }
    enriched_player["resource"] = {
        "current": resource_current,
        "max": resource_max,
        "ratio": round(resource_current / resource_max, 2) if resource_max else 0.0,
    }
    enriched_player["combat_stats"] = {
        "ability_power": int(float(champion_stats.get("abilityPower") or 0)),
        "attack_damage": int(float(champion_stats.get("attackDamage") or 0)),
        "armor": int(float(champion_stats.get("armor") or 0)),
        "magic_resist": int(float(champion_stats.get("magicResist") or 0)),
        "move_speed": int(float(champion_stats.get("moveSpeed") or 0)),
    }
    enriched_player["abilities"] = _normalize_abilities(raw_abilities)
    enriched_player["ultimate_rank"] = enriched_player["abilities"]["R"]["level"]
    enriched_player["ultimate_unlocked"] = enriched_player["ultimate_rank"] > 0
    return enriched_player


def _normalize_abilities(raw_abilities: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """Normalize active-player basic abilities and ultimate."""
    abilities = {}

    for slot in ("Q", "W", "E", "R"):
        raw_spell = raw_abilities.get(slot) or {}
        abilities[slot] = {
            "name": raw_spell.get("displayName", slot),
            "level": int(raw_spell.get("abilityLevel") or 0),
        }

    return abilities


def _find_player(players: List[Dict[str, Any]], summoner_name: str) -> Dict[str, Any] | None:
    """Locate the active player inside the normalized roster."""
    target_key = _normalize_name(summoner_name)
    for player in players:
        if player["summoner_name"] == summoner_name:
            return player
        if _normalize_name(player.get("summoner_name", "")) == target_key:
            return player
    return None


def _team_totals(players: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Aggregate team combat, farm, level, and inventory totals."""
    player_count = max(len(players), 1)
    alive_count = sum(1 for player in players if player["is_alive"])

    return {
        "kills": sum(player["kills"] for player in players),
        "deaths": sum(player["deaths"] for player in players),
        "assists": sum(player["assists"] for player in players),
        "cs": sum(player["cs"] for player in players),
        "ward_score": sum(player["ward_score"] for player in players),
        "item_count": sum(player["item_count"] for player in players),
        "avg_level": round(sum(player["level"] for player in players) / player_count, 2),
        "alive_count": alive_count,
        "dead_count": len(players) - alive_count,
    }


def _normalize_events(
    raw_events: List[Dict[str, Any]],
    player_lookup: Dict[str, Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Keep event fields that are useful for live coaching decisions."""
    normalized_events = []

    for event in raw_events:
        if not isinstance(event, dict):
            continue

        killer_name = event.get("KillerName", "")
        victim_name = event.get("VictimName", "")
        killer_team = _lookup_team(player_lookup, killer_name)
        victim_team = _lookup_team(player_lookup, victim_name)
        position = _normalize_position(
            event.get("Position")
            or event.get("position")
            or event.get("KillerPosition")
            or event.get("VictimPosition")
        )
        normalized_events.append(
            {
                "event_name": event.get("EventName", ""),
                "event_time": int(float(event.get("EventTime") or 0)),
                "killer_name": killer_name,
                "killer_team": killer_team,
                "victim_name": victim_name,
                "victim_team": victim_team,
                "dragon_type": event.get("DragonType", ""),
                "target_name": event.get("TurretKilled") or event.get("InhibKilled") or "",
                "position": position,
            }
        )

    return normalized_events


def _build_team_context(
    player: Dict[str, Any],
    ally_roster: List[Dict[str, Any]],
    enemy_roster: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """Resolve key team-context actors that affect macro decisions."""
    ally_jungler = find_team_jungler(ally_roster)
    enemy_jungler = find_team_jungler(enemy_roster)

    return {
        "player_role": player.get("role", "laner"),
        "ally_jungler": _player_glance(ally_jungler),
        "enemy_jungler": _player_glance(enemy_jungler),
    }


def _player_glance(player: Dict[str, Any] | None) -> Dict[str, Any] | None:
    """Trim a player payload down to fields useful for tactical summaries."""
    if not player:
        return None

    return {
        "summoner_name": player["summoner_name"],
        "champion_name": player["champion_name"],
        "is_alive": player["is_alive"],
        "respawn_timer": player["respawn_timer"],
        "level": player["level"],
        "cs": player["cs"],
    }


def _summarize_events(
    events: List[Dict[str, Any]],
    game_time_seconds: int,
    ally_team: str,
) -> Dict[str, Any]:
    """Extract recent momentum and pick windows from the event stream."""
    enemy_team = "CHAOS" if ally_team == "ORDER" else "ORDER"

    ally_kills_60 = _count_recent(events, game_time_seconds, 60, "ChampionKill", ally_team)
    enemy_kills_60 = _count_recent(events, game_time_seconds, 60, "ChampionKill", enemy_team)
    ally_towers_180 = _count_recent(events, game_time_seconds, 180, "TurretKilled", ally_team)
    enemy_towers_180 = _count_recent(events, game_time_seconds, 180, "TurretKilled", enemy_team)
    ally_objectives_180 = _count_recent_objectives(events, game_time_seconds, 180, ally_team)
    enemy_objectives_180 = _count_recent_objectives(events, game_time_seconds, 180, enemy_team)

    recent_pick = _resolve_recent_pick(events, game_time_seconds, ally_team, enemy_team)
    momentum_score = (
        (ally_kills_60 - enemy_kills_60)
        + 2 * (ally_towers_180 - enemy_towers_180)
        + 2 * (ally_objectives_180 - enemy_objectives_180)
    )

    if momentum_score >= 2:
        momentum = "allies"
    elif momentum_score <= -2:
        momentum = "enemies"
    else:
        momentum = "neutral"

    last_event = max(events, key=lambda item: item["event_time"]) if events else None

    return {
        "ally_kills_last_60": ally_kills_60,
        "enemy_kills_last_60": enemy_kills_60,
        "ally_towers_last_180": ally_towers_180,
        "enemy_towers_last_180": enemy_towers_180,
        "ally_objectives_last_180": ally_objectives_180,
        "enemy_objectives_last_180": enemy_objectives_180,
        "recent_pick": recent_pick,
        "momentum": momentum,
        "momentum_score": momentum_score,
        "last_event": {
            "event_name": last_event["event_name"],
            "event_time": last_event["event_time"],
            "killer_name": last_event["killer_name"],
            "victim_name": last_event["victim_name"],
        }
        if last_event
        else None,
    }


def _build_tactical_state(
    player: Dict[str, Any],
    ally_totals: Dict[str, Any],
    enemy_totals: Dict[str, Any],
    team_context: Dict[str, Any],
    event_summary: Dict[str, Any],
) -> Dict[str, Any]:
    """Create high-level tactical flags consumed by the coaching engine."""
    alive_diff = ally_totals["alive_count"] - enemy_totals["alive_count"]
    level_diff = round(ally_totals["avg_level"] - enemy_totals["avg_level"], 2)
    health_ratio = player.get("health", {}).get("ratio", 0.0)

    if alive_diff >= 1 or event_summary["recent_pick"]["team"] == "allies":
        fight_state = "advantage"
    elif alive_diff <= -1 or event_summary["recent_pick"]["team"] == "enemies":
        fight_state = "disadvantage"
    elif health_ratio <= 0.4:
        fight_state = "unstable"
    elif level_diff >= 1:
        fight_state = "slight_advantage"
    elif level_diff <= -1:
        fight_state = "slight_disadvantage"
    else:
        fight_state = "even"

    enemy_jungler = team_context.get("enemy_jungler") or {}
    ally_jungler = team_context.get("ally_jungler") or {}

    return {
        "fight_state": fight_state,
        "player_low_health": health_ratio <= 0.4,
        "player_high_gold": player.get("current_gold", 0) >= 1300,
        "alive_diff": alive_diff,
        "level_diff": level_diff,
        "enemy_jungler_dead": bool(enemy_jungler) and not enemy_jungler.get("is_alive", True),
        "ally_jungler_dead": bool(ally_jungler) and not ally_jungler.get("is_alive", True),
    }


def _count_recent(
    events: List[Dict[str, Any]],
    game_time_seconds: int,
    window_seconds: int,
    event_name: str,
    team: str,
) -> int:
    """Count recent events for a team within the provided time window."""
    return sum(
        1
        for event in events
        if event["event_name"] == event_name
        and event["killer_team"] == team
        and game_time_seconds - event["event_time"] <= window_seconds
    )


def _count_recent_objectives(
    events: List[Dict[str, Any]],
    game_time_seconds: int,
    window_seconds: int,
    team: str,
) -> int:
    """Count recent dragon and baron takedowns for a team."""
    return sum(
        1
        for event in events
        if event["event_name"] in {"DragonKill", "BaronKill"}
        and event["killer_team"] == team
        and game_time_seconds - event["event_time"] <= window_seconds
    )


def _resolve_recent_pick(
    events: List[Dict[str, Any]],
    game_time_seconds: int,
    ally_team: str,
    enemy_team: str,
) -> Dict[str, Any]:
    """Resolve whether a recent champion kill created a numbers window."""
    recent_kills = [
        event
        for event in events
        if event["event_name"] == "ChampionKill" and game_time_seconds - event["event_time"] <= 30
    ]

    if not recent_kills:
        return {"team": "none", "age_seconds": None, "victim_name": "", "killer_name": ""}

    latest_kill = max(recent_kills, key=lambda item: item["event_time"])
    killer_team = latest_kill["killer_team"]

    if killer_team == ally_team:
        team = "allies"
    elif killer_team == enemy_team:
        team = "enemies"
    else:
        team = "none"

    return {
        "team": team,
        "age_seconds": game_time_seconds - latest_kill["event_time"],
        "victim_name": latest_kill["victim_name"],
        "killer_name": latest_kill["killer_name"],
    }


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


def _is_boots_item(item_name: str) -> bool:
    """Heuristic used to spot movement boots from the inventory."""
    lower_name = item_name.lower()
    return "boots" in lower_name or "greaves" in lower_name or "treads" in lower_name


def _empty_state(error: str | None) -> Dict[str, Any]:
    """Return the API shape used when no match is active."""
    return {
        "status": "not_in_game",
        "connection_error": error or "Live Client API no disponible.",
        "map": {"name": "Unknown map", "mode": "Unknown mode", "number": 0, "terrain": ""},
        "map_number": 0,
        "game_time": "00:00",
        "game_time_seconds": 0,
        "phase": "waiting",
        "player": {},
        "allies": [],
        "enemies": [],
        "team_stats": {
            "allies": {
                "kills": 0,
                "deaths": 0,
                "assists": 0,
                "cs": 0,
                "ward_score": 0,
                "item_count": 0,
                "avg_level": 0.0,
                "alive_count": 0,
                "dead_count": 0,
            },
            "enemies": {
                "kills": 0,
                "deaths": 0,
                "assists": 0,
                "cs": 0,
                "ward_score": 0,
                "item_count": 0,
                "avg_level": 0.0,
                "alive_count": 0,
                "dead_count": 0,
            },
            "kill_diff": 0,
            "cs_diff": 0,
            "avg_level_diff": 0.0,
            "alive_diff": 0,
            "ward_score_diff": 0,
            "item_diff": 0,
        },
        "events": [],
        "event_summary": {
            "ally_kills_last_60": 0,
            "enemy_kills_last_60": 0,
            "ally_towers_last_180": 0,
            "enemy_towers_last_180": 0,
            "ally_objectives_last_180": 0,
            "enemy_objectives_last_180": 0,
            "recent_pick": {"team": "none", "age_seconds": None, "victim_name": "", "killer_name": ""},
            "momentum": "neutral",
            "momentum_score": 0,
            "last_event": None,
        },
        "team_context": {
            "player_role": "laner",
            "ally_jungler": None,
            "enemy_jungler": None,
        },
        "tactical": {
            "fight_state": "even",
            "player_low_health": False,
            "player_high_gold": False,
            "alive_diff": 0,
            "level_diff": 0.0,
            "enemy_jungler_dead": False,
            "ally_jungler_dead": False,
        },
    }


def _normalize_name(name: str) -> str:
    """Normalize summoner/riot names for event lookups."""
    if not name:
        return ""
    base = name.split("#", 1)[0].strip()
    return base.lower()


def _build_player_lookup(players: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """Build a lookup table keyed by multiple player name variants."""
    lookup: Dict[str, Dict[str, Any]] = {}
    for player in players:
        for key in _player_name_keys(player):
            if key:
                lookup[key] = player
    return lookup


def _player_name_keys(player: Dict[str, Any]) -> List[str]:
    """Generate name variants for lookup matching."""
    keys = []
    summoner_name = player.get("summoner_name", "")
    riot_id = player.get("riot_id_game_name", "")
    for candidate in (summoner_name, riot_id):
        if candidate:
            keys.append(candidate)
            keys.append(_normalize_name(candidate))
    return keys


def _lookup_team(player_lookup: Dict[str, Dict[str, Any]], name: str) -> str:
    """Resolve a team name from a lookup table using normalized keys."""
    if not name:
        return ""
    player = player_lookup.get(name)
    if player:
        return player.get("team", "")
    player = player_lookup.get(_normalize_name(name))
    if player:
        return player.get("team", "")
    return ""
