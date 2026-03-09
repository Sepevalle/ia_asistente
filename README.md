# LoL AI Assistant

AI in-game assistant for League of Legends.

The goal of this project is to create a real-time AI overlay that helps players make better macro and item decisions during matches.

Features planned:

- Live game analysis
- Item recommendations
- Objective timers
- Enemy jungle tracking
- AI macro suggestions

Example suggestions:

- "Dragon spawning in 40s – rotate bot"
- "Enemy Soraka detected – build anti-heal"
- "Enemy jungler top – invade bot jungle"

## Architecture

League Client
↓
Live Client API (localhost:2999)
↓
Python backend
↓
AI decision engine
↓
Overlay UI

## Tech Stack

Backend
- Python
- Flask

Data
- Riot API
- Live Client Data API

Frontend
- Electron overlay

AI
- Rule engine + LLM recommendations