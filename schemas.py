from typing import List, Optional, TypedDict, Annotated
from pydantic import BaseModel, Field
import operator

class UserContext(BaseModel):
    dilemma_statement: str = Field(description="The primary question or decision the user is facing")
    background_context: str = Field(description="Relevant history, values, or non-financial constraints")
    proposed_options: List[str] = Field(description="Candidate choices")
    liquid_savings: Optional[float] = Field(default=None)
    monthly_expenses: Optional[float] = Field(default=None)
    current_income: Optional[float] = Field(default=None)

class AgentPosition(BaseModel):
    agent_name: str = Field(description="Name/role of the agent")
    preferred_option_index: int = Field(description="Index of preferred choice from proposed_options")
    confidence_score: float = Field(ge=0.0, le=1.0, description="Confidence in choice (0.0 to 1.0)")
    core_argument: str = Field(description="Main reasoning supporting this choice")
    key_metrics: List[str] = Field(description="Supporting numbers, calculations, or metrics")
    sources: List[str] = Field(default_factory=list, description="URLs or citation sources backing up the argument")

class Rebuttal(BaseModel):
    round_number: int = Field(description="Current debate round")
    agent_name: str = Field(description="Agent making the rebuttal")
    target_agent: str = Field(description="Agent being challenged")
    points_challenged: str = Field(description="Specific point or argument being criticized")
    concession: Optional[str] = Field(default=None, description="Acknowledgment of valid points")
    revised_option_index: int = Field(description="Preferred option index after rebuttal")
    revised_confidence_score: float = Field(ge=0.0, le=1.0, description="Updated confidence score")
    sources: List[str] = Field(default_factory=list, description="URLs or citation sources backing up the rebuttal")

class DecisionMatrix(BaseModel):
    recommended_option: str = Field(description="The final synthesized recommendation")
    consensus_score: float = Field(ge=0.0, le=1.0, description="Calculated agreement level")
    key_trade_offs: List[str] = Field(description="Main trade-offs acknowledged across positions")
    dissenting_views: List[str] = Field(description="Remaining unresolvable disagreements")
    action_plan_30_days: List[str] = Field(description="Concrete immediate steps")
    sources: List[str] = Field(default_factory=list, description="Referenced URLs and benchmark sources")

class CouncilState(TypedDict):
    user_context: UserContext
    positions: Annotated[List[AgentPosition], operator.add]
    rebuttals: Annotated[List[Rebuttal], operator.add]
    revision_count: int
    final_matrix: Optional[DecisionMatrix]