const LISTENING_URL = "assets/listening.json";
const POLL_MS = 60000;

function ago(uts) {
  const delta = Math.max(0, Math.floor(Date.now() / 1000 - uts));
  for (const [step, unit] of [[86400, "d"], [3600, "h"], [60, "m"]]) {
    if (delta >= step) {
      return `${Math.floor(delta / step)}${unit}`;
    }
  }
  return "just now";
}

function widgetSection(data) {
  const section = document.createElement("section");
  section.className = "entry";
  section.id = "listening";

  const heading = document.createElement("h2");
  heading.className = "cmd";
  heading.textContent = "listening";

  const line = document.createElement("p");
  const state = data.playing ? "\u25B6 " : (data.uts ? `\u25FC ${ago(data.uts)} \u2014 ` : "");
  const label = `${state}${data.track} \u2014 ${data.artist}`;

  if (data.url) {
    const link = document.createElement("a");
    link.href = data.url;
    link.target = "_blank";
    link.rel = "noopener";
    link.textContent = label;
    line.append(link);
  } else {
    line.textContent = label;
  }

  section.append(heading, line);
  return section;
}

function show(section) {
  const existing = document.getElementById("listening");
  if (existing) {
    existing.replaceWith(section);
    return;
  }
  document.getElementById("contact").before(section);
}

function hide() {
  document.getElementById("listening")?.remove();
}

async function refresh() {
  if (document.hidden) {
    return;
  }
  try {
    const response = await fetch(LISTENING_URL, { cache: "no-cache" });
    if (!response.ok) {
      hide();
      return;
    }
    const data = await response.json();
    if (!data.track) {
      hide();
      return;
    }
    show(widgetSection(data));
  } catch {
    hide();
  }
}

document.addEventListener("visibilitychange", () => {
  if (!document.hidden) {
    refresh();
  }
});
setInterval(refresh, POLL_MS);
refresh();
