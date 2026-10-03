from langgraph.graph import StateGraph, START, END
from schemas import CouncilState
from agents import (
    risk_agent_node,
    philosopher_agent_node,
    innovator_agent_node,
    mediator_agent_node
)
from router import route_debate

# 1. Initialize the StateGraph
builder = StateGraph(CouncilState)

# 2. Add all Nodes
builder.add_node("risk_agent", risk_agent_node)
builder.add_node("philosopher_agent", philosopher_agent_node)
builder.add_node("innovator_agent", innovator_agent_node)
builder.add_node("mediator_agent", mediator_agent_node)

# 3. Entry Point: Start with the Risk Agent
builder.add_edge(START, "risk_agent")

# 4. Sequential Debate Flow
builder.add_edge("risk_agent", "philosopher_agent")
builder.add_edge("philosopher_agent", "innovator_agent")

# 5. Conditional Router after Innovator speaks
builder.add_conditional_edges(
    "innovator_agent",
    route_debate,
    {
        "rebuttal": "risk_agent",      # Loop back to risk_agent for another round
        "synthesize": "mediator_agent" # Move to mediator_agent when finished
    }
)

# 6. Final Edge
builder.add_edge("mediator_agent", END)

# 7. Compile Graph
app = builder.compile()