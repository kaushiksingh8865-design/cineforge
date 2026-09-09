from fastapi import APIRouter, HTTPException

from app.ai.agents.story_runner import run_story_agent
from app.ai.schemas.story import StoryResult


router = APIRouter(
    prefix="/projects",
    tags=["story"],
)


@router.post(
    "/{project_id}/ideas",
    response_model=StoryResult,
)
async def generate_ideas(
    project_id: int,
    request: str,
):
    if not request.strip():
        raise HTTPException(
            status_code=400,
            detail="Story request cannot be empty.",
        )

    try:
        return await run_story_agent(
            story_request=request,
            story_context="Scene 07 - Laboratory",
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Idea generation failed: {str(exc)}",
        )