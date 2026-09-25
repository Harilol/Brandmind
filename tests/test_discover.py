# from state import BrandState
from agent import position_agent

# state: BrandState = {
#     "raw_idea": "I want an app that helps teachers to track students progess individually but since there are 100's of students in class its easy to get lost and forget hwo a student is performing and who needs more attention in studoies like that",
#     "revision_count": 0,
#     "max_revisions": 2,
# }

# result = discover_agent(state)
# d = result["discover"]

# print("CORE PROBLEM:", d.core_problem)
# print("TARGET USER:", d.target_user)
# print("CONTEXT:", d.context)
# print("CONSTRAINTS:", d.constraints)
# print("CORE VALUE:", d.core_value)
# print("OPEN QUESTIONS:", d.open_questions)


# import sys
# from state import BrandState
# from agent import discover_agent, position_agent

# idea = sys.argv[1] if len(sys.argv) > 1 else "I want an app that helps students find teammates"

# state: BrandState = {
#     "raw_idea": idea,
#     "user_clarifications": "Undergrads only. Free tier with paid upgrade. Mobile-first.",
#     "revision_count": 0,
#     "max_revisions": 2,
# }

# state = discover_agent(state)
# print("=== DISCOVER ===")
# print("Core value:", state["discover"].core_value)

# state = position_agent(state)
# p = state["position"]
# print("\n=== POSITION ===")
# print("CATEGORY:", p.category)
# print("DIFFERENTIATOR:", p.differentiator)
# print("VALUE PROP:", p.value_proposition)
# print("COMPETITIVE ANGLE:", p.competitive_angle)

# import sys
# from state import BrandState
# from agent import discover_agent, position_agent, shape_agent

# idea = sys.argv[1] if len(sys.argv) > 1 else "I want an app that helps students find teammates"

# state: BrandState = {
#     "raw_idea": idea,
#     "user_clarifications": "Undergrads only. Free tier with paid upgrade. Mobile-first.",
#     "revision_count": 0,
#     "max_revisions": 2,
# }

# state = discover_agent(state)
# state = position_agent(state)
# state = shape_agent(state)

# s = state["shape"]
# print("=== SHAPE ===\n")

# print("PERSONALITY TRAITS:")
# for t in s.personality_traits:
#     print(f"  • {t.trait} — {t.why}")

# print("\nTRAITS TO AVOID:")
# for t in s.traits_to_avoid:
#     print(f"  • {t.trait} — {t.why}")

# print("\nNAMING DIRECTIONS:")
# for n in s.naming_directions:
#     print(f"  • {n.name}: {n.rationale}")

# print("\nTAGLINE:", s.tagline)
# print("PITCH:", s.one_line_pitch)


# import sys
# from state import BrandState
# from agent import discover_agent, position_agent, shape_agent, visualize_agent

# idea = sys.argv[1] if len(sys.argv) > 1 else "I want an app that helps teachers to track students progess individually but since there are 100's of students in class its easy to get lost and forget hwo a student is performing and who needs more attention in studoies like that"

# state: BrandState = {
#     "raw_idea": idea,
#     "user_clarifications": "Undergrads only. Free tier with paid upgrade. Mobile-first.",
#     "revision_count": 0,
#     "max_revisions": 2,
# }

# state = discover_agent(state)
# state = position_agent(state)
# state = shape_agent(state)
# state = visualize_agent(state)

# v = state["visual"]
# print("=== VISUAL DIRECTION ===\n")
# print("TYPOGRAPHY:", v.typography_direction)
# print("\nCOLOR MOOD:", v.color_mood)
# print("\nCOMPOSITION:", v.composition_notes)
# print("\nSYMBOLS/MOTIFS:")
# for m in v.symbols_or_motifs:
#     print(f"  • {m}")
# print("\nIMAGERY STYLE:", v.imagery_style)
# print("\nCONCEPTS TO AVOID:")
# for c in v.concepts_to_avoid:
#     print(f"  • {c}")







# import sys
# from state import BrandState
# from agent import (
#     discover_agent, position_agent, shape_agent,
#     visualize_agent, challenge_agent,
# )

# idea = sys.argv[1] if len(sys.argv) > 1 else "I want to create an app that helps students find teammates"

# state: BrandState = {
#     "raw_idea": idea,
#     "user_clarifications": "Undergrads only. Free tier. Mobile-first.",
#     "revision_count": 0,
#     "max_revisions": 2,
# }

# print(">>> STAGE 1: Discover")
# state = discover_agent(state)

# print(">>> STAGE 2: Position")
# state = position_agent(state)

# print(">>> STAGE 3: Shape")
# state = shape_agent(state)

# print(">>> STAGE 4: Visualize")
# state = visualize_agent(state)

