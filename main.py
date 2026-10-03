from schemas import UserContext, CouncilState
from graph import app
from dotenv import load_dotenv

load_dotenv()

def run_council_demo():
    user_context = UserContext(
        dilemma_statement="Should our startup pivot to an enterprise-only SaaS model?",
        background_context=(
            "We have 6 months of runway left ($150,000 liquid cash). Current B2C revenue is flat at $5,000/month. "
            "Our monthly burn rate is approximately $25,000. Two enterprise clients have expressed strong intent "
            "and offered $50,000 annual contracts each, but only if we build custom security compliance features."
        ),
        proposed_options=[
            "Pivot fully to enterprise SaaS",
            "Maintain current B2C model and cut operational costs",
            "Hybrid model: Keep B2C live while building enterprise features"
        ],
        #  NUMERICAL INPUTS:
        liquid_savings=150000.0,
        monthly_expenses=25000.0,
        current_income=5000.0
    )

    initial_state: CouncilState = {
        "user_context": user_context,
        "positions": [],
        "rebuttals": [],
        "revision_count": 0,
        "final_matrix": None
    }

    print("\n" + "#" * 60)
    print("STARTING THE AUTONOMOUS AI COUNCIL DEBATE")
    print("#" * 60)

    # Run the state graph
    final_output = app.invoke(initial_state)

    # Final Summary Output
    print("\n" + "#" * 60)
    print("FINAL MEDIATOR SYNTHESIS & DECISION")
    print("#" * 60)

    matrix = final_output.get("final_matrix")
    if matrix:
        print(f"\nRECOMMENDED OPTION:\n   {matrix.recommended_option}")
        print(f"\nCOUNCIL CONSENSUS SCORE: {matrix.consensus_score * 100:.1f}%")

        if matrix.key_trade_offs:
            print("\nKEY TRADE-OFFS ACKNOWLEDGED:")
            for item in matrix.key_trade_offs:
                print(f"   • {item}")

        if matrix.dissenting_views:
            print("\nREMAINING DISSENTING VIEWS / RISKS:")
            for view in matrix.dissenting_views:
                print(f"   • {view}")

        if matrix.action_plan_30_days:
            print("\n30-DAY CONCRETE ACTION PLAN:")
            for step in matrix.action_plan_30_days:
                print(f"   [ ] {step}")

        if matrix.sources:
            print("\nCOMPILED RESEARCH SOURCES:")
            for url in matrix.sources:
                print(f"    {url}")
    else:
        print("No final decision matrix was generated.")

if __name__ == "__main__":
    run_council_demo()