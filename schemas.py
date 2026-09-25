from pydantic import BaseModel, Field
from typing import List, Optional


class DiscoverOutput(BaseModel):
    """Stage 1: Understand the idea."""
    core_problem: str = Field(description="The real problem the product solves")
    target_user: str = Field(description="Who this is actually for")
    context: str = Field(description="Setting/market this lives in")
    constraints: List[str] = Field(description="Limits or realities to respect")
    core_value: str = Field(description="The single most valuable thing offered")
    open_questions: List[str] = Field(
        description="Unclear things that should be clarified before branding"
    )


class PositionOutput(BaseModel):
    """Stage 2: Positioning."""
    category: str = Field(description="The market category this competes in")
    differentiator: str = Field(description="What makes it meaningfully different")
    value_proposition: str = Field(description="One-sentence value prop")
    competitive_angle: str = Field(description="Strategic angle vs alternatives")


class PersonalityTrait(BaseModel):
    trait: str = Field(description="The trait in 1-3 words")
    why: str = Field(description="Plain-English reason tied to the audience")


class NamingDirection(BaseModel):
    name: str
    rationale: str


class ShapeOutput(BaseModel):
    """Stage 3: Brand personality + naming + voice."""
    personality_traits: List[PersonalityTrait] = Field(
        description="3-5 traits, each with a plain-English justification"
    )
    traits_to_avoid: List[PersonalityTrait] = Field(
        description="Traits that would feel wrong for this audience"
    )
    naming_directions: List[NamingDirection] = Field(
        description="3 naming territories with reasoning"
    )
    tagline: str
    one_line_pitch: str


class VisualOutput(BaseModel):
    """Stage 4: Visual direction."""
    typography_direction: str
    color_mood: str
    composition_notes: str
    symbols_or_motifs: List[str]
    imagery_style: str
    concepts_to_avoid: List[str]

class ChallengeOutput(BaseModel):
    """Stage 5: Critic agent."""
    cliches_detected: List[str]
    contradictions: List[str]
    audience_mismatch: List[str]
    scores: dict
    overall_score: float = Field(ge=1, le=10)
    revision_needed: bool
    revision_target: Optional[str] = Field(
        default=None,
        description="Which stage to redo if revision_needed is True"
    )
    revision_instructions: Optional[str] = Field(
        default=None,
        description="Specific, actionable guidance for the agent being asked to revise"
    )


class ConsistencyOutput(BaseModel):
    """Stage 6: Consistency guardian."""
    is_consistent: bool
    conflicts: List[str]
    suggested_fixes: List[str]


class LaunchOutput(BaseModel):
    """Stage 7: Launch assets."""
    landing_headline: str
    subheadline: str
    social_posts: List[str] = Field(description="3 launch posts")