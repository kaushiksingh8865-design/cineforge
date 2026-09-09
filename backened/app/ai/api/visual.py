from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.agents.visual_runner import run_visual_agent
from app.ai.service.filmstartengine import FilmStateEngine
from app.ai.schemas.visual import VisualResult
from app.ai.database.database import get_db


router = APIRouter(
    prefix="/projects",
    tags=["visual"],
)


@router.post(
    "/{project_id}/scenes/{scene_id}/visual",
    response_model=VisualResult,
)
async def generate_visual(
    project_id: int,
    scene_id: int,
    request: str,
    db: AsyncSession = Depends(get_db),
):
    if not request.strip():
        raise HTTPException(
            status_code=400,
            detail="Visual request cannot be empty.",
        )

    try:
        # Get the scene and its Film State
        scene = await FilmStateEngine.get_film_state(
            db=db,
            scene_id=scene_id,
        )

        if scene is None:
            raise HTTPException(
                status_code=404,
                detail="Scene not found.",
            )

        # Make sure the scene belongs to the requested project
        if scene.project_id != project_id:
            raise HTTPException(
                status_code=404,
                detail="Scene does not belong to this project.",
            )

        # Assemble structured Film State context
        scene_state = FilmStateEngine.assemble_scene_state(scene)

        # Convert the state into text that can safely be supplied
        # to the Visual Agent.
        film_context = f"""
Project ID:
{project_id}

Scene ID:
{scene.id}

Scene:
{scene}

Scene State:
{scene_state["scene_state"]}

Character States:
{scene_state["character_states"]}

Prop States:
{scene_state["prop_states"]}
"""

        return await run_visual_agent(
            visual_request=request,
            film_context=film_context,
        )

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Visual generation failed: {str(exc)}",
        )