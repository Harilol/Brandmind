import os
import json
from dotenv import load_dotenv
from groq import Groq
from schemas import DiscoverOutput, PositionOutput, ShapeOutput, VisualOutput, ChallengeOutput, ConsistencyOutput, LaunchOutput
from state import BrandState

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def call_llm(prompt: str) -> str:
    """
    Single helper. Every agent uses this.
    Swap Groq → Gemini later by editing ONLY this function.
    """
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        response_format={"type": "json_object"},   # Groq supports forced JSON mode
    )
    return response.choices[0].message.content


def discover_agent(state: BrandState) -> BrandState:
    """Agent 1: understand the idea."""
    raw_idea = state["raw_idea"]

    prompt = f"""
You are a brand strategist. A founder gave you this rough idea:

"{raw_idea}"

Understand the REAL problem behind it, not the surface feature.

Return JSON with this exact shape:
{{
  "core_problem": "the real problem, 2-3 sentences",
  "target_user": "who this is really for, 2-3 sentences",
  "context": "setting and market, 2-3 sentences",
  "constraints": ["3-5 realistic limits"],
  "core_value": "what the user actually gains, 2-3 sentences",
  "open_questions": ["3-5 real uncertainties"]
}}

Write in plain English like you're explaining to a friend. No buzzwords.
Be specific. "Students" is bad. "University CS undergrads on group projects" is good.
Return JSON only. No markdown, no explanation.
"""

    raw_response = call_llm(prompt)
    data = json.loads(raw_response)
    discover_output = DiscoverOutput(**data)

    state["discover"] = discover_output
    return state


def position_agent(state: BrandState) -> BrandState:
    """Agent 2: positioning. Handles revisions."""
    d = state["discover"]
    clarifications = state.get("user_clarifications", "No additional clarifications provided.")

    revision_notes = ""
    ch = state.get("challenge")
    if ch and ch.revision_target == "position" and ch.revision_instructions:
        revision_notes = f"""

REVISION REQUESTED BY CRITIC:
{ch.revision_instructions}

Avoid these cliches: {ch.cliches_detected}
"""

    prompt = f"""
You are a positioning strategist.

PROBLEM: {d.core_problem}
USER: {d.target_user}
VALUE: {d.core_value}
FOUNDER'S NOTES: {clarifications}

Define how this product should be positioned.

Return JSON:
{{
  "category": "the market category, 1 sentence",
  "differentiator": "what's meaningfully different, 2-3 sentences",
  "value_proposition": "one sentence a founder would say out loud",
  "competitive_angle": "how it wins vs alternatives, 2-3 sentences"
}}

Plain English. No buzzwords. Be specific. JSON only.
"""

    raw_response = call_llm(prompt)
    data = json.loads(raw_response)
    state["position"] = PositionOutput(**data)
    return state



def shape_agent(state: BrandState) -> BrandState:
    """Agent 3: personality, naming, voice, tagline. Handles revisions."""
    d = state["discover"]
    p = state["position"]
    clarifications = state.get("user_clarifications", "No additional clarifications provided.")

    # Revision handling: if the critic asked for a tagline/shape revision, include it
    revision_notes = ""
    ch = state.get("challenge")
    if ch and ch.revision_target in ("shape", "tagline") and ch.revision_instructions:
        revision_notes = f"""

REVISION REQUESTED BY CRITIC:
Previous attempt was rejected. Here is the feedback:
{ch.revision_instructions}

Also avoid these cliches that were flagged:
{ch.cliches_detected}

You MUST fix these specific issues this time.
"""

    prompt = f"""
You are a brand strategist.

USER: {d.target_user}
CATEGORY: {p.category}
DIFFERENTIATOR: {p.differentiator}
FOUNDER'S NOTES: {clarifications}
{revision_notes}

Build the brand's personality, names, and voice.

Return JSON:
{{
  "personality_traits": [
    {{"trait": "1-3 words", "why": "1 short sentence tied to the audience"}}
  ],
  "traits_to_avoid": [
    {{"trait": "1-3 words", "why": "1 short sentence"}}
  ],
  "naming_directions": [
    {{"name": "Name", "rationale": "1 short sentence"}}
  ],
  "tagline": "short, specific, no time words like 'minutes'",
  "one_line_pitch": "one sentence a founder could say out loud"
}}

Give 3-5 traits, 2-3 avoid, 3 names (one descriptive, one invented, one metaphorical).
Plain English. No buzzwords. JSON only.
"""
    raw_response = call_llm(prompt)
    data = json.loads(raw_response)
    state["shape"] = ShapeOutput(**data)
    return state




