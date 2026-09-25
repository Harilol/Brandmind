const STAGES = ["discover", "position", "shape", "visual", "challenge", "consistency", "launch"];
const rendered = {};   // { stageName: DOMElement }

document.getElementById("run-btn").addEventListener("click", runPipeline);

async function runPipeline() {
  const btn = document.getElementById("run-btn");
  btn.disabled = true;
  btn.textContent = "Running...";

  document.getElementById("stages").innerHTML = `
    <div class="stage" id="working">
      <div class="stage-label">Working</div>
      <h2>Running all 7 agents…</h2>
      <p>Each stage will appear below as it finishes.</p>
    </div>`;

  Object.keys(rendered).forEach(k => delete rendered[k]);

  const idea = document.getElementById("idea").value.trim();
  const clarifications = document.getElementById("clarifications").value.trim();

  if (!idea) {
    alert("Please enter an idea first.");
    btn.disabled = false;
    btn.textContent = "Run BrandMind →";
    document.getElementById("stages").innerHTML = "";
    return;
  }

 let firstCardArrived = false;
 let revisionRound = 0;
 const data = {};        // <-- accumulate stage output here

  try {
    const res = await fetch("/run/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ raw_idea: idea, user_clarifications: clarifications }),
    });

    if (!res.ok || !res.body) throw new Error(`Server error ${res.status}`);

    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });

      const parts = buffer.split("\n\n");
      buffer = parts.pop() || "";

      for (const part of parts) {
        const lines = part.split("\n");
        let eventName = "message";
        let payload = "";
        for (const line of lines) {
          if (line.startsWith("event: ")) eventName = line.slice(7).trim();
          else if (line.startsWith("data: ")) payload += line.slice(6);
        }
        if (!payload) continue;

        let parsed;
        try { parsed = JSON.parse(payload); } catch { continue; }

        if (eventName === "stage") {
          const { node, data: nodeData } = parsed;

          // Special case: prep_revision means the loop is firing
        if (node === "prep_revision") {
        revisionRound++;

        // Remove the "Working..." placeholder if still there
        const w = document.getElementById("working");
        if (w) w.remove();

        // Remove any previous revision banners so they don't stack
        document.querySelectorAll(".stage-revision").forEach(el => el.remove());

        // Look at the challenge object we already rendered to know what's being fixed
        const ch = data.challenge || {};
        const target = ch.revision_target || "weak sections";
        const score = ch.overall_score || "?";

        const el = document.createElement("div");
        el.className = "stage stage-revision";
        el.innerHTML = `
            <div class="stage-label">🔄 Revision Round ${revisionRound}</div>
            <h2>Rewriting the ${target}</h2>
            <p>The critic scored your brand ${score}/10 and flagged the <strong>${target}</strong> as too weak. Re-running that stage with feedback…</p>
        `;
        document.getElementById("stages").appendChild(el);
        continue;
        }

        if (!firstCardArrived) {
          const w = document.getElementById("working");
          if (w) w.remove();
          firstCardArrived = true;
          // Scroll to top of results so user sees the first card
          document.getElementById("stages").scrollIntoView({ behavior: "smooth", block: "start" });
        }

          for (const [stageKey, stageValue] of Object.entries(nodeData)) {
            if (!STAGES.includes(stageKey)) continue;
            if (stageKey === "consistency" && stageValue?.is_consistent) continue;


            data[stageKey] = stageValue;

            
            // If this stage was already rendered, remove the old card (loop replaced it)
            if (rendered[stageKey]) {
              rendered[stageKey].remove();
            }

            const el = renderStage(stageKey, stageValue);
            rendered[stageKey] = el;
          }
        } else if (eventName === "error") {
          document.getElementById("stages").innerHTML += `
            <div class="stage"><div class="stage-label">Error</div><h2>Something broke</h2><p>${parsed.error}</p></div>`;
        }
      }
    }
  } catch (e) {
    document.getElementById("stages").innerHTML += `
      <div class="stage"><div class="stage-label">Error</div><h2>Something broke</h2><p>${e.message}</p></div>`;
  }

  btn.disabled = false;
  btn.textContent = "Run BrandMind →";
}


// --- Renderers ---

