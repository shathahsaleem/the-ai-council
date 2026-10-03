from schemas import CouncilState

def route_debate(state: CouncilState) -> str:
    """
    Determines whether the debate should continue ("rebuttal") 
    or move to final summary ("synthesize").
    """
    MAX_ROUNDS = 3
    revision_count = state.get("revision_count", 0)

    # Check 1: Reached Max Round Cap
    if revision_count >= MAX_ROUNDS:
        return "synthesize"

    # Gather latest choice per agent
    latest_choices = {}
    if state.get("rebuttals"):
        for rebuttal in reversed(state["rebuttals"]):
            if rebuttal.agent_name not in latest_choices:
                latest_choices[rebuttal.agent_name] = rebuttal.revised_option_index
    else:
        for pos in state.get("positions", []):
            latest_choices[pos.agent_name] = pos.preferred_option_index

    # Check 2: Full Consensus Reached
    unique_choices = set(latest_choices.values())
    if len(unique_choices) == 1:
        return "synthesize"

    # Check 3: Only check if rebuttals actually exist!
    if state.get("rebuttals") and state.get("positions"):
        initial_choices = {p.agent_name: p.preferred_option_index for p in state["positions"]}
        rebuttal_choices = {r.agent_name: r.revised_option_index for r in state["rebuttals"]}

        # Put this INSIDE the if block so it doesn't crash in Round 0
        if initial_choices == rebuttal_choices:
            return "synthesize"

    # If no stopping conditions were met, proceed to rebuttal round
    return "rebuttal"