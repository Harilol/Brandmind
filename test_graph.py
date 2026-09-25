import sys
import json
from graph import build_graph

idea = sys.argv[1] if len(sys.argv) > 1 else "an app that connects freelancers with clients"

graph = build_graph()

initial = {
    "raw_idea": idea,
    "user_clarifications": "Keep it simple.",
    "revision_count": 0,
    "max_revisions": 2,
}

for event in graph.stream(initial, stream_mode="updates"):
    for node_name, node_output in event.items():
        print(f"\n{'=' * 60}")
        print(f"  NODE: {node_name}")
        print('=' * 60)
        # Only print the field that node just added
        for key, value in node_output.items():
            if hasattr(value, "model_dump"):
                print(f"--- {key} ---")
                print(json.dumps(value.model_dump(), indent=2))
            elif key not in ("raw_idea", "user_clarifications", "revision_count", "max_revisions"):
                print(f"--- {key} ---")
                print(value)