const API_URL = "http://127.0.0.1:5000/game";
const POLL_INTERVAL_MS = 2000;

document.addEventListener("DOMContentLoaded", () => {
  refreshState();
  window.setInterval(refreshState, POLL_INTERVAL_MS);
});

async function refreshState() {
  try {
    const response = await fetch(API_URL);
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const data = await response.json();
    renderState(data);
  } catch (error) {
    renderConnectionError(error);
  }
}

function renderState(data) {
  const player = data.player || {};
  const inGame = data.status === "in_game";
  const playerName = inGame
    ? `${player.champion_name || "Unknown"} - ${player.summoner_name || "Jugador"}`
    : "Esperando partida";

  setText("player-name", playerName);
  setText("game-time", data.game_time || "00:00");
  setText("game-phase", formatPhase(data.phase));
  setText(
    "player-kda",
    `${player.kills || 0} / ${player.deaths || 0} / ${player.assists || 0}`
  );
  setText("player-gold", `${player.current_gold || 0}`);
  setText("map-name", data.map?.name || "Sin mapa");
  setText("summary-text", data.summary || "Sin resumen");

  const connectionPill = document.getElementById("connection-pill");
  connectionPill.textContent = inGame ? "Coach activo" : "Esperando cliente";
  connectionPill.dataset.state = inGame ? "online" : "idle";

  renderObjectives(data.objectives || {});
  renderSuggestions(data.suggestions || [], data.connection_error);
}

function renderObjectives(objectives) {
  const container = document.getElementById("objectives");
  container.innerHTML = "";

  const cards = Object.values(objectives);
  if (!cards.length) {
    container.appendChild(
      createEmptyBlock("Los timers de objetivos apareceran al entrar en Summoner's Rift.")
    );
    return;
  }

  for (const objective of cards) {
    const card = document.createElement("article");
    card.className = "objective-card";
    card.dataset.state = objective.is_alive ? "alive" : objective.status;
    card.innerHTML = `
      <span class="objective-name">${objective.name}</span>
      <strong class="objective-timer">${objective.timer}</strong>
      <p class="objective-hint">${objective.hint}</p>
    `;
    container.appendChild(card);
  }
}

function renderSuggestions(suggestions, connectionError) {
  const container = document.getElementById("suggestions");
  container.innerHTML = "";

  if (!suggestions.length) {
    const message =
      connectionError || "No hay sugerencias todavia. Inicia una partida para recibir coaching.";
    container.appendChild(createEmptyBlock(message));
    return;
  }

  for (const suggestion of suggestions) {
    const item = document.createElement("article");
    item.className = "suggestion-card";
    item.dataset.priority = suggestion.priority || "low";
    item.innerHTML = `
      <span class="suggestion-tag">${(suggestion.category || "macro").toUpperCase()}</span>
      <p class="suggestion-copy">${suggestion.message}</p>
    `;
    container.appendChild(item);
  }
}

function renderConnectionError(error) {
  setText("player-name", "Backend no disponible");
  setText("game-time", "--:--");
  setText("game-phase", "Offline");
  setText("player-kda", "0 / 0 / 0");
  setText("player-gold", "0");
  setText("map-name", "Sin conexion");
  setText("summary-text", "Inicia Flask en http://127.0.0.1:5000");

  const connectionPill = document.getElementById("connection-pill");
  connectionPill.textContent = "Backend offline";
  connectionPill.dataset.state = "offline";

  renderObjectives({});
  renderSuggestions([], error.message);
}

function createEmptyBlock(message) {
  const block = document.createElement("div");
  block.className = "empty-state";
  block.textContent = message;
  return block;
}

function setText(id, value) {
  document.getElementById(id).textContent = value;
}

function formatPhase(phase) {
  if (!phase) {
    return "Waiting";
  }

  return phase.charAt(0).toUpperCase() + phase.slice(1);
}
