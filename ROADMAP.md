# ROADMAP.md

# LoL AI Assistant – Project Roadmap

This document defines the development roadmap for the **LoL AI Assistant** project.

The goal is to build a **real-time strategic coaching assistant** for League of Legends that provides Challenger-level macro and decision guidance during matches.

The project will evolve incrementally through versioned releases.

---

# Versioning Strategy

We follow **semantic versioning**:

MAJOR.MINOR.PATCH

Examples:

1.0.0
1.1.0
1.2.0
2.0.0

Definitions:

MAJOR
Large architectural improvements or major AI features.

MINOR
New gameplay features or coaching systems.

PATCH
Bug fixes and performance improvements.

---

# v1.0.0 – Minimal Playable Assistant

Goal:

Create the first functional prototype.

Features:

* Live Client API integration
* Game time tracking
* Objective timers
* Basic suggestion engine
* Flask API endpoint

Output example:

Dragon spawning in 45 seconds.

Status:

Prototype ready for testing.

---

# v1.1.0 – Jungle Awareness

Goal:

Add map awareness and jungle tracking.

Features:

* Detect enemy jungler
* Predict jungle pathing
* Early gank warnings

Example suggestions:

Enemy jungler likely top side.
Bot lane safe to play aggressive.

---

# v1.2.0 – Item Recommendation Engine

Goal:

Improve player decision-making with item suggestions.

Features:

* Detect enemy healing
* Detect heavy AD/AP compositions
* Recommend defensive items

Example:

Enemy team heavy healing.
Build anti-heal item.

---

# v1.3.0 – Champion Composition Analysis

Goal:

Understand team compositions.

Features:

* Detect enemy team archetype

Types:

poke
sustain
dive
scaling
split push

Example suggestion:

Enemy team scaling.
Play aggressive early.

---

# v1.4.0 – Wave and Lane Analysis

Goal:

Improve laning guidance.

Features:

* Wave state detection
* Push / freeze suggestions
* Recall timing hints

Example:

Freeze wave near tower.

---

# v1.5.0 – Vision and Map Control

Goal:

Improve map awareness.

Features:

* Ward placement suggestions
* Vision control alerts
* River and jungle vision reminders

Example:

Place ward near dragon pit.

---

# v2.0.0 – Advanced Macro Coach

Major milestone.

Goal:

Transform the assistant into a true **macro decision engine**.

Features:

* Objective priority system
* Teamfight evaluation
* Risk vs reward analysis
* Map pressure evaluation

Example:

Trade dragon for Herald.

---

# v2.1.0 – Win Condition Detection

Goal:

Identify how the team should win.

Examples:

Protect hypercarry.
Split push strategy.

---

# v2.2.0 – Real-Time Shotcalling

Goal:

Simulate Challenger shotcalling.

Examples:

Group mid.
Push bot then rotate dragon.

---

# v2.3.0 – Power Spike Detection

Goal:

Detect champion power spikes.

Features:

* Mythic item completion detection
* Level spikes
* Late game scaling

Example:

You completed core item.
Look for fight.

---

# v2.4.0 – Teamfight Analyzer

Goal:

Evaluate if fights are good or bad.

Inputs:

* gold difference
* levels
* cooldowns

Output:

Fight favorable.
Avoid teamfight.

---

# v3.0.0 – Challenger AI System

Final vision of the project.

Goal:

Create a full **AI coaching assistant** that behaves like a Challenger-level strategist.

Features:

* AI decision engine
* jungle prediction model
* macro decision engine
* dynamic coaching suggestions

Example suggestions:

Enemy jungler top side.
Start dragon.

Push mid wave then rotate.

---

# Future Vision

Potential advanced systems:

Machine learning models trained on match history.

Features:

* jungle path prediction
* win probability estimation
* automated coaching reports

---

# Long-Term Goal

Create the **most advanced real-time League of Legends coaching assistant** capable of analyzing the match like a high-elo player and providing actionable guidance.
