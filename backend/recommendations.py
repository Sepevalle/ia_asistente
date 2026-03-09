"""Champion archetype helpers used by the first rule engine."""

from __future__ import annotations

from typing import Dict, List, Set

SUSTAIN_CHAMPIONS: Set[str] = {
    "Aatrox",
    "Briar",
    "DrMundo",
    "Fiora",
    "Illaoi",
    "Mundo",
    "Nami",
    "Nilah",
    "Rhaast",
    "Samira",
    "Seraphine",
    "Soraka",
    "Swain",
    "Sylas",
    "Vladimir",
    "Warwick",
    "Yuumi",
    "Zac",
}

MAGIC_DAMAGE_CHAMPIONS: Set[str] = {
    "Ahri",
    "Annie",
    "AurelionSol",
    "Brand",
    "Cassiopeia",
    "Diana",
    "Ekko",
    "Elise",
    "Evelynn",
    "Fiddlesticks",
    "Gragas",
    "Hwei",
    "Karthus",
    "Kassadin",
    "Katarina",
    "Kennen",
    "LeBlanc",
    "Lillia",
    "Lux",
    "Malzahar",
    "Mordekaiser",
    "Morgana",
    "Neeko",
    "Nidalee",
    "Orianna",
    "Ryze",
    "Seraphine",
    "Syndra",
    "Taliyah",
    "TwistedFate",
    "Veigar",
    "Vex",
    "Viktor",
    "Xerath",
    "Ziggs",
    "Zoe",
}

PHYSICAL_DAMAGE_CHAMPIONS: Set[str] = {
    "Aatrox",
    "Aphelios",
    "Ashe",
    "Belveth",
    "Caitlyn",
    "Darius",
    "Draven",
    "Ezreal",
    "Fiora",
    "Gangplank",
    "Gnar",
    "Graves",
    "Hecarim",
    "Irelia",
    "JarvanIV",
    "Jax",
    "Jhin",
    "Jinx",
    "KaiSa",
    "Kalista",
    "Kayn",
    "KhaZix",
    "Kindred",
    "LeeSin",
    "Lucian",
    "MasterYi",
    "MissFortune",
    "Nocturne",
    "Olaf",
    "Pantheon",
    "Quinn",
    "Rengar",
    "Riven",
    "Samira",
    "Sett",
    "Talon",
    "Tristana",
    "Tryndamere",
    "Vayne",
    "Vi",
    "XinZhao",
    "Yasuo",
    "Yone",
    "Zed",
}


def detect_enemy_signals(enemies: List[Dict[str, str]]) -> Dict[str, int]:
    """Summarize simple composition signals from enemy champions."""
    champion_names = [enemy.get("champion_name", "") for enemy in enemies]

    return {
        "sustain_count": _count_matches(champion_names, SUSTAIN_CHAMPIONS),
        "magic_count": _count_matches(champion_names, MAGIC_DAMAGE_CHAMPIONS),
        "physical_count": _count_matches(champion_names, PHYSICAL_DAMAGE_CHAMPIONS),
    }


def _count_matches(champion_names: List[str], champion_pool: Set[str]) -> int:
    """Count how many champions belong to a predefined archetype."""
    return sum(1 for champion_name in champion_names if champion_name in champion_pool)
