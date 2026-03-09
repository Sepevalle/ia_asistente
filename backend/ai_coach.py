"""Rule-based coaching engine for the first playable assistant."""

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

    suggestions: List[Dict[str, str]] = []
    signals = detect_enemy_signals(game_state.get("enemies", []))

    suggestions.extend(_objective_suggestions(game_state))
    suggestions.extend(_tempo_suggestions(game_state))
    suggestions.extend(_build_suggestions(signals))

    unique_suggestions = _dedupe_suggestions(suggestions)
    unique_suggestions.sort(key=lambda item: PRIORITY_ORDER[item["priority"]])

    phase = game_state.get("phase", "game")
    summary = f"Coach activo en fase {phase}."

    return {
        "summary": summary,
        "signals": signals,
        "suggestions": unique_suggestions[:5],
    }


def _objective_suggestions(game_state: Dict[str, Any]) -> List[Dict[str, str]]:
    """Generate recommendations around objective timings."""
    suggestions: List[Dict[str, str]] = []
    objectives = game_state.get("objectives", {})

    dragon = objectives.get("dragon")
    if dragon:
        if dragon.get("is_alive"):
            suggestions.append(
                _make_suggestion(
                    "objective",
                    "high",
                    "Dragon disponible: empuja bot y mid antes de entrar a rio.",
                )
            )
        elif dragon.get("seconds_until_spawn", 0) <= 75:
            suggestions.append(
                _make_suggestion(
                    "objective",
                    "high",
                    f"Dragon en {dragon['timer']}: coloca vision y prepara un reset corto.",
                )
            )

    baron = objectives.get("baron")
    if baron:
        if baron.get("is_alive"):
            suggestions.append(
                _make_suggestion(
                    "objective",
                    "high",
                    "Baron disponible: controla vision del rio superior antes de forzar.",
                )
            )
        elif baron.get("seconds_until_spawn", 0) <= 90:
            suggestions.append(
                _make_suggestion(
                    "objective",
                    "medium",
                    f"Baron en {baron['timer']}: limpia vision y deja empujado el carril central.",
                )
            )

    return suggestions


def _tempo_suggestions(game_state: Dict[str, Any]) -> List[Dict[str, str]]:
    """Generate tempo, reset, and fight recommendations."""
    suggestions: List[Dict[str, str]] = []
    player = game_state.get("player", {})
    team_stats = game_state.get("team_stats", {})
    health = player.get("health", {})

    current_gold = player.get("current_gold", 0)
    if current_gold >= 1300:
        suggestions.append(
            _make_suggestion(
                "tempo",
                "medium",
                f"Tienes {current_gold} de oro sin gastar: busca ventana de reset antes de la proxima pelea.",
            )
        )

    max_health = health.get("max", 0)
    current_health = health.get("current", 0)
    if max_health and current_health / max_health <= 0.35:
        suggestions.append(
            _make_suggestion(
                "survival",
                "high",
                "Estas bajo de vida: evita forzar y prioriza reset o recursos antes de pelear.",
            )
        )

    kill_diff = team_stats.get("kill_diff", 0)
    phase = game_state.get("phase")
    if kill_diff >= 4:
        suggestions.append(
            _make_suggestion(
                "macro",
                "medium",
                "Tienes ventaja de kills: usa prioridad de oleadas para entrar primero al objetivo.",
            )
        )
    elif kill_diff <= -4:
        suggestions.append(
            _make_suggestion(
                "macro",
                "medium",
                "Vais por detras: evita pelear a ciegas y juega a limpiar oleadas con vision defensiva.",
            )
        )
    elif phase == "early":
        suggestions.append(
            _make_suggestion(
                "macro",
                "low",
                "Fase temprana: usa tus wards para asegurar rio y detectar la ruta del jungla rival.",
            )
        )

    return suggestions


def _build_suggestions(signals: Dict[str, int]) -> List[Dict[str, str]]:
    """Generate itemization recommendations from the enemy composition."""
    suggestions: List[Dict[str, str]] = []

    if signals.get("sustain_count", 0) >= 2:
        suggestions.append(
            _make_suggestion(
                "build",
                "medium",
                "El rival tiene bastante sustain: prioriza anti-curacion en tu siguiente compra util.",
            )
        )

    if signals.get("magic_count", 0) >= 3:
        suggestions.append(
            _make_suggestion(
                "build",
                "low",
                "La composicion rival carga bastante dano magico: la resistencia magica gana valor.",
            )
        )
    elif signals.get("physical_count", 0) >= 4:
        suggestions.append(
            _make_suggestion(
                "build",
                "low",
                "La composicion rival es muy AD: una pieza temprana de armadura puede estabilizar el mid game.",
            )
        )

    return suggestions


def _make_suggestion(category: str, priority: str, message: str) -> Dict[str, str]:
    """Create a structured suggestion payload."""
    return {
        "category": category,
        "priority": priority,
        "message": message,
    }


def _dedupe_suggestions(
    suggestions: List[Dict[str, str]]
) -> List[Dict[str, str]]:
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
