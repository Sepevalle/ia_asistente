"""Rule-based coaching engine for the live assistant."""

from __future__ import annotations

from typing import Any, Dict, List

from recommendations import detect_enemy_signals

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


def analyze_game(game_state: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze the normalized game state and return coaching suggestions."""
    if game_state.get("status") != "in_game":
        return {
            "summary": "Esperando una partida activa.",
            "signals": {},
            "suggestions": [
                _make_suggestion(
                    "system",
                    "medium",
                    "Abre una partida de League of Legends para activar el asistente en tiempo real.",
                )
            ],
        }

    signals = _build_signals(game_state)
    suggestions: List[Dict[str, str]] = []

    suggestions.extend(_objective_suggestions(game_state, signals))
    suggestions.extend(_fight_window_suggestions(game_state, signals))
    suggestions.extend(_tempo_suggestions(game_state, signals))
    suggestions.extend(_macro_suggestions(game_state, signals))
    suggestions.extend(_build_suggestions(signals))
    suggestions.extend(_role_suggestions(game_state, signals))

    unique_suggestions = _dedupe_suggestions(suggestions)
    unique_suggestions.sort(key=lambda item: PRIORITY_ORDER[item["priority"]])

    return {
        "summary": _build_summary(game_state, signals),
        "signals": signals,
        "suggestions": unique_suggestions[:6],
    }


def _build_signals(game_state: Dict[str, Any]) -> Dict[str, Any]:
    """Aggregate the most relevant live signals for decision making."""
    player = game_state.get("player", {})
    team_stats = game_state.get("team_stats", {})
    event_summary = game_state.get("event_summary", {})
    tactical = game_state.get("tactical", {})
    team_context = game_state.get("team_context", {})
    objectives = game_state.get("objectives", {})

    enemy_signals = detect_enemy_signals(game_state.get("enemies", []))

    return {
        **enemy_signals,
        "player_role": team_context.get("player_role", "laner"),
        "fight_state": tactical.get("fight_state", "even"),
        "momentum": event_summary.get("momentum", "neutral"),
        "momentum_score": event_summary.get("momentum_score", 0),
        "alive_diff": team_stats.get("alive_diff", 0),
        "kill_diff": team_stats.get("kill_diff", 0),
        "cs_diff": team_stats.get("cs_diff", 0),
        "avg_level_diff": team_stats.get("avg_level_diff", 0.0),
        "player_health_ratio": player.get("health", {}).get("ratio", 0.0),
        "player_resource_ratio": player.get("resource", {}).get("ratio", 0.0),
        "player_high_gold": tactical.get("player_high_gold", False),
        "player_low_health": tactical.get("player_low_health", False),
        "kill_participation": player.get("kill_participation", 0.0),
        "enemy_jungler_dead": tactical.get("enemy_jungler_dead", False),
        "ally_jungler_dead": tactical.get("ally_jungler_dead", False),
        "recent_pick": event_summary.get("recent_pick", {}),
        "dragon_priority": objectives.get("dragon", {}).get("priority", "low"),
        "baron_priority": objectives.get("baron", {}).get("priority", "low"),
        "ultimate_unlocked": player.get("ultimate_unlocked", False),
    }


def _objective_suggestions(
    game_state: Dict[str, Any],
    signals: Dict[str, Any],
) -> List[Dict[str, str]]:
    """Generate recommendations around live objective windows."""
    suggestions: List[Dict[str, str]] = []
    objectives = game_state.get("objectives", {})
    dragon = objectives.get("dragon", {})
    baron = objectives.get("baron", {})
    recent_pick = signals.get("recent_pick", {})

    if dragon.get("is_alive") and signals.get("dragon_priority") == "high":
        suggestions.append(
            _make_suggestion(
                "objective",
                "high",
                "Dragon es la mejor jugada ahora: gana prioridad de mid/bot y entra con vision.",
            )
        )
    elif dragon.get("seconds_until_spawn", 999) <= 75:
        suggestions.append(
            _make_suggestion(
                "objective",
                "high" if signals.get("dragon_priority") == "high" else "medium",
                f"Dragon en {dragon.get('timer', '00:00')}: prepara reset, wards y la oleada antes de moverte.",
            )
        )

    if baron.get("is_alive") and signals.get("baron_priority") == "high":
        suggestions.append(
            _make_suggestion(
                "objective",
                "high",
                "Baron abierto con ventaja: empuja mid, borra vision y amenaza start o turn.",
            )
        )
    elif baron.get("seconds_until_spawn", 999) <= 90:
        suggestions.append(
            _make_suggestion(
                "objective",
                "medium",
                f"Baron en {baron.get('timer', '00:00')}: sincroniza reset y control del rio superior.",
            )
        )

    if recent_pick.get("team") == "allies" and recent_pick.get("age_seconds") is not None:
        if dragon.get("is_alive") or baron.get("is_alive"):
            suggestions.append(
                _make_suggestion(
                    "conversion",
                    "high",
                    "Teneis una pick reciente: convierte la ventaja en objetivo, vision profunda o torre.",
                )
            )

    return suggestions


def _fight_window_suggestions(
    game_state: Dict[str, Any],
    signals: Dict[str, Any],
) -> List[Dict[str, str]]:
    """Generate fight and pick-window recommendations."""
    suggestions: List[Dict[str, str]] = []
    fight_state = signals.get("fight_state")
    recent_pick = signals.get("recent_pick", {})

    if recent_pick.get("team") == "enemies":
        suggestions.append(
            _make_suggestion(
                "warning",
                "high",
                "Ellos sacaron una pick reciente: no pelees a ciegas y concede terreno hasta reagrupar.",
            )
        )

    if fight_state == "advantage":
        suggestions.append(
            _make_suggestion(
                "fight",
                "medium",
                "Teneis superioridad numerica: juega agresivo sobre vision y fuerza primero el espacio.",
            )
        )
    elif fight_state == "disadvantage":
        suggestions.append(
            _make_suggestion(
                "fight",
                "high",
                "Estais en desventaja numerica: evita all-in y prioriza limpiar oleada desde zona segura.",
            )
        )
    elif fight_state == "unstable":
        suggestions.append(
            _make_suggestion(
                "survival",
                "high",
                "Tu estado es inestable para pelear: resetea o espera recursos antes de entrar.",
            )
        )

    if signals.get("enemy_jungler_dead"):
        suggestions.append(
            _make_suggestion(
                "jungle",
                "high",
                "Jungla rival muerto: invade vision o asegura objetivo antes de que reaparezca.",
            )
        )
    elif signals.get("ally_jungler_dead"):
        suggestions.append(
            _make_suggestion(
                "jungle",
                "medium",
                "Tu jungla esta muerto: no inicies objetivo neutral sin control total de la zona.",
            )
        )

    return suggestions


def _tempo_suggestions(
    game_state: Dict[str, Any],
    signals: Dict[str, Any],
) -> List[Dict[str, str]]:
    """Generate tempo and resource recommendations."""
    suggestions: List[Dict[str, str]] = []
    player = game_state.get("player", {})

    if signals.get("player_high_gold"):
        suggestions.append(
            _make_suggestion(
                "tempo",
                "medium",
                f"Tienes {player.get('current_gold', 0)} de oro: busca reset util antes de la siguiente ventana grande.",
            )
        )

    if signals.get("player_low_health"):
        suggestions.append(
            _make_suggestion(
                "survival",
                "high",
                "Estas bajo de vida: evita gastar la prioridad en una pelea mala y resetea si puedes.",
            )
        )

    if signals.get("player_resource_ratio", 1.0) <= 0.25 and signals.get("player_role") != "jungle":
        suggestions.append(
            _make_suggestion(
                "resources",
                "medium",
                "Vas corto de recurso: no fuerces una rotacion larga sin antes recuperar tempo.",
            )
        )

    if not signals.get("ultimate_unlocked") and game_state.get("phase") != "early":
        suggestions.append(
            _make_suggestion(
                "power",
                "low",
                "Tu definitiva no aporta ventana real todavia: prioriza picks cortos o limpieza de oleadas.",
            )
        )

    return suggestions


def _macro_suggestions(
    game_state: Dict[str, Any],
    signals: Dict[str, Any],
) -> List[Dict[str, str]]:
    """Generate macro suggestions from team momentum and leads."""
    suggestions: List[Dict[str, str]] = []
    momentum = signals.get("momentum")

    if momentum == "allies" and signals.get("kill_diff", 0) >= 2:
        suggestions.append(
            _make_suggestion(
                "macro",
                "medium",
                "Llevais el momentum: convierte picks en vision profunda y usa la siguiente oleada para moverte primero.",
            )
        )
    elif momentum == "enemies":
        suggestions.append(
            _make_suggestion(
                "macro",
                "medium",
                "Ellos llevan el ritmo: frena la partida, limpia vision defensiva y no des entrada gratis al rio.",
            )
        )

    if signals.get("avg_level_diff", 0.0) >= 1:
        suggestions.append(
            _make_suggestion(
                "macro",
                "low",
                "Teneis ventaja de niveles: busca primero espacio en rio y obliga a que ellos entren tarde.",
            )
        )
    elif signals.get("avg_level_diff", 0.0) <= -1:
        suggestions.append(
            _make_suggestion(
                "macro",
                "medium",
                "Vais por detras en niveles: evita frontales largos y juega a trade de oleadas u objetivos cruzados.",
            )
        )

    if signals.get("cs_diff", 0) >= 40:
        suggestions.append(
            _make_suggestion(
                "macro",
                "low",
                "La ventaja de farmeo ya es relevante: no la regales con peleas fuera de tempo.",
            )
        )

    return suggestions


def _build_suggestions(signals: Dict[str, Any]) -> List[Dict[str, str]]:
    """Generate itemization and composition recommendations."""
    suggestions: List[Dict[str, str]] = []

    if signals.get("sustain_count", 0) >= 2:
        suggestions.append(
            _make_suggestion(
                "build",
                "medium",
                "La composicion rival tiene sustain fuerte: mete anti-curacion temprano si tu campeon puede aplicarla.",
            )
        )

    if signals.get("magic_count", 0) >= 3:
        suggestions.append(
            _make_suggestion(
                "build",
                "low",
                "El dano magico rival es alto: una compra de resistencia magica gana mucho valor.",
            )
        )
    elif signals.get("physical_count", 0) >= 4:
        suggestions.append(
            _make_suggestion(
                "build",
                "low",
                "La composicion rival es muy AD: armadura temprana y posicionamiento limpio valen mas.",
            )
        )

    if signals.get("engage_count", 0) >= 3:
        suggestions.append(
            _make_suggestion(
                "spacing",
                "low",
                "El rival tiene mucho engage: guarda movilidad para kitear su primera entrada.",
            )
        )

    if signals.get("scaling_count", 0) >= 2 and signals.get("kill_diff", 0) >= 0:
        suggestions.append(
            _make_suggestion(
                "macro",
                "low",
                "Ellos escalan bien: castiga ahora las ventanas de objetivo en lugar de dejar la partida gratis.",
            )
        )

    return suggestions


def _role_suggestions(
    game_state: Dict[str, Any],
    signals: Dict[str, Any],
) -> List[Dict[str, str]]:
    """Generate role-aware advice from the active player's lane function."""
    suggestions: List[Dict[str, str]] = []
    role = signals.get("player_role", "laner")
    objectives = game_state.get("objectives", {})

    if role == "jungle":
        if signals.get("dragon_priority") == "high" and objectives.get("dragon", {}).get("seconds_until_spawn", 999) <= 75:
            suggestions.append(
                _make_suggestion(
                    "role",
                    "high",
                    "Como jungla, sincroniza tu path hacia bot side y llega antes que el rival al setup de dragon.",
                )
            )
        else:
            suggestions.append(
                _make_suggestion(
                    "role",
                    "low",
                    "Como jungla, usa la prioridad de lineas para transformar vision en objetivo y no al reves.",
                )
            )
    elif role == "support":
        suggestions.append(
            _make_suggestion(
                "role",
                "medium",
                "Como support, sal primero de base cuando haya objetivo cercano y gana el primer ward profundo.",
            )
        )
    else:
        if signals.get("recent_pick", {}).get("team") == "allies":
            suggestions.append(
                _make_suggestion(
                    "role",
                    "medium",
                    "Como laner, empuja rapido la siguiente wave y mueve primero para convertir la pick.",
                )
            )
        else:
            suggestions.append(
                _make_suggestion(
                    "role",
                    "low",
                    "Como laner, tu prioridad de wave decide el acceso al rio: no rotes dejando una wave gratis.",
                )
            )

    return suggestions


def _build_summary(game_state: Dict[str, Any], signals: Dict[str, Any]) -> str:
    """Create a compact live summary shown in the overlay header."""
    phase = game_state.get("phase", "game")
    fight_state = signals.get("fight_state", "even")
    momentum = signals.get("momentum", "neutral")

    if signals.get("enemy_jungler_dead"):
        return f"Fase {phase}. Ventana fuerte: jungla rival fuera y {momentum} a favor."
    if fight_state == "advantage":
        return f"Fase {phase}. Teneis ventana de pelea con momentum {momentum}."
    if fight_state == "disadvantage":
        return f"Fase {phase}. Juega defensivo hasta recuperar numeros o tempo."
    return f"Fase {phase}. Estado {fight_state} con momentum {momentum}."


def _make_suggestion(category: str, priority: str, message: str) -> Dict[str, str]:
    """Create a structured suggestion payload."""
    return {
        "category": category,
        "priority": priority,
        "message": message,
    }


def _dedupe_suggestions(suggestions: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """Remove duplicate messages while preserving order."""
    seen_messages = set()
    unique_suggestions: List[Dict[str, str]] = []

    for suggestion in suggestions:
        message = suggestion["message"]
        if message in seen_messages:
            continue
        seen_messages.add(message)
        unique_suggestions.append(suggestion)

    return unique_suggestions
