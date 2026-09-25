from state import BrandState
from schemas import DiscoverOutput

# Start with just the raw idea (like the graph does)
state: BrandState = {
    "raw_idea": "I want an app that helps students find teammates",
    "revision_count": 0,
    "max_revisions": 2,
}

print("Initial keys:", list(state.keys()))
print("Discover filled?", state.get("discover"))

# Simulate Agent 1 running and writing into state
state["discover"] = DiscoverOutput(
    core_problem="Students struggle to find compatible project teammates",
    target_user="University CS students",
    context="Academic group projects",
    constraints=["No budget", "Mobile-first"],
    core_value="Better-matched team formation",
    open_questions=["Undergrads only?"]
)

print("\nAfter Discover runs:")
print("Discover filled?", state["discover"].core_problem)
print("Position filled?", state.get("position"))