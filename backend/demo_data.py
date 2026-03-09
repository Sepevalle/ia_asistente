"""Static data used to validate the first assistant version without a live game."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict

DEMO_SNAPSHOT: Dict[str, Any] = {
    "gameData": {
        "gameMode": "CLASSIC",
        "gameTime": 755,
        "mapName": "Summoner's Rift",
        "mapNumber": 11,
    },
    "activePlayer": {
        "summonerName": "Josep",
        "currentGold": 1480,
        "level": 9,
        "championStats": {
            "currentHealth": 1115,
            "maxHealth": 1670,
            "resourceValue": 730,
            "resourceMax": 980,
        },
    },
    "allPlayers": [
        {
            "summonerName": "Josep",
            "championName": "Ahri",
            "team": "ORDER",
            "level": 9,
            "isDead": False,
            "respawnTimer": 0,
            "items": [
                {"itemID": 1056, "displayName": "Doran's Ring", "slot": 0},
                {"itemID": 3020, "displayName": "Sorcerer's Shoes", "slot": 1},
            ],
            "scores": {"kills": 3, "deaths": 1, "assists": 4, "creepScore": 81, "wardScore": 9},
        },
        {
            "summonerName": "Top Ally",
            "championName": "Gnar",
            "team": "ORDER",
            "level": 8,
            "isDead": False,
            "respawnTimer": 0,
            "items": [{"itemID": 1054, "displayName": "Doran's Shield", "slot": 0}],
            "scores": {"kills": 1, "deaths": 2, "assists": 2, "creepScore": 69, "wardScore": 5},
        },
        {
            "summonerName": "Jungle Ally",
            "championName": "JarvanIV",
            "team": "ORDER",
            "level": 8,
            "isDead": False,
            "respawnTimer": 0,
            "items": [{"itemID": 1039, "displayName": "Hailblade", "slot": 0}],
            "scores": {"kills": 2, "deaths": 2, "assists": 4, "creepScore": 57, "wardScore": 12},
        },
        {
            "summonerName": "ADC Ally",
            "championName": "Jinx",
            "team": "ORDER",
            "level": 8,
            "isDead": False,
            "respawnTimer": 0,
            "items": [{"itemID": 1036, "displayName": "Long Sword", "slot": 0}],
            "scores": {"kills": 2, "deaths": 1, "assists": 3, "creepScore": 88, "wardScore": 6},
        },
        {
            "summonerName": "Support Ally",
            "championName": "Nautilus",
            "team": "ORDER",
            "level": 7,
            "isDead": False,
            "respawnTimer": 0,
            "items": [{"itemID": 3860, "displayName": "Runic Compass", "slot": 0}],
            "scores": {"kills": 0, "deaths": 2, "assists": 7, "creepScore": 13, "wardScore": 19},
        },
        {
            "summonerName": "Enemy Top",
            "championName": "Aatrox",
            "team": "CHAOS",
            "level": 8,
            "isDead": False,
            "respawnTimer": 0,
            "items": [{"itemID": 1054, "displayName": "Doran's Shield", "slot": 0}],
            "scores": {"kills": 2, "deaths": 2, "assists": 1, "creepScore": 75, "wardScore": 4},
        },
        {
            "summonerName": "Enemy Jungle",
            "championName": "LeeSin",
            "team": "CHAOS",
            "level": 8,
            "isDead": False,
            "respawnTimer": 0,
            "items": [{"itemID": 1039, "displayName": "Mosstomper Seedling", "slot": 0}],
            "scores": {"kills": 1, "deaths": 2, "assists": 2, "creepScore": 54, "wardScore": 10},
        },
        {
            "summonerName": "Enemy Mid",
            "championName": "Syndra",
            "team": "CHAOS",
            "level": 9,
            "isDead": False,
            "respawnTimer": 0,
            "items": [{"itemID": 1056, "displayName": "Doran's Ring", "slot": 0}],
            "scores": {"kills": 2, "deaths": 2, "assists": 1, "creepScore": 84, "wardScore": 8},
        },
        {
            "summonerName": "Enemy ADC",
            "championName": "KaiSa",
            "team": "CHAOS",
            "level": 8,
            "isDead": False,
            "respawnTimer": 0,
            "items": [{"itemID": 1055, "displayName": "Doran's Blade", "slot": 0}],
            "scores": {"kills": 2, "deaths": 1, "assists": 1, "creepScore": 85, "wardScore": 5},
        },
        {
            "summonerName": "Enemy Support",
            "championName": "Soraka",
            "team": "CHAOS",
            "level": 7,
            "isDead": False,
            "respawnTimer": 0,
            "items": [{"itemID": 3860, "displayName": "Runic Compass", "slot": 0}],
            "scores": {"kills": 0, "deaths": 1, "assists": 5, "creepScore": 12, "wardScore": 17},
        },
    ],
    "events": {
        "Events": [
            {"EventName": "GameStart", "EventTime": 0},
            {"EventName": "DragonKill", "EventTime": 420, "KillerName": "Jungle Ally"},
            {"EventName": "ChampionKill", "EventTime": 700, "KillerName": "Josep", "VictimName": "Enemy Mid"},
        ]
    },
}


def get_demo_data() -> Dict[str, Any]:
    """Return a copy of the demo snapshot to avoid accidental mutation."""
    return deepcopy(DEMO_SNAPSHOT)
