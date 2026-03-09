# GAMESTATE_SCHEMA.md

# GameState Data Model

This document defines the internal data structure used by the LoL AI Assistant.

The goal is to transform raw Live Client API data into a normalized structure used by the AI decision engine.

Source of raw data:

Live Client API

https://127.0.0.1:2999/liveclientdata/allgamedata

---

# Root Object

GameState

Fields:

game_time
player
allies
enemies
objectives
events
map_state

---

# Player Object

Represents the active player.

Fields:

summoner_name
champion_name
level
current_gold
items
position
health
mana
kills
deaths
assists

Example:

player:

summoner_name: "Player1"

champion_name: "Ahri"

level: 8

current_gold: 1450

kills: 3

deaths: 1

assists: 2

---

# Team Player Object

Used for both allies and enemies.

Fields:

summoner_name
champion_name
level
items
kills
deaths
assists
is_alive
position

Example:

enemy_player:

champion_name: "LeeSin"

level: 7

kills: 2

deaths: 1

assists: 1

---

# Items Object

Represents purchased items.

Fields:

item_id
item_name
price
stats

Example:

items:

* item_name: "Infinity Edge"
* item_name: "Berserker Greaves"

---

# Objective State

Tracks major map objectives.

Fields:

dragon_timer
herald_timer
baron_timer

dragon_alive
herald_alive
baron_alive

Example:

objectives:

dragon_timer: 120

herald_timer: 0

baron_timer: 600

---

# Events

List of important in-game events.

Possible events:

ChampionKill
TurretKilled
DragonKilled
BaronKilled

Example:

events:

* type: ChampionKill
  killer: "Player1"
  victim: "EnemyMid"

---

# Map State

High level map information.

Fields:

ally_towers
enemy_towers
vision_control
lane_pressure

Example:

map_state:

ally_towers: 7

enemy_towers: 5

vision_control: "neutral"

lane_pressure: "bot"

---

# AI Engine Input

The AI coaching engine receives a GameState object.

Example:

analyze_game(game_state)

Output:

{
"suggestions": [
"Dragon spawning soon",
"Push bot wave",
"Place vision"
]
}

---

# Future Extensions

Future GameState fields may include:

jungle_camps
vision_wards
summoner_spells
cooldowns
gold_difference

This structure will evolve as the AI coaching system becomes more advanced.
