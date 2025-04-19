from fastapi import APIRouter
from backend.agents.agent_loader import load_agent

router = APIRouter()

agent = load_agent()

@router.post("/agent", tags=["Agent"])
async def run_agent(query: str):
    """
    Executes the agent with the given query input.

    Parameters
    ----------
    query : str
        The input prompt or question from the user.

    Returns
    -------
    dict
        The agent's response.
    """
    result = await agent.ainvoke({"input": query})
    return {"response": result}
