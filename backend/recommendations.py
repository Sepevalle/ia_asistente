"""Champion and role heuristics used by the live coaching engine."""

from __future__ import annotations

from typing import Any, Dict, List, Set

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

ENGAGE_CHAMPIONS: Set[str] = {
    "Alistar",
    "Amumu",
    "Diana",
    "Galio",
    "JarvanIV",
    "Leona",
    "Malphite",
    "Nautilus",
    "Nocturne",
    "Rakan",
    "Sejuani",
    "Vi",
    "Wukong",
    "Zac",
}

SCALING_CHAMPIONS: Set[str] = {
    "AurelionSol",
    "Jinx",
    "KaiSa",
    "Kassadin",
    "Kayle",
    "KogMaw",
    "Nasus",
    "Senna",
    "Smolder",
    "Sona",
    "Twitch",
    "Veigar",
    "Vladimir",
    "Vayne",
}

JUNGLE_CHAMPIONS: Set[str] = {
    "Belveth",
    "Diana",
    "Ekko",
    "Elise",
    "Evelynn",
    "Fiddlesticks",
    "Graves",
    "Hecarim",
    "Ivern",
    "JarvanIV",
    "Karthus",
    "Kayn",
    "Kindred",
    "LeeSin",
    "Lillia",
    "MasterYi",
    "Nidalee",
    "Nocturne",
    "Nunu",
    "Olaf",
    "Poppy",
    "Rammus",
    "RekSai",
    "Sejuani",
    "Shaco",
    "Skarner",
    "Trundle",
    "Udyr",
    "Vi",
    "Viego",
    "Volibear",
    "Warwick",
    "XinZhao",
    "Zac",
}

SUPPORT_ITEM_KEYWORDS = (
    "world atlas",
    "runic compass",
    "bloodsong",
    "dream maker",
    "celestial opposition",
    "solstice sleigh",
    "zam zaks",
)

SUPPORT_ITEM_IDS = {
    3860,
    3865,
    3866,
    3867,
    3868,
    3869,
    3870,
}

JUNGLE_ITEM_KEYWORDS = (
    "scorchclaw",
    "gustwalker",
    "mosstomper",
    "hailblade",
    "emberknife",
)

JUNGLE_ITEM_IDS = {
    1101,
    1102,
    1103,
}


def detect_enemy_signals(enemies: List[Dict[str, Any]]) -> Dict[str, int]:
    """Summarize composition signals from enemy champions."""
    champion_names = [enemy.get("champion_name", "") for enemy in enemies]

    return {
        "sustain_count": _count_matches(champion_names, SUSTAIN_CHAMPIONS),
        "magic_count": _count_matches(champion_names, MAGIC_DAMAGE_CHAMPIONS),
        "physical_count": _count_matches(champion_names, PHYSICAL_DAMAGE_CHAMPIONS),
        "engage_count": _count_matches(champion_names, ENGAGE_CHAMPIONS),
        "scaling_count": _count_matches(champion_names, SCALING_CHAMPIONS),
    }


def infer_player_role(player: Dict[str, Any]) -> str:
    """Infer a coarse role from summoner spells, items, and champion pool."""
    position = str(player.get("position") or "").upper()
    if position == "JUNGLE":
        return "jungle"
    if position in {"UTILITY", "SUPPORT"}:
        return "support"
    if player.get("has_smite") or player.get("jungle_item_owned"):
        return "jungle"
    if player.get("support_item_owned"):
        return "support"
    if player.get("champion_name") in JUNGLE_CHAMPIONS:
        return "jungle"
    return "laner"


def find_team_jungler(players: List[Dict[str, Any]]) -> Dict[str, Any] | None:
    """Find the most likely jungler in a roster."""
    candidates = [player for player in players if player.get("has_smite") or player.get("jungle_item_owned")]
    if candidates:
        return sorted(candidates, key=lambda item: (item["level"], item["cs"]), reverse=True)[0]

    champion_candidates = [player for player in players if player.get("champion_name") in JUNGLE_CHAMPIONS]
    if champion_candidates:
        return sorted(champion_candidates, key=lambda item: item["cs"], reverse=True)[0]

    return None


def has_support_item(items: List[Dict[str, Any]]) -> bool:
    """Return whether the inventory contains a support starter or upgrade."""
    return _has_item_id(items, SUPPORT_ITEM_IDS) or _has_item_keyword(items, SUPPORT_ITEM_KEYWORDS)


def has_jungle_item(items: List[Dict[str, Any]]) -> bool:
    """Return whether the inventory contains a jungle companion or upgrade."""
    return _has_item_id(items, JUNGLE_ITEM_IDS) or _has_item_keyword(items, JUNGLE_ITEM_KEYWORDS)


def spell_names(raw_spells: Dict[str, Any]) -> List[str]:
    """Extract normalized summoner spell names from the raw payload."""
    names = []
    for spell_key in ("summonerSpellOne", "summonerSpellTwo"):
        spell_data = raw_spells.get(spell_key) or {}
        display_name = str(spell_data.get("displayName") or "").strip()
        raw_display_name = str(spell_data.get("rawDisplayName") or "").strip()
        if display_name:
            names.append(display_name)
        if raw_display_name and raw_display_name != display_name:
            names.append(raw_display_name)
    return names


def has_smite(raw_spells: Dict[str, Any]) -> bool:
    """Detect Smite from spell display names or raw keys."""
    return any(
        token in spell_name.lower() for spell_name in spell_names(raw_spells) for token in ("smite", "aplastar")
    )


def _count_matches(champion_names: List[str], champion_pool: Set[str]) -> int:
    """Count how many champions belong to a predefined archetype."""
    return sum(1 for champion_name in champion_names if champion_name in champion_pool)


def _has_item_keyword(items: List[Dict[str, Any]], keywords: tuple[str, ...]) -> bool:
    """Match inventories against lowercase item-name keywords."""
    for item in items:
        item_name = str(item.get("name", "")).lower()
        if any(keyword in item_name for keyword in keywords):
            return True
    return False


def _has_item_id(items: List[Dict[str, Any]], item_ids: set[int]) -> bool:
    """Match inventories against numeric item ids."""
    for item in items:
        try:
            item_id = int(item.get("id", 0))
        except (TypeError, ValueError):
            continue
        if item_id in item_ids:
            return True
    return False
