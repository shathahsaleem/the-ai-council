class UserContext(BaseModel):
    dilemma_statement: str = Field(description="The primary question or decision the user is facing")
    background_context: str = Field(description="Relevant history, values, or non-financial constraints")
    proposed_options: List[str] = Field(description="Dynamic candidate choices extracted or proposed during intake")
    
    # Optional fields for grounding tools when quantitative data is present
    liquid_savings: Optional[float] = Field(default=None, description="Available liquid cash balance")
    monthly_expenses: Optional[float] = Field(default=None, description="Essential monthly burn rate")
    current_income: Optional[float] = Field(default=None, description="Current monthly income")


class AgentPosition(BaseModel):
    agent_name: str = Field(description="Name/role of the agent (e.g., Risk Analyst)")
    preferred_option_index: int = Field(description="Index of the preferred choice from proposed_options")
    confidence_score: float = Field(ge=0.0, le=1.0, description="Confidence in this choice from 0.0 to 1.0")
    core_argument: str = Field(description="Main reasoning supporting this choice")
    key_metrics: List[str] = Field(description="Supporting data points, financial metrics, or core values cited")


class Rebuttal(BaseModel):
    round_number: int = Field(description="The current debate round")
    agent_name: str = Field(description="Agent making the rebuttal")
    target_agent: str = Field(description="Agent being challenged")
    points_challenged: str = Field(description="Specific point or argument being criticized")
    concession: Optional[str] = Field(default=None, description="Acknowledgment of valid points from the target agent")
    revised_option_index: int = Field(description="Current preferred option index after debate (whether changed or kept)")
    revised_confidence_score: float = Field(ge=0.0, le=1.0, description="Updated confidence score after rebuttal")


class DecisionMatrix(BaseModel):
    recommended_option: str = Field(description="The final synthesized recommendation")
    consensus_score: float = Field(ge=0.0, le=1.0, description="Calculated agreement level")
    key_trade_offs: List[str] = Field(description="Main trade-offs acknowledged across positions")
    dissenting_views: List[str] = Field(description="Remaining unresolvable disagreements")
    action_plan_30_days: List[str] = Field(description="Concrete immediate steps for the user")

class CouncilState(TypedDict):
    user_context: UserContext
    positions: Annotated[List[AgentPosition], operator.add]
    rebuttals: Annotated[List[Rebuttal], operator.add]
    revision_count: int
    final_matrix: Optional[DecisionMatrix]