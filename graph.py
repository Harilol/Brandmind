from langgraph.graph import StateGraph, END
from state import BrandState
import time
from agent import (
    discover_agent,
    position_agent,
    shape_agent,
    visualize_agent,
    challenge_agent,
    consistency_agent,
    deliver_agent,
)

def with_throttle(fn, seconds=2):
    def wrapped(state):
        time.sleep(seconds)
        return fn(state)
    return wrapped


def route_after_challenge(state: BrandState) -> str:
    """Where to go after challenge: loop back or move on."""
    ch = state["challenge"]

    if not ch.revision_needed:
        return "consistency"

    if state.get("revision_count", 0) >= state.get("max_revisions", 2):
        return "consistency"

    return "prep_revision"


def bump_revision(state: BrandState) -> BrandState:
    """Increment revision count when we loop back."""
    state["revision_count"] = state.get("revision_count", 0) + 1
    return state


def route_after_prep(state: BrandState) -> str:
    """prep_revision decides which stage to redo."""
    target = state["challenge"].revision_target or "shape"
    if target in ("shape", "tagline"):
        return "shape"
    if target == "visual":
        return "visualize"     # <-- return the NODE name
    if target == "position":
        return "position"
    return "shape"

def build_graph():
    g = StateGraph(BrandState)

    g.add_node("discover",    with_throttle(discover_agent))
    g.add_node("position",    with_throttle(position_agent))
    g.add_node("shape",       with_throttle(shape_agent))
    g.add_node("visualize",   with_throttle(visualize_agent))
    g.add_node("challenge",   with_throttle(challenge_agent))
    g.add_node("consistency", with_throttle(consistency_agent))
    g.add_node("deliver",     with_throttle(deliver_agent))
    g.add_node("prep_revision", bump_revision)   # no throttle, no LLM

    g.set_entry_point("discover")

    # Linear flow
    g.add_edge("discover", "position")
    g.add_edge("position", "shape")
    g.add_edge("shape", "visualize")
    g.add_edge("visualize", "challenge")

    # After challenge: either loop back via prep_revision, or move to consistency
    g.add_conditional_edges(
        "challenge",
        route_after_challenge,
        {
            "prep_revision": "prep_revision",
            "consistency": "consistency",
        },
    )

    # After prep_revision: choose which stage to redo
    g.add_conditional_edges(
        "prep_revision",
        route_after_prep,
        {
            "position": "position",
            "shape": "shape",
            "visualize": "visualize",
        },
    )

    # After consistency: deliver and end
    g.add_edge("consistency", "deliver")
    g.add_edge("deliver", END)

    return g.compile()