"""Live Client API access layer with endpoint aggregation and caching."""

from __future__ import annotations

import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, Tuple

import requests
import urllib3

from demo_data import get_demo_data

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LIVE_CLIENT_BASE_URL = os.getenv(
    "LOL_LIVE_CLIENT_BASE_URL", "https://127.0.0.1:2999/liveclientdata"
)
REQUEST_TIMEOUT = float(os.getenv("LOL_LIVE_CLIENT_TIMEOUT", "2"))
CACHE_TTL = float(os.getenv("LOL_LIVE_CACHE_TTL", "0.75"))

ENDPOINT_PATHS = {
    "gameData": "gamestats",
    "activePlayer": "activeplayer",
    "activePlayerAbilities": "activeplayerabilities",
    "activePlayerName": "activeplayername",
    "allPlayers": "playerlist",
    "events": "eventdata",
}

REQUIRED_SECTIONS = {"gameData", "activePlayer", "allPlayers", "events"}

_CACHE: Dict[str, Any] = {
    "expires_at": 0.0,
    "payload": {},
    "error": None,
    "meta": {},
}


def get_live_data(
    use_demo: bool = False,
) -> Tuple[Dict[str, Any], str | None, Dict[str, Any]]:
    """Fetch the current game snapshot from the local Live Client API."""
    if use_demo or os.getenv("LOL_ASSISTANT_DEMO") == "1":
        return get_demo_data(), None, _build_meta(source="demo", cache_hit=False)

    now = time.time()
    if _CACHE["payload"] and now < _CACHE["expires_at"]:
        cached_meta = dict(_CACHE["meta"])
        cached_meta["cache_hit"] = True
        cached_meta["cache_age_ms"] = int((now - cached_meta.get("fetched_at_epoch", now)) * 1000)
        return _CACHE["payload"], _CACHE["error"], cached_meta

    payload, error, meta = _fetch_live_bundle()
    if payload:
        _CACHE["payload"] = payload
        _CACHE["error"] = error
        _CACHE["meta"] = meta
        _CACHE["expires_at"] = time.time() + CACHE_TTL
        return payload, error, meta

    if _CACHE["payload"]:
        stale_meta = dict(_CACHE["meta"])
        stale_meta["cache_hit"] = True
        stale_meta["stale"] = True
        stale_meta["cache_age_ms"] = int((time.time() - stale_meta.get("fetched_at_epoch", time.time())) * 1000)
        return _CACHE["payload"], error or _CACHE["error"], stale_meta

    return payload, error, meta


def _fetch_live_bundle() -> Tuple[Dict[str, Any], str | None, Dict[str, Any]]:
    """Fetch a smaller live-data bundle from dedicated endpoints."""
    started_at = time.perf_counter()
    payload: Dict[str, Any] = {}
    endpoint_errors: Dict[str, str] = {}

    with ThreadPoolExecutor(max_workers=len(ENDPOINT_PATHS)) as executor:
        future_map = {
            executor.submit(_fetch_endpoint, section, path): section
            for section, path in ENDPOINT_PATHS.items()
        }

        for future in as_completed(future_map):
            section = future_map[future]
            try:
                value = future.result()
            except Exception as exc:
                endpoint_errors[section] = str(exc)
                continue

            if value is not None:
                payload[section] = value

    fallback_used = False
    if REQUIRED_SECTIONS - payload.keys():
        fallback_payload, fallback_error = _fetch_all_game_data()
        if fallback_payload:
            payload = _merge_payloads(payload, fallback_payload)
            fallback_used = True
        elif fallback_error:
            endpoint_errors["allGameData"] = fallback_error

    fetch_ms = int((time.perf_counter() - started_at) * 1000)
    error = _compose_error(endpoint_errors)
    source = "hybrid" if fallback_used else "bundle"

    if not payload:
        return {}, error or "No se pudo obtener informacion de la Live Client API.", _build_meta(
            source=source,
            cache_hit=False,
            fetch_ms=fetch_ms,
            available_sections=[],
            partial_errors=endpoint_errors,
        )

    return payload, error, _build_meta(
        source=source,
        cache_hit=False,
        fetch_ms=fetch_ms,
        available_sections=sorted(payload.keys()),
        partial_errors=endpoint_errors,
    )


def _fetch_endpoint(section: str, path: str) -> Any:
    """Fetch and decode a single Live Client API endpoint."""
    response = requests.get(
        f"{LIVE_CLIENT_BASE_URL}/{path}",
        timeout=REQUEST_TIMEOUT,
        verify=False,
    )
    response.raise_for_status()

    if section == "activePlayerName":
        return response.text.strip().strip('"')

    return response.json()


def _fetch_all_game_data() -> Tuple[Dict[str, Any], str | None]:
    """Fallback to the aggregate endpoint when dedicated endpoints are incomplete."""
    try:
        response = requests.get(
            f"{LIVE_CLIENT_BASE_URL}/allgamedata",
            timeout=REQUEST_TIMEOUT,
            verify=False,
        )
        response.raise_for_status()
        payload = response.json()
        if not isinstance(payload, dict):
            return {}, "La Live Client API devolvio un formato inesperado en /allgamedata."
        return payload, None
    except requests.RequestException as exc:
        return {}, f"No se pudo conectar con /allgamedata: {exc}"
    except ValueError as exc:
        return {}, f"La respuesta de /allgamedata no es JSON valido: {exc}"


def _merge_payloads(primary: Dict[str, Any], fallback: Dict[str, Any]) -> Dict[str, Any]:
    """Merge partial endpoint data with the aggregate endpoint payload."""
    merged = dict(fallback)
    merged.update(primary)
    return merged


def _compose_error(endpoint_errors: Dict[str, str]) -> str | None:
    """Build a compact error string from partial endpoint failures."""
    if not endpoint_errors:
        return None

    error_parts = [f"{section}: {message}" for section, message in sorted(endpoint_errors.items())]
    return " | ".join(error_parts)


def _build_meta(
    source: str,
    cache_hit: bool,
    fetch_ms: int = 0,
    available_sections: list[str] | None = None,
    partial_errors: Dict[str, str] | None = None,
) -> Dict[str, Any]:
    """Return diagnostics used by the overlay and debugging endpoints."""
    fetched_at_epoch = time.time()
    return {
        "source": source,
        "cache_hit": cache_hit,
        "cache_ttl_ms": int(CACHE_TTL * 1000),
        "cache_age_ms": 0,
        "fetch_ms": fetch_ms,
        "available_sections": available_sections or [],
        "partial_errors": partial_errors or {},
        "fetched_at_epoch": fetched_at_epoch,
        "stale": False,
    }
