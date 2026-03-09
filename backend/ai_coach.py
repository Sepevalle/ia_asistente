def analyze_game(game_data):
    """
    Analyze live game data and return suggestions.
    """

    suggestions = []

    game_time = game_data.get("gameData", {}).get("gameTime", 0)

    if game_time > 300:
        suggestions.append("Start preparing for first dragon.")

    return {
        "suggestions": suggestions
    }