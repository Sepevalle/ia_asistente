# ARCHITECTURE.md

# LoL AI Assistant – System Architecture

This document describes the architecture of the **LoL AI Assistant** project.

The goal is to build a modular system capable of analyzing a live League of Legends match and providing real-time strategic suggestions.

The architecture must be scalable to support future AI features and advanced coaching systems.

---

# High-Level Architecture

The system is composed of three main layers:

1. Data Layer
2. Analysis Layer
3. Presentation Layer

Flow:

League of Legends Client
↓
Live Client API
↓
Backend Data Processing
↓
AI Decision Engine
↓
Overlay UI

---

# System Components

## 1 Data Layer

Responsible for collecting game data.

Sources:

Live Client API
Riot API

---

### Live Client API

Local endpoint exposed by the League of Legends client.

URL:

https://127.0.0.1:2999/liveclientdata/allgamedata

Provides real-time information such as:

* game time
* champion stats
* items
* gold
* abilities
* team data

Module:

backend/live_client.py

Responsibilities:

* fetch data
* handle connection errors
* return normalized JSON

---

### Riot API

Used for external data.

Examples:

* champion stats
* player match history
* ranking data

Module:

backend/riot_api.py

---

# 2 Game State Layer

Transforms raw API data into a structured object.

Module:

backend/game_state.py

Purpose:

Create a unified representation of the match state.

GameState structure:

GameState

* game_time
* player_info
* allied_team
* enemy_team
* map_state
* objectives
* items
* gold

Benefits:

* simplifies analysis logic
* isolates API complexity
* enables easier testing

---

# 3 Objective System

Responsible for tracking map objectives.

Module:

backend/objectives.py

Objectives tracked:

Dragon
Rift Herald
Baron Nashor

Responsibilities:

* calculate spawn timers
* track availability
* notify upcoming objectives

Example output:

Dragon spawning in 45 seconds.

---

# 4 AI Coaching Engine

The core intelligence of the system.

Module:

backend/ai_coach.py

Input:

GameState

Output:

Strategic suggestions.

Example output:

Prepare vision around dragon.

Push bot wave.

Avoid teamfight.

---

# Decision Engine Structure

The AI engine will evolve over time.

Initial versions:

Rule-based logic.

Future versions:

Hybrid system:

Rules + Machine Learning + LLM analysis.

---

# Coaching Categories

The AI generates suggestions in multiple categories.

Early Game

* jungle tracking
* wave management
* lane pressure

Mid Game

* rotations
* objective preparation
* map pressure

Late Game

* Baron control
* split push strategy
* teamfight evaluation

---

# 5 API Layer

Provides access to suggestions for the overlay.

Module:

backend/app.py

Framework:

Flask

Endpoint:

/game

Response example:

{
"game_time": 532,
"suggestions": [
"Dragon spawning soon",
"Prepare vision around dragon"
]
}

---

# 6 Overlay UI

Displays coaching suggestions during the match.

Location:

overlay/

Technology:

Electron

Features:

* transparent overlay
* small window
* real-time suggestions

Displayed elements:

* objective timers
* coaching messages
* warnings

---

# Data Flow

Step-by-step process:

1 Live Client API provides game data.

2 Backend fetches raw data.

3 GameState parser structures data.

4 Objective system computes timers.

5 AI engine analyzes match state.

6 Suggestions generated.

7 Flask API returns suggestions.

8 Overlay UI displays suggestions.

---

# Example Runtime Flow

1 Player starts match.

2 Backend begins polling Live Client API.

3 Game state updates every second.

4 AI engine analyzes match state.

5 Suggestions updated in real time.

Example:

Dragon spawning in 60 seconds.

Push bot wave.

Place vision.

---

# Future Architecture Expansion

Future versions may include:

Machine Learning modules.

New components:

backend/models/
backend/prediction/
backend/analytics/

Examples:

* jungle path prediction
* win probability estimation
* fight outcome prediction

---

# Performance Considerations

The assistant must run with minimal impact on the game.

Strategies:

* lightweight polling
* efficient JSON parsing
* caching champion data

Target performance:

Update cycle every 1 second.

---

# Security Considerations

The system should:

* avoid interfering with game processes
* only read data from official APIs
* follow Riot developer guidelines

---

# Scalability

Future improvements may include:

* cloud-based analysis
* match history analytics
* player improvement tracking

---

# Summary

The LoL AI Assistant architecture focuses on:

Modularity
Scalability
Real-time analysis

The system will evolve from a simple rule-based assistant into a **full strategic coaching AI** capable of analyzing matches at a high level and guiding player decisions during gameplay.
