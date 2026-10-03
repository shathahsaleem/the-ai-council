from typing import Optional, List
from pydantic import BaseModel, Field
from duckduckgo_search import DDGS

# --- Financial Tool Schema ---
class RunwayOutput(BaseModel):
    runway_months: float = Field(description="Months of liquid runway remaining based on current savings and net burn")
    net_monthly_burn: float = Field(description="Monthly expenses minus current income")
    is_infinite: bool = Field(description="True if income covers or exceeds expenses")

# --- Search Tool Schema ---
class SearchResultItem(BaseModel):
    title: str = Field(description="Title of the article or study")
    snippet: str = Field(description="Key summary or relevant statistic")
    url: str = Field(description="Source URL for attribution")

class SearchOutput(BaseModel):
    query: str = Field(description="The search query executed")
    results: List[SearchResultItem] = Field(description="List of retrieved facts or statistics")


# TOOL FUNCTIONS

def calculate_financial_runway(
    liquid_savings: float,
    monthly_expenses: float,
    current_income: float = 0.0
) -> RunwayOutput:
    """Calculates how many months of cash remain based on spending and income."""
    
    # Calculate how much money is lost each month
    net_burn = monthly_expenses - current_income
    
    # If income covers expenses, you never run out of money!
    if net_burn <= 0:
        return RunwayOutput(
            runway_months=float("inf"),
            net_monthly_burn=net_burn,
            is_infinite=True
        )
    
    # Simple math: Savings divided by monthly loss
    runway = liquid_savings / net_burn
    
    return RunwayOutput(
        runway_months=round(runway, 1), # Round to 1 decimal place
        net_monthly_burn=net_burn,
        is_infinite=False
    )


def search_web_resources(query: str, max_results: int = 3) -> SearchOutput:
    """Searches DuckDuckGo for facts, regret rates, or studies to support non-financial agents."""
    
    ddgs = DDGS()
    
    # Get raw web search results
    raw_results = ddgs.text(query, max_results=max_results)
    
    # Loop through the web results and format them into our Pydantic model
    formatted_results = []
    for item in raw_results:
        formatted_results.append(
            SearchResultItem(
                title=item.get("title", ""),
                snippet=item.get("body", ""),
                url=item.get("href", "")
            )
        )
    
    return SearchOutput(query=query, results=formatted_results)