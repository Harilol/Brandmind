import json
from django.shortcuts import render
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from graph import build_graph


# Which state field each graph node is responsible for producing.
# This lets us emit ONLY the new field on each stream tick, not the whole state.
NODE_TO_FIELD = {
    "discover": "discover",
    "position": "position",
    "shape": "shape",
    "visualize": "visual",
    "challenge": "challenge",
    "consistency": "consistency",
    "deliver": "launch",
}


def home(request):
    return render(request, "index.html")


def _sse(event_name, payload):
    """Format a Server-Sent Event."""
    return f"event: {event_name}\ndata: {json.dumps(payload)}\n\n"


@csrf_exempt
def run_pipeline(request):
    if request.method != "POST":
        return StreamingHttpResponse(
            _sse("error", {"error": "POST only"}),
            content_type="text/event-stream",
        )

    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return StreamingHttpResponse(
            _sse("error", {"error": "Invalid JSON"}),
            content_type="text/event-stream",
        )

    raw_idea = (body.get("raw_idea") or "").strip()
    clarifications = (body.get("user_clarifications") or "").strip()

    if not raw_idea:
        return StreamingHttpResponse(
            _sse("error", {"error": "raw_idea is required"}),
            content_type="text/event-stream",
        )

    def event_stream():
        graph = build_graph()
        initial = {
            "raw_idea": raw_idea,
            "user_clarifications": clarifications or "No additional clarifications.",
            "revision_count": 0,
            "max_revisions": 2,
        }

        try:
            for event in graph.stream(initial, stream_mode="updates"):
                for node_name, node_output in event.items():

                    # Special case: prep_revision signals a loop is starting
                    if node_name == "prep_revision":
                        yield _sse("stage", {"node": "prep_revision", "data": {}})
                        continue

                    # Which field is this node responsible for?
                    field = NODE_TO_FIELD.get(node_name)
                    if field is None:
                        continue

                    # Skip if the node didn't actually emit that field
                    if field not in node_output:
                        continue

                    val = node_output[field]
                    clean = {field: val.model_dump() if hasattr(val, "model_dump") else val}
                    yield _sse("stage", {"node": node_name, "data": clean})

            yield _sse("done", {"ok": True})

        except Exception as e:
            yield _sse("error", {"error": str(e)})

    response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
    response["Cache-Control"] = "no-cache"
    response["X-Accel-Buffering"] = "no"
    return response