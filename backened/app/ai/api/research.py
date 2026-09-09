from fastapi import APIRouter, HTTPException

from app.ai.agents.research_runner import run_research_agent
from app.ai.schemas.research import ResearchResult


router = APIRouter(
    prefix="/projects",
    tags=["research"],
)


@router.post(
    "/{project_id}/research",
    response_model=ResearchResult,
)
async def research(
    project_id: int,
    question: str,
):
    if not question.strip():
        raise HTTPException(
            status_code=400,
            detail="Research question cannot be empty.",
        )

    try:
        return await run_research_agent(question)

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Research failed: {str(exc)}",
        )