# # --- LOOP ---
# MAX = state["max_revisions"]
# for attempt in range(MAX + 1):
#     print(f"\n>>> STAGE 5: Challenge (attempt {attempt + 1})")
#     state = challenge_agent(state)
#     ch = state["challenge"]

#     print(f"    Scores: {ch.scores}")
#     print(f"    Overall: {ch.overall_score}/10")
#     print(f"    Revision needed? {ch.revision_needed}")
#     print(f"    Target: {ch.revision_target}")

#     if not ch.revision_needed:
#         print("    ✅ Passed critique. Moving on.")
#         break

#     print(f"    ❌ Sending back to: {ch.revision_target}")
#     instructions = ch.revision_instructions or "(no specific instructions provided)"
#     print(f"    Target: {ch.revision_target}")
#     print(f"    Instructions: {ch.revision_instructions}")

#     if ch.revision_target in ("shape", "tagline"):
#         state = shape_agent(state)
#         state = visualize_agent(state)  # re-run visualize too since shape changed
#     elif ch.revision_target == "visual":
#         state = visualize_agent(state)
#     elif ch.revision_target == "position":
#         state = position_agent(state)
#         state = shape_agent(state)
#         state = visualize_agent(state)

#     state["revision_count"] += 1

# print("\n=== FINAL TAGLINE ===")
# print(state["shape"].tagline)


# import sys
# from state import BrandState
# from agent import (
#     discover_agent, position_agent, shape_agent,
#     visualize_agent, challenge_agent, consistency_agent,
# )

# idea = sys.argv[1] if len(sys.argv) > 1 else "I want an app that helps teachers track student progress"

# state: BrandState = {
#     "raw_idea": idea,
#     "user_clarifications": "Undergrads only. Free tier. Mobile-first.",
#     "revision_count": 0,
#     "max_revisions": 2,
# }

# state = discover_agent(state)
# state = position_agent(state)
# state = shape_agent(state)
# state = visualize_agent(state)

# # Loop
# for attempt in range(state["max_revisions"] + 1):
#     state = challenge_agent(state)
#     ch = state["challenge"]
#     print(f"[Challenge attempt {attempt+1}] overall={ch.overall_score}, needs_revision={ch.revision_needed}")
#     if not ch.revision_needed:
#         break
#     if ch.revision_target in ("shape", "tagline"):
#         state = shape_agent(state)
#         state = visualize_agent(state)
#     elif ch.revision_target == "visual":
#         state = visualize_agent(state)
#     elif ch.revision_target == "position":
#         state = position_agent(state)
#         state = shape_agent(state)
#         state = visualize_agent(state)
#     state["revision_count"] += 1

# # Consistency check
# state = consistency_agent(state)
# c = state["consistency"]
# print("\n=== CONSISTENCY ===")
# print("Consistent?", c.is_consistent)
# print("\nCONFLICTS:")
# for x in c.conflicts or ["(none)"]:
#     print(f"  • {x}")
# print("\nSUGGESTED FIXES:")
# for x in c.suggested_fixes or ["(none)"]:
#     print(f"  • {x}")


import sys
from state import BrandState
from agent import (
    discover_agent, position_agent, shape_agent,
    visualize_agent, challenge_agent, consistency_agent,
    deliver_agent,
)

idea = sys.argv[1] if len(sys.argv) > 1 else "I want an app that helps teachers track student progress"

state: BrandState = {
    "raw_idea": idea,
    "user_clarifications": "Undergrads only. Free tier. Mobile-first.",
    "revision_count": 0,
    "max_revisions": 2,
}

state = discover_agent(state)
state = position_agent(state)
state = shape_agent(state)
state = visualize_agent(state)

for attempt in range(state["max_revisions"] + 1):
    state = challenge_agent(state)
    ch = state["challenge"]
    print(f"[Challenge {attempt+1}] overall={ch.overall_score}, needs_revision={ch.revision_needed}")
    if not ch.revision_needed:
        break
    if ch.revision_target in ("shape", "tagline"):
        state = shape_agent(state); state = visualize_agent(state)
    elif ch.revision_target == "visual":
        state = visualize_agent(state)
    elif ch.revision_target == "position":
        state = position_agent(state); state = shape_agent(state); state = visualize_agent(state)
    state["revision_count"] += 1

state = consistency_agent(state)
state = deliver_agent(state)

l = state["launch"]
print("\n=== LAUNCH ASSETS ===\n")
print("HEADLINE:", l.landing_headline)
print("SUBHEADLINE:", l.subheadline)
print("\nSOCIAL POSTS:")
for i, post in enumerate(l.social_posts, 1):
    print(f"\n  {i}. {post}")