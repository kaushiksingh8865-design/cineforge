from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.database.database import get_db
from app.ai.schemas.save import SaveRequest
from app.ai.service.update import (
    StateUpdateError,
    StateUpdateService,
)

router = APIRouter(
    prefix="/save",
    tags=["save"],
)


@router.post("")
async def save_film_state(
    save_request: SaveRequest,
    db: AsyncSession = Depends(get_db),
):
    try:
        results = await StateUpdateService.apply_save_request(
            db=db,
            save_request=save_request,
        )

        return {
            "success": True,
            "message": "Film state saved successfully.",
            "changes_applied": len(results),
        }

    except StateUpdateError as exc:
        raise HTTPException(
            status_code=409,
            detail=str(exc),
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Failed to save film state.",
        )