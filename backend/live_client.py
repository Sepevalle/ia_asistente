"""Live Client API access layer."""

from __future__ import annotations

import os
from typing import Any, Dict, Tuple

import requests
import urllib3

from demo_data import get_demo_data

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

LIVE_CLIENT_URL = os.getenv(
    "LOL_LIVE_CLIENT_URL", "https://127.0.0.1:2999/liveclientdata/allgamedata"
)
REQUEST_TIMEOUT = float(os.getenv("LOL_LIVE_CLIENT_TIMEOUT", "2"))


def get_live_data(use_demo: bool = False) -> Tuple[Dict[str, Any], str | None]:
    """Fetch the current game snapshot from the local Live Client API."""
    if use_demo or os.getenv("LOL_ASSISTANT_DEMO") == "1":
        return get_demo_data(), None

    try:
        response = requests.get(
            LIVE_CLIENT_URL,
            timeout=REQUEST_TIMEOUT,
            verify=False,
        )
        response.raise_for_status()

        payload = response.json()
        if not isinstance(payload, dict):
            return {}, "La Live Client API devolvio un formato inesperado."

        return payload, None
    except requests.RequestException as exc:
        return {}, f"No se pudo conectar con la Live Client API: {exc}"
    except ValueError as exc:
        return {}, f"La respuesta de la Live Client API no es JSON valido: {exc}"
