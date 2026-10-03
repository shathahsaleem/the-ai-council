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

    # Check 3: Debate Stalled (No position changes in the last turn)
    if revision_count > 1 and state.get("rebuttals"):
        last_round = [r for r in state["rebuttals"] if r.round_number == revision_count]
        prev_round = [r for r in state["rebuttals"] if r.round_number == revision_count - 1]

        last_choices = {r.agent_name: r.revised_option_index for r in last_round}
        prev_choices = {r.agent_name: r.revised_option_index for r in prev_round}

        if last_choices and last_choices == prev_choices:
            return "synthesize"

    # If no stopping conditions were met, keep debating!
    return "rebuttal"