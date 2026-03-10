"""Static data used to validate the assistant without a live game."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict

DEMO_SNAPSHOT: Dict[str, Any] = {
    "gameData": {
        "gameMode": "CLASSIC",
        "gameTime": 1185,
        "mapName": "Summoner's Rift",
        "mapNumber": 11,
        "mapTerrain": "Chemtech",
    },
    "activePlayerName": "Josep",
    "activePlayer": {
        "summonerName": "Josep",
        "currentGold": 1825,
        "level": 11,
        "championStats": {
            "currentHealth": 1315,
            "maxHealth": 1760,
            "resourceValue": 640,
            "resourceMax": 1025,
            "abilityPower": 167,
            "armor": 61,
            "magicResist": 44,
            "attackDamage": 88,
            "moveSpeed": 380,
        },
    },
    "activePlayerAbilities": {
        "Q": {"displayName": "Orb of Deception", "abilityLevel": 5},
        "W": {"displayName": "Fox-Fire", "abilityLevel": 3},
        "E": {"displayName": "Charm", "abilityLevel": 2},
        "R": {"displayName": "Spirit Rush", "abilityLevel": 1},
    },
    "allPlayers": [
        {
            "summonerName": "Josep",
            "championName": "Ahri",
            "team": "ORDER",
            "level": 11,
            "isDead": False,
            "respawnTimer": 0,
            "items": [
                {"itemID": 1056, "displayName": "Doran's Ring", "slot": 0},
                {"itemID": 3020, "displayName": "Sorcerer's Shoes", "slot": 1},
                {"itemID": 6655, "displayName": "Luden's Companion", "slot": 2},
            ],
            "summonerSpells": {
                "summonerSpellOne": {"displayName": "Flash", "rawDisplayName": "GeneratedTip_SummonerSpell_SummonerFlash_DisplayName"},
                "summonerSpellTwo": {"displayName": "Ignite", "rawDisplayName": "GeneratedTip_SummonerSpell_SummonerDot_DisplayName"},
            },
            "scores": {"kills": 5, "deaths": 1, "assists": 6, "creepScore": 126, "wardScore": 14},
        },
        {
            "summonerName": "Top Ally",
            "championName": "Gnar",
            "team": "ORDER",
            "level": 10,
            "isDead": False,
            "respawnTimer": 0,
            "items": [
                {"itemID": 1054, "displayName": "Doran's Shield", "slot": 0},
                {"itemID": 3071, "displayName": "Black Cleaver", "slot": 1},
            ],
            "summonerSpells": {
                "summonerSpellOne": {"displayName": "Flash", "rawDisplayName": "GeneratedTip_SummonerSpell_SummonerFlash_DisplayName"},
                "summonerSpellTwo": {"displayName": "Teleport", "rawDisplayName": "GeneratedTip_SummonerSpell_SummonerTeleport_DisplayName"},
            },
            "scores": {"kills": 2, "deaths": 2, "assists": 3, "creepScore": 118, "wardScore": 9},
        },
        {
            "summonerName": "Jungle Ally",
            "championName": "JarvanIV",
            "team": "ORDER",
            "level": 10,
            "isDead": False,
            "respawnTimer": 0,
            "items": [
                {"itemID": 1101, "displayName": "Scorchclaw Pup", "slot": 0},
                {"itemID": 6630, "displayName": "Goredrinker", "slot": 1},
            ],
            "summonerSpells": {
                "summonerSpellOne": {"displayName": "Flash", "rawDisplayName": "GeneratedTip_SummonerSpell_SummonerFlash_DisplayName"},
                "summonerSpellTwo": {"displayName": "Smite", "rawDisplayName": "GeneratedTip_SummonerSpell_SummonerSmite_DisplayName"},
            },
            "scores": {"kills": 3, "deaths": 2, "assists": 7, "creepScore": 91, "wardScore": 21},
        },
        {
            "summonerName": "ADC Ally",
            "championName": "Jinx",
            "team": "ORDER",
            "level": 10,
            "isDead": False,
            "respawnTimer": 0,
            "items": [
                {"itemID": 1055, "displayName": "Doran's Blade", "slot": 0},
                {"itemID": 3006, "displayName": "Berserker's Greaves", "slot": 1},
                {"itemID": 3031, "displayName": "Infinity Edge", "slot": 2},
            ],
            "summonerSpells": {
                "summonerSpellOne": {"displayName": "Flash", "rawDisplayName": "GeneratedTip_SummonerSpell_SummonerFlash_DisplayName"},
                "summonerSpellTwo": {"displayName": "Heal", "rawDisplayName": "GeneratedTip_SummonerSpell_SummonerHeal_DisplayName"},
            },
            "scores": {"kills": 4, "deaths": 2, "assists": 5, "creepScore": 148, "wardScore": 8},
        },
        {
            "summonerName": "Support Ally",
            "championName": "Nautilus",
            "team": "ORDER",
            "level": 9,
            "isDead": False,
            "respawnTimer": 0,
            "items": [
                {"itemID": 3860, "displayName": "Runic Compass", "slot": 0},
                {"itemID": 3190, "displayName": "Locket of the Iron Solari", "slot": 1},
            ],
            "summonerSpells": {
                "summonerSpellOne": {"displayName": "Flash", "rawDisplayName": "GeneratedTip_SummonerSpell_SummonerFlash_DisplayName"},
                "summonerSpellTwo": {"displayName": "Exhaust", "rawDisplayName": "GeneratedTip_SummonerSpell_SummonerExhaust_DisplayName"},
            },
            "scores": {"kills": 1, "deaths": 2, "assists": 11, "creepScore": 22, "wardScore": 31},
        },
        {
            "summonerName": "Enemy Top",
            "championName": "Aatrox",
            "team": "CHAOS",
            "level": 10,
            "isDead": False,
            "respawnTimer": 0,
            "items": [
                {"itemID": 1054, "displayName": "Doran's Shield", "slot": 0},
                {"itemID": 6631, "displayName": "Stridebreaker", "slot": 1},
            ],
            "summonerSpells": {
                "summonerSpellOne": {"displayName": "Flash", "rawDisplayName": "GeneratedTip_SummonerSpell_SummonerFlash_DisplayName"},
                "summonerSpellTwo": {"displayName": "Teleport", "rawDisplayName": "GeneratedTip_SummonerSpell_SummonerTeleport_DisplayName"},
            },
            "scores": {"kills": 2, "deaths": 4, "assists": 2, "creepScore": 119, "wardScore": 8},
        },
        {
            "summonerName": "Enemy Jungle",
            "championName": "LeeSin",
            "team": "CHAOS",
            "level": 9,
            "isDead": True,
            "respawnTimer": 18,
            "items": [
                {"itemID": 1102, "displayName": "Gustwalker Hatchling", "slot": 0},
                {"itemID": 6692, "displayName": "Eclipse", "slot": 1},
            ],
            "summonerSpells": {
                "summonerSpellOne": {"displayName": "Flash", "rawDisplayName": "GeneratedTip_SummonerSpell_SummonerFlash_DisplayName"},
                "summonerSpellTwo": {"displayName": "Smite", "rawDisplayName": "GeneratedTip_SummonerSpell_SummonerSmite_DisplayName"},
            },
            "scores": {"kills": 2, "deaths": 5, "assists": 3, "creepScore": 83, "wardScore": 16},
        },
        {
            "summonerName": "Enemy Mid",
            "championName": "Syndra",
            "team": "CHAOS",
            "level": 10,
            "isDead": False,
            "respawnTimer": 0,
            "items": [
                {"itemID": 1056, "displayName": "Doran's Ring", "slot": 0},
                {"itemID": 6653, "displayName": "Liandry's Torment", "slot": 1},
            ],
            "summonerSpells": {
                "summonerSpellOne": {"displayName": "Flash", "rawDisplayName": "GeneratedTip_SummonerSpell_SummonerFlash_DisplayName"},
                "summonerSpellTwo": {"displayName": "Teleport", "rawDisplayName": "GeneratedTip_SummonerSpell_SummonerTeleport_DisplayName"},
            },
            "scores": {"kills": 3, "deaths": 4, "assists": 2, "creepScore": 128, "wardScore": 10},
        },
        {
            "summonerName": "Enemy ADC",
            "championName": "KaiSa",
            "team": "CHAOS",
            "level": 10,
            "isDead": False,
            "respawnTimer": 0,
            "items": [
                {"itemID": 1055, "displayName": "Doran's Blade", "slot": 0},
                {"itemID": 3006, "displayName": "Berserker's Greaves", "slot": 1},
                {"itemID": 6672, "displayName": "Kraken Slayer", "slot": 2},
            ],
            "summonerSpells": {
                "summonerSpellOne": {"displayName": "Flash", "rawDisplayName": "GeneratedTip_SummonerSpell_SummonerFlash_DisplayName"},
                "summonerSpellTwo": {"displayName": "Heal", "rawDisplayName": "GeneratedTip_SummonerSpell_SummonerHeal_DisplayName"},
            },
            "scores": {"kills": 4, "deaths": 2, "assists": 2, "creepScore": 141, "wardScore": 7},
        },
        {
            "summonerName": "Enemy Support",
            "championName": "Soraka",
            "team": "CHAOS",
            "level": 9,
            "isDead": False,
            "respawnTimer": 0,
            "items": [
                {"itemID": 3860, "displayName": "Runic Compass", "slot": 0},
                {"itemID": 6617, "displayName": "Moonstone Renewer", "slot": 1},
            ],
            "summonerSpells": {
                "summonerSpellOne": {"displayName": "Flash", "rawDisplayName": "GeneratedTip_SummonerSpell_SummonerFlash_DisplayName"},
                "summonerSpellTwo": {"displayName": "Exhaust", "rawDisplayName": "GeneratedTip_SummonerSpell_SummonerExhaust_DisplayName"},
            },
            "scores": {"kills": 0, "deaths": 3, "assists": 8, "creepScore": 19, "wardScore": 28},
        },
    ],
    "events": {
        "Events": [
            {"EventName": "GameStart", "EventTime": 0},
            {"EventName": "FirstBlood", "EventTime": 145, "KillerName": "Enemy Jungle", "VictimName": "Top Ally"},
            {"EventName": "DragonKill", "EventTime": 610, "KillerName": "Jungle Ally", "DragonType": "Chemtech"},
            {"EventName": "TurretKilled", "EventTime": 940, "KillerName": "ADC Ally", "TurretKilled": "Turret_T2_C_05_A"},
            {
                "EventName": "ChampionKill",
                "EventTime": 1166,
                "KillerName": "Josep",
                "VictimName": "Enemy Jungle",
                "Position": {"x": 6100, "y": 8700},
            },
            {
                "EventName": "ChampionKill",
                "EventTime": 1171,
                "KillerName": "Jungle Ally",
                "VictimName": "Enemy Top",
                "Position": {"x": 5400, "y": 9100},
            },
        ]
    },
}


def get_demo_data() -> Dict[str, Any]:
    """Return a copy of the demo snapshot to avoid accidental mutation."""
    return deepcopy(DEMO_SNAPSHOT)
