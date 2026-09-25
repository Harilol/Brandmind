# BrandMind

**Turn a rough idea into a launch-ready brand.**

BrandMind is an AI-powered brand intelligence system. A founder types a rough product idea — like *"an app that helps teachers track student progress"* — and BrandMind runs it through a 7-stage AI pipeline that produces a complete, launch-ready brand kit: audience analysis, positioning, personality, visual direction, launch copy, and more.

Built for the **WCC Launchpad 30 Hackathon**, sponsored by [Inkloom](https://inkloom.art).

---

## The problem

Founders often start with a single rough sentence. That sentence is not a brand. Turning it into one requires identifying the audience, sharpening the problem, choosing a position, defining personality, finding a name, picking visual direction, writing copy, and preparing a launch.

Most AI tools do this with **one prompt → one generic answer**. BrandMind does it with a **structured multi-agent workflow** where each stage builds on the previous one and a critic agent scores and rewrites weak output.

---

## How it works

BrandMind is a [LangGraph](https://github.com/langchain-ai/langgraph) pipeline of 7 specialized agents. Each agent produces a structured JSON output validated by Pydantic, and passes state forward to the next.

```
USER INPUT (rough idea + optional clarifications)
        │
        ▼
┌───────────────────────────────┐
│ 1. DISCOVER                   │  Understands the real problem, user, constraints
└───────────────────────────────┘
        │
        ▼
┌───────────────────────────────┐
│ 2. POSITION                   │  Category, differentiator, value prop
└───────────────────────────────┘
        │
        ▼
┌───────────────────────────────┐
│ 3. SHAPE                      │  Personality traits, naming directions, tagline
└───────────────────────────────┘
        │
        ▼
┌───────────────────────────────┐
│ 4. VISUALIZE                  │  Typography, colors, mood, symbols
└───────────────────────────────┘
        │
        ▼
┌───────────────────────────────┐
│ 5. CHALLENGE (critic)         │  Scores each stage 1-10, detects clichés
└───────────────────────────────┘
        │
        ├── score < 7?  → LOOP BACK to the weak stage with feedback
        │
        ▼
┌───────────────────────────────┐
│ 6. CONSISTENCY                │  Checks all pieces feel like ONE brand
└───────────────────────────────┘
        │
        ▼
┌───────────────────────────────┐
│ 7. DELIVER                    │  Landing headline + 3 social posts
└───────────────────────────────┘
        │
        ▼
   FINAL BRAND KIT
```

### What makes it different

**Staged reasoning, not one-shot generation.** Every agent builds on prior context.

**A real critic loop.** The Challenge agent scores every stage honestly. If any score falls below 7, the pipeline rewrites that stage with specific feedback and re-scores it. Max 2 revision rounds.

**Structured outputs everywhere.** Every agent returns validated JSON matching a Pydantic schema — no freeform paragraphs that break downstream stages.

**Streaming UI.** Results appear card-by-card as each agent finishes, so the user watches the pipeline think in real time.

**Consistency guardian.** A final agent checks that the personality, tagline, visuals, and copy all feel like the same brand.

---

## Tech stack

| Layer | Tech |
|---|---|
| Backend | Python 3.12, Django |
| AI orchestration | LangGraph, LangChain core |
| LLM | Groq (`openai/gpt-oss-20b`) — swappable to Gemini 2.5 Flash |
| Validation | Pydantic v2 |
| Frontend | Vanilla HTML/CSS/JS with Server-Sent Events |
| Deployment | Render (Gunicorn) |

---

## Project structure

```
brandmind/
├── myproject/           Django project (settings, urls, wsgi)
├── api/                 Django app (views, urls)
├── templates/           index.html
├── static/              style.css, app.js
├── agent.py             All 7 agents
├── graph.py             LangGraph wiring + routers
├── schemas.py           Pydantic schemas
├── state.py             Shared graph state
├── test_graph.py        CLI test that streams the full pipeline
├── requirements.txt
├── Procfile
└── manage.py
```

---

## Running locally

```bash
# Setup
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Add your Groq API key
echo "GROQ_API_KEY=your_key_here" > .env

# Run
python manage.py runserver
```

Open `http://127.0.0.1:8000/`, enter a rough idea, and watch the pipeline run.

### Testing the pipeline from CLI

```bash
python test_graph.py "an app that connects freelancers with clients"
```

Streams each agent's output live.

---

## Notes on the AI workflow

Each agent uses a short, direct prompt with strict JSON output and a Pydantic schema. The Challenge agent's prompt enforces an honest scoring rubric — it's told that generic taglines score 5/10, not 8/10.

When a revision is triggered, the weak agent's prompt receives the critic's feedback injected as `REVISION REQUESTED BY CRITIC:`, so it knows exactly what to fix.

The graph is built with `StateGraph(BrandState)` and two routers:
- `route_after_challenge` — decides loop back or continue
- `route_after_prep` — decides which stage to redo

`revision_count` caps loops at `max_revisions` (default 2) to prevent infinite cycles.

---

## Submission

Built for **WCC Launchpad 30 Hackathon** × Inkloom.

- **Live demo**: [link]
- **Demo video**: [link]
- **GitHub**: this repo

Inkloom early-access code: `INKLOOM-WCC`