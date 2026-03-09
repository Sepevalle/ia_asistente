# Project Specification

## Goal

Build an AI-powered assistant for League of Legends that gives real-time advice during a match.

## Data Sources

Riot API:
- Match history
- Player rank
- Champion statistics

Live Client API:
- Champion stats
- Items
- Gold
- Game time

Endpoint:

https://127.0.0.1:2999/liveclientdata/allgamedata

## AI Features

### Item Recommendation

Input:
- Enemy champions
- Current items
- Game state

Output:
Recommended next item.

Example:

Enemy team:
- Aatrox
- Soraka

Suggestion:
Buy Executioner's Calling.

---

### Objective Tracking

Track:

- Dragon
- Baron
- Herald

Notify:

Dragon in 40 seconds.

---

### Macro Suggestions

Examples:

- Rotate bot
- Invade jungle
- Push mid