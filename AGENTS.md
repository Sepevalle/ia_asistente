# AGENTS.md

This repository builds an AI assistant for League of Legends.

## Tech stack

Backend:
- Python
- Flask

Frontend:
- Electron overlay

## Data sources

1. Riot API
2. Live Client Data API
https://127.0.0.1:2999/liveclientdata/allgamedata

## Code guidelines

- Keep modules small
- Separate logic from API calls
- Prefer async where possible
- Add docstrings to functions

## Goals

Codex should help implement:

1. Live game data ingestion
2. AI recommendation engine
3. Overlay communication
4. Match analysis

## Backend commands

Install dependencies

pip install -r requirements.txt

Run backend

python backend/app.py