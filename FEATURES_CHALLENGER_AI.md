# FEATURES_CHALLENGER_AI.md

# Challenger AI Coaching System

Goal:

Design an AI system capable of providing **high-elo strategic coaching** during a League of Legends match.

The AI should simulate the reasoning of a **Challenger player or professional coach**.

The system must continuously evaluate the game state and output **clear and actionable recommendations**.

---

# Core Philosophy

A Challenger player constantly evaluates:

1. Map pressure
2. Objective priority
3. Vision control
4. Champion power spikes
5. Enemy mistakes

The AI must replicate this reasoning process.

---

# Decision Categories

The AI should generate suggestions in these categories:

* Macro decisions
* Lane management
* Jungle awareness
* Objective control
* Itemization
* Teamfight evaluation

---

# 1 Early Game Coaching (0-10 minutes)

Focus:

* jungle tracking
* lane pressure
* wave control
* early objectives

Features:

### Jungle Start Prediction

Detect enemy jungle start.

Examples:

Enemy jungler started bot side.

Suggestions:

Top lane should play safe.

---

### Level 2 Priority

Evaluate lane push advantage.

Outputs:

Push for level 2 spike.

or

Avoid trading until level 3.

---

### Early Gank Warning

Use jungle path prediction.

Example:

Enemy jungler likely ganking top at 3:15.

---

### Wave Management

AI evaluates wave state.

Suggestions:

Freeze wave near tower.

or

Push wave before recalling.

---

# 2 Mid Game Coaching (10-20 minutes)

Focus:

* rotations
* objective control
* vision

---

### Objective Preparation

AI checks:

* dragon timer
* team gold
* summoner spells

Example suggestion:

Dragon spawning in 50 seconds.
Push bot wave and place vision.

---

### Lane Rotation

AI detects best lane to rotate.

Examples:

Rotate mid after taking bot tower.

or

Send top laner to split push.

---

### Enemy Jungle Pressure

Evaluate map state.

Example output:

Enemy jungler seen top side.
Safe to invade bot jungle.

---

### Tower Pressure

Evaluate tower HP and wave state.

Example:

Push mid to pressure tier 1 tower.

---

# 3 Late Game Coaching (20+ minutes)

Focus:

* Baron control
* pick opportunities
* teamfight setup

---

### Baron Control

AI checks:

* enemy deaths
* map vision
* damage potential

Example:

Enemy jungler dead.
Start Baron.

---

### Pick Opportunities

AI detects isolated enemies.

Example:

Enemy support alone in river.
Possible pick.

---

### Split Push Strategy

Evaluate champion kit.

Example:

Your champion strong in side lane.
Pressure top while team holds mid.

---

# 4 Itemization Intelligence

AI evaluates:

* enemy damage types
* healing
* armor

Examples:

Enemy team heavy healing.
Buy anti-heal item.

Enemy AP burst.
Buy magic resist.

---

# 5 Summoner Spell T
