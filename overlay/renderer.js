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
  setText("kill-diff", formatSignedNumber(data.team_stats?.kill_diff || 0));
  setText("alive-diff", formatSignedNumber(data.team_stats?.alive_diff || 0));
  setText("map-name", data.map?.name || "Sin mapa");
  setText("summary-text", data.summary || "Sin resumen");
  setText("signal-summary", buildSignalSummary(data));

  const connectionPill = document.getElementById("connection-pill");
  connectionPill.textContent = inGame ? "Coach activo" : "Esperando cliente";
  connectionPill.dataset.state = inGame ? "online" : "idle";

  renderObjectives(data.objectives || {});
  renderSignals(data);
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
    const metadata = buildObjectiveMetadata(objective);
    card.innerHTML = `
      <span class="objective-name">${objective.name}</span>
      <strong class="objective-timer">${objective.timer}</strong>
      <span class="objective-meta">${metadata}</span>
      <p class="objective-hint">${objective.hint}</p>
    `;
    container.appendChild(card);
  }
}

function renderSignals(data) {
  const container = document.getElementById("signals-grid");
  container.innerHTML = "";

  if (data.status !== "in_game") {
    container.appendChild(
      createEmptyBlock("Las senales tacticas apareceran cuando haya partida activa.")
    );
    return;
  }

  const signals = data.signals || {};
  const enemyJungler = data.team_context?.enemy_jungler;
  const liveClient = data.live_client || {};

  const cards = [
    {
      label: "Fight",
      value: formatToken(signals.fight_state || "even"),
      tone: resolveFightTone(signals.fight_state)
    },
    {
      label: "Momentum",
      value: formatToken(signals.momentum || "neutral"),
      tone: resolveMomentumTone(signals.momentum)
    },
    {
      label: "Role",
      value: formatToken(signals.player_role || "laner"),
      tone: "neutral"
    },
    {
      label: "Enemy JG",
      value: formatEnemyJungler(enemyJungler),
      tone: enemyJungler?.is_alive === false ? "good" : "neutral"
    },
    {
      label: "Feed",
      value: formatFeedSource(liveClient),
      tone: liveClient.stale || liveClient.cache_hit ? "good" : "neutral"
    }
  ];

  for (const signal of cards) {
    const card = document.createElement("article");
    card.className = "signal-card";
    card.dataset.tone = signal.tone;
    card.innerHTML = `
      <span>${signal.label}</span>
      <strong>${signal.value}</strong>
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
  setText("kill-diff", "0");
  setText("alive-diff", "0");
  setText("map-name", "Sin conexion");
  setText("summary-text", "Inicia Flask en http://127.0.0.1:5000");
  setText("signal-summary", "Sin senales");

  const connectionPill = document.getElementById("connection-pill");
  connectionPill.textContent = "Backend offline";
  connectionPill.dataset.state = "offline";

  renderObjectives({});
  renderSignals({ status: "offline" });
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

function formatSignedNumber(value) {
  if (value > 0) {
    return `+${value}`;
  }

  return `${value}`;
}

function formatToken(value) {
  return String(value)
    .replaceAll("_", " ")
    .replace(/\b\w/g, (match) => match.toUpperCase());
}

function formatEnemyJungler(enemyJungler) {
  if (!enemyJungler) {
    return "Unknown";
  }

  if (enemyJungler.is_alive === false) {
    return `Dead ${enemyJungler.respawn_timer || 0}s`;
  }

  return `${enemyJungler.champion_name || "JG"} alive`;
}

function formatFeedSource(liveClient) {
  if (!liveClient.source) {
    return "Unknown";
  }

  const source = formatToken(liveClient.source);
  if (liveClient.stale) {
    return `${source} stale`;
  }

  if (liveClient.cache_hit) {
    return `${source} cache`;
  }

  return `${source} ${liveClient.fetch_ms || 0}ms`;
}

function buildSignalSummary(data) {
  if (data.status !== "in_game") {
    return "Sin senales";
  }

  const fight = formatToken(data.signals?.fight_state || "even");
  const momentum = formatToken(data.signals?.momentum || "neutral");
  return `${fight} / ${momentum}`;
}

function buildObjectiveMetadata(objective) {
  const parts = [];

  if (objective.priority) {
    parts.push(`prio ${objective.priority}`);
  }

  if (typeof objective.ally_stacks === "number" && typeof objective.enemy_stacks === "number") {
    parts.push(`stacks ${objective.ally_stacks}-${objective.enemy_stacks}`);
  }

  return parts.join(" - ");
}

function resolveFightTone(fightState) {
  if (fightState === "advantage" || fightState === "slight_advantage") {
    return "good";
  }

  if (
    fightState === "disadvantage" ||
    fightState === "slight_disadvantage" ||
    fightState === "unstable"
  ) {
    return "bad";
  }

  return "neutral";
}

function resolveMomentumTone(momentum) {
  if (momentum === "allies") {
    return "good";
  }

  if (momentum === "enemies") {
    return "bad";
  }

  return "neutral";
}