function renderStage(stageName, data) {
  if (!data) return null;
  const container = document.getElementById("stages");
  const el = document.createElement("div");
  el.className = "stage";

  if (stageName === "discover") {
    el.innerHTML = `
      <div class="stage-label">Stage 1 · Understanding</div>
      <h2>What we understood</h2>
      <div class="row"><div class="row-label">The real problem</div><div class="row-value">${data.core_problem}</div></div>
      <div class="row"><div class="row-label">Who it's for</div><div class="row-value">${data.target_user}</div></div>
      <div class="row"><div class="row-label">Value</div><div class="row-value">${data.core_value}</div></div>
    `;
  } else if (stageName === "position") {
    el.innerHTML = `
      <div class="stage-label">Stage 2 · Positioning</div>
      <h2>How it stands out</h2>
      <div class="row"><div class="row-label">Category</div><div class="row-value">${data.category}</div></div>
      <div class="row"><div class="row-label">Differentiator</div><div class="row-value">${data.differentiator}</div></div>
      <div class="row"><div class="row-label">One-liner</div><div class="row-value">${data.value_proposition}</div></div>
    `;
  } else if (stageName === "shape") {
    const good = (data.personality_traits || []).map(t => `<span class="tag tag-good">${t.trait}</span>`).join("");
    const bad = (data.traits_to_avoid || []).map(t => `<span class="tag tag-bad">${t.trait}</span>`).join("");
    const names = (data.naming_directions || []).map(n =>
      `<div class="row"><div class="row-value"><strong>${n.name}</strong> — ${n.rationale}</div></div>`).join("");
    el.innerHTML = `
      <div class="stage-label">Stage 3 · Brand personality</div>
      <h2>How the brand feels</h2>
      <div class="row"><div class="row-label">Traits</div>${good}</div>
      <div class="row"><div class="row-label">Avoid</div>${bad}</div>
      <div class="row"><div class="row-label">Tagline</div><div class="tagline">"${data.tagline}"</div></div>
      <div class="row"><div class="row-label">Naming directions</div>${names}</div>
    `;
  } else if (stageName === "visual") {
    const hexes = ((data.color_mood || "").match(/#[0-9A-Fa-f]{6}/g) || []);
    const swatches = hexes.map(h => `<span class="color-swatch" style="background:${h}" title="${h}"></span>`).join("");
    el.innerHTML = `
      <div class="stage-label">Stage 4 · Visual direction</div>
      <h2>How it looks</h2>
      <div class="row"><div class="row-label">Colors</div><div>${swatches}<span class="row-value">${hexes.join(" · ")}</span></div></div>
      <div class="row"><div class="row-label">Typography</div><div class="row-value">${data.typography_direction}</div></div>
      <div class="row"><div class="row-label">Avoid</div><div class="row-value">${(data.concepts_to_avoid || []).join(" · ")}</div></div>
    `;
  } else if (stageName === "challenge") {
    const score = data.overall_score;
    const scoreClass = score >= 7 ? "score-good" : "score-mid";
    const cliches = (data.cliches_detected || []).map(c => `<span class="tag tag-bad">${c}</span>`).join("");
    const willLoop = data.revision_needed
      ? `<div class="row"><div class="row-label">Decision</div><div class="row-value">🔄 Weak sections detected — sending back for revision.</div></div>`
      : `<div class="row"><div class="row-label">Decision</div><div class="row-value">✅ Passed. Moving to launch.</div></div>`;
    el.innerHTML = `
      <div class="stage-label">Stage 5 · Self-critique</div>
      <h2>What our AI critic caught</h2>
      <div class="row"><div class="row-label">Overall score</div><span class="score-badge ${scoreClass}">${score}/10</span></div>
      <div class="row"><div class="row-label">Clichés detected</div>${cliches || "<em>none</em>"}</div>
      ${willLoop}
    `;
  } else if (stageName === "consistency") {
    const conflicts = (data.conflicts || []).map(c => `<div class="row"><div class="row-value">• ${c}</div></div>`).join("");
    el.innerHTML = `
      <div class="stage-label">Stage 6 · Consistency check</div>
      <h2>Does it all fit together?</h2>
      <div class="row"><div class="row-label">Consistent?</div><div class="row-value">${data.is_consistent ? "Yes" : "No"}</div></div>
      ${conflicts}
    `;
  } else if (stageName === "launch") {
    const posts = (data.social_posts || []).map(p => `<div class="post">${p}</div>`).join("");
    el.innerHTML = `
      <div class="stage-label">Stage 7 · Launch kit</div>
      <h2>Ready to launch</h2>
      <div class="row"><div class="row-label">Headline</div><div class="tagline">${data.landing_headline}</div></div>
      <div class="row"><div class="row-label">Subheadline</div><div class="row-value">${data.subheadline}</div></div>
      <div class="row"><div class="row-label">Social posts</div>${posts}</div>
    `;
  }

  container.appendChild(el);
  return el;
}