def visualize_agent(state: BrandState) -> BrandState:
    """Agent 4: visual direction as text. Handles revisions."""
    d = state["discover"]
    p = state["position"]
    s = state["shape"]

    revision_notes = ""
    ch = state.get("challenge")
    if ch and ch.revision_target == "visual" and ch.revision_instructions:
        revision_notes = f"""

REVISION REQUESTED BY CRITIC:
Previous visual direction was rejected. Feedback:
{ch.revision_instructions}
"""

    prompt = f"""
You are a brand designer.

USER: {d.target_user}
PERSONALITY: {[t.trait for t in s.personality_traits]}
TAGLINE: {s.tagline}
{revision_notes}

Describe a visual direction. Do NOT generate images.

Return JSON:
{{
  "typography_direction": "font style + why, 1-2 sentences",
  "color_mood": "palette feeling + 2-3 hex codes, 2-3 sentences",
  "composition_notes": "how layouts should feel, 1-2 sentences",
  "symbols_or_motifs": ["3-4 concrete visual ideas"],
  "imagery_style": "what to use and avoid, 1-2 sentences",
  "concepts_to_avoid": ["3-5 specific clichés and why"]
}}

Plain English. Real hex codes. JSON only.
"""

    raw_response = call_llm(prompt)
    data = json.loads(raw_response)
    state["visual"] = VisualOutput(**data)
    return state



def challenge_agent(state: BrandState) -> BrandState:
    """Agent 5: critic. Scores everything, decides if revision is needed."""
    d = state["discover"]
    p = state["position"]
    s = state["shape"]
    v = state["visual"]

    prompt = f"""
You are a tough brand critic. Find weaknesses, cliches, contradictions.

DISCOVER: {d.core_problem} | {d.target_user}
POSITION: {p.category} | {p.differentiator}
SHAPE tagline: {s.tagline}
SHAPE traits: {[t.trait for t in s.personality_traits]}
VISUAL: {v.color_mood}

Score each stage 1-10. Be honest. A generic tagline is a 5, not an 8.

Return JSON with EXACTLY these top-level keys:
{{
  "cliches_detected": ["specific cliches found"],
  "contradictions": ["places where the brand clashes with itself"],
  "audience_mismatch": ["places where tone doesn't fit the user"],
  "scores": {{"positioning": 7, "personality": 7, "tagline": 7, "visual": 7}},
  "overall_score": 7,
  "revision_needed": false,
  "revision_target": null,
  "revision_instructions": null
}}

CRITICAL RULES:
- "scores" contains ONLY the four numbers. Nothing else inside it.
- "revision_instructions" is TOP-LEVEL, not inside scores.
- If revision_needed is true, revision_instructions MUST be specific and non-null.
- revision_target = weakest stage (position / shape / tagline / visual).
- Only these TOP-LEVEL keys. No extras.

JSON only.
REVISION LOGIC (mandatory):
- If ANY score is < 7, revision_needed MUST be true.
- If revision_needed is true, revision_target MUST be the lowest-scoring stage.
- If revision_needed is true, revision_instructions MUST be a specific string (not null).
"""

    raw_response = call_llm(prompt)
    data = json.loads(raw_response)
    state["challenge"] = ChallengeOutput(**data)
    return state


def consistency_agent(state: BrandState) -> BrandState:
    """Agent 6: check everything feels like one brand."""
    d = state["discover"]
    p = state["position"]
    s = state["shape"]
    v = state["visual"]

    prompt = f"""
You are a brand consistency checker. Ask: "Do all these pieces feel like ONE brand?"

USER: {d.target_user}
POSITION: {p.category} | {p.value_proposition}
PERSONALITY: {[t.trait for t in s.personality_traits]}
TAGLINE: {s.tagline}
VISUAL: {v.color_mood} | {v.typography_direction}

Return JSON:
{{
  "is_consistent": true,
  "conflicts": ["only real conflicts; name the two things that clash"],
  "suggested_fixes": ["one fix per conflict"]
}}

Only flag REAL conflicts. If everything fits, is_consistent = true and lists are empty.
Plain English. JSON only.
"""

    raw_response = call_llm(prompt)
    data = json.loads(raw_response)
    state["consistency"] = ConsistencyOutput(**data)
    return state




def deliver_agent(state: BrandState) -> BrandState:
    """Agent 7: launch assets."""
    d = state["discover"]
    p = state["position"]
    s = state["shape"]

    ch = state.get("challenge")
    banned = []
    if ch and ch.cliches_detected:
        banned = ch.cliches_detected

    ban_list = ", ".join(banned) if banned else "none flagged by critic"

    ch = state.get("challenge")
    banned = ch.cliches_detected if ch and ch.cliches_detected else []

    prompt = f"""
Write launch copy for this brand.

USER: {d.target_user}
VALUE: {p.value_proposition}
TAGLINE: {s.tagline}

Avoid these words: {banned + ["seamless", "empower", "unlock", "next-level", "data-driven", "in minutes"]}

Return ONLY this JSON object, no other text:
{{
  "landing_headline": "short headline, no time words",
  "subheadline": "one supporting sentence",
  "social_posts": ["post 1", "post 2", "post 3"]
}}

Each post is 2-3 sentences. Different angle for each. Sound human. JSON only.
"""

    raw_response = call_llm(prompt)
    data = json.loads(raw_response)
    state["launch"] = LaunchOutput(**data)
    return state