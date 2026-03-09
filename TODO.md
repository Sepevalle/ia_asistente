# TODO.md

# LoL AI Assistant – Development Roadmap

Goal:
Build a professional in-game AI coach that provides real-time macro and micro decision support for League of Legends players.

The final system should behave like a **Challenger-level strategic assistant** that analyzes the match state and suggests optimal actions.

---

# Phase 1 — Core Infrastructure

## Backend foundation

* [ ] Setup Flask API structure
* [ ] Implement error handling and logging
* [ ] Create modular architecture

Modules:

backend/

* live_client.py
* riot_api.py
* game_state.py
* ai_engine.py
* objectives.py
* recommendations.py

---

## Live Client Data Integration

Use Live Client API endpoint:

https://127.0.0.1:2999/liveclientdata/allgamedata

Tasks:

* [ ] Fetch live data safely

* [ ] Implement polling loop (1s interval)

* [ ] Parse:

  * game time
  * champions
  * items
  * gold
  * health
  * cooldowns

* [ ] Normalize game data structure

* [ ] Create internal `GameState` object

Example:

GameState:

* game_time
* ally_team
* enemy_team
* player_stats
* map_state

---

# Phase 2 — Game Awareness Systems

## Objective Tracking

Track spawn timers for:

* [ ] Dragon
* [ ] Rift Herald
* [ ] Baron Nashor
* [ ] Buff camps

Features:

* [ ] spawn timer predictions
* [ ] respawn tracking
* [ ] objective alerts

Example alerts:

"Dragon spawning in 45s"
"Baron available"

---

## Gold and Item Tracking

* [ ] Track player gold
* [ ] Detect shop visits
* [ ] Predict next item purchase

Suggestions:

* Buy anti-heal
* Buy armor
* Buy magic resist

---

## Champion Composition Analysis

Using Riot champion data.

Features:

* [ ] Detect enemy composition type

Types:

* poke
* sustain
* dive
* scaling
* splitpush

Example output:

Enemy comp: Heavy sustain

Recommendation:
Build anti-heal early.

---

# Phase 3 — Jungle Intelligence

One of the most valuable coaching features.

## Enemy Jungle Tracking

* [ ] Identify enemy jungler
* [ ] Track jungle camp timers
* [ ] Predict jungle pathing

Possible outputs:

"Enemy jungler likely bot side"
"Top lane vulnerable to gank"

---

## Vision Awareness

* [ ] Detect wards placed
* [ ] Track control wards
* [ ] Suggest ward placements

Example suggestions:

"Ward river brush"
"Clear enemy vision before dragon"

---

# Phase 4 — Macro Decision Engine

The system should analyze the match like a high-elo player.

Create module:

ai_engine.py

Input:

GameState

Output:

Strategic suggestions.

---

## Lane State Analysis

Evaluate:

* minion wave
* tower health
* champion presence

Outputs:

"Freeze wave"
"Push and roam"
"Recall timing optimal"

---

## Objective Priority System

Evaluate:

* team strength
* map pressure
* champion scaling

Possible outputs:

"Contest dragon"
"Trade dragon for herald"
"Push mid before baron"

---

## Fight Evaluation

Before fights:

* evaluate gold difference
* evaluate cooldowns
* evaluate champion scaling

Outputs:

"Fight favorable"
"Avoid teamfight"

---

# Phase 5 — Coaching System

Goal:

Simulate a **Challenger coach voice**.

Suggestions categories:

### Early Game

Examples:

"Enemy jungler started red."
"Push wave before roaming."

---

### Mid Game

Examples:

"Group for dragon."
"Rotate to mid lane."

---

### Late Game

Examples:

"Play around Baron vision."
"Avoid fighting without flash."

---

# Phase 6 — AI Recommendation Layer

Implement hybrid AI.

Approach:

Rule engine + LLM suggestions.

---

## Rule-Based System

Fast decisions:

* objective timers
* item suggestions
* jungle tracking

---

## AI Analysis Layer

Use LLM to analyze match context.

Input example:

GameState JSON

Output:

Strategic coaching.

Example:

"You are ahead. Pressure side lanes and avoid unnecessary fights."

---

# Phase 7 — Overlay UI

Electron overlay.

Features:

* [ ] transparent overlay
* [ ] draggable window
* [ ] compact UI

Display:

* objective timers
* item suggestions
* macro decisions

Example UI:

AI Coach

Next Dragon: 1:10

Suggestions:

• Push bot wave
• Prepare dragon vision
• Enemy jungler top

---

# Phase 8 — Advanced Coaching Features

## Win Probability Model

Estimate win chance.

Inputs:

* gold difference
* towers
* objectives

Output:

Win probability:

62%

---

## Mistake Detection

Detect common mistakes:

* dying before objective
* bad recall timing
* wrong itemization

Output:

"Recall earlier before dragon."

---

## Player Improvement Feedback

After match:

Generate report.

Sections:

* laning phase
* objective control
* teamfight positioning

---

# Phase 9 — Performance and Optimization

* [ ] Reduce CPU usage
* [ ] Optimize polling
* [ ] cache champion data

---

# Phase 10 — Professional Productization

## Security

* [ ] API key protection
* [ ] config management

---

## Installer

Create:

* Windows installer
* auto start with game

---

## Settings System

Allow user to configure:

* suggestion frequency
* overlay position
* coaching style

---

# Phase 11 — Advanced ML Systems

Future improvements.

---

## Jungle Prediction Model

Train model using match history.

Predict:

Enemy jungle path.

---

## Decision Model

Use ML to evaluate:

Best macro decision.

Example:

Split push vs teamfight.

---

# Phase 12 — Elite Coach Mode

Goal:

Simulate a Challenger shotcaller.

Examples:

"Enemy top has no teleport."
"Force Baron now."

---

# Long-Term Vision

Create the most advanced League of Legends coaching assistant.

Comparable tools today include:

* iTero
* Blitz
* Porofessor

The goal is to surpass them with real-time strategic intelligence.
