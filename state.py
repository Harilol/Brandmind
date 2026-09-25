from typing import TypedDict, Optional
from schemas import (
    DiscoverOutput,
    PositionOutput,
    ShapeOutput,
    VisualOutput,
    ChallengeOutput,
    ConsistencyOutput,
    LaunchOutput,
)


class BrandState(TypedDict, total=False):
    # --- INPUT ---
    raw_idea: str                    # what user typed initially
    user_clarifications: str         # user's answers to Discover's follow-ups

    # --- STAGE OUTPUTS (filled by agents, in order) ---
    discover: Optional[DiscoverOutput]
    position: Optional[PositionOutput]
    shape: Optional[ShapeOutput]
    visual: Optional[VisualOutput]
    challenge: Optional[ChallengeOutput]
    consistency: Optional[ConsistencyOutput]
    launch: Optional[LaunchOutput]

    # --- LOOP CONTROL ---
    revision_count: int              # how many times we've looped back
    max_revisions: int               # cap it (e.g. 2)