import traceback

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.api.auth import get_current_user
from app.ai.database.database import get_db
from app.ai.etl.extractor import SourceExtractor
from app.ai.etl.loader import FilmDataLoader
from app.ai.etl.transformer import transform_source
from app.ai.models.user import User
from app.ai.schemas.source import SourceFileResponse
from app.ai.service.filmprojectservice import FilmService
from app.ai.service.sourceservice import SourceService


class SourceContentUpdate(BaseModel):
    content: str


router = APIRouter(
    prefix="/projects",
    tags=["sources"],
)


# =========================================================
# UPLOAD SOURCE
# =========================================================

@router.post(
    "/{project_id}/sources/upload",
    response_model=SourceFileResponse,
)
async def upload_source(
    project_id: int,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = await FilmService.get_project(
        db,
        project_id,
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found.",
        )

    if project.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this project.",
        )

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="File name is required.",
        )

    file_content = await file.read()

    if not file_content:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty.",
        )

    try:
        source = await SourceService.create_uploaded_source(
            db=db,
            project_id=project_id,
            filename=file.filename,
            file_content=file_content,
            mime_type=file.content_type,
        )

        return {
            "id": source.id,
            "project_id": source.project_id,
            "name": source.name,
            "source_type": source.source_type,
            "mime_type": source.mime_type,
            "file_path": source.file_path,
            "content": source.content,
            "file_metadata": source.file_metadata,
        }

    except Exception:
        await db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Failed to upload source file.",
        )


# =========================================================
# INGEST SOURCE
# =========================================================

@router.post(
    "/{project_id}/sources/{source_id}/ingest",
)
async def ingest_source(
    project_id: int,
    source_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = await FilmService.get_project(
        db,
        project_id,
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found.",
        )

    if project.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this project.",
        )

    source = await SourceService.get_source(
        db,
        source_id,
    )

    if source is None:
        raise HTTPException(
            status_code=404,
            detail="Source not found.",
        )

    if source.project_id != project_id:
        raise HTTPException(
            status_code=404,
            detail="Source does not belong to this project.",
        )

    try:
        # 1. Extract source text
        source_text = await SourceExtractor.extract(
            source
        )

        if not source_text.strip():
            raise HTTPException(
                status_code=400,
                detail="Source contains no usable text.",
            )

        # 2. Transform source text using Gemini
        film_data = await transform_source(
            source_text
        )

        # 3. Load structured data into Film State
        scene = await FilmDataLoader.load(
            db=db,
            project_id=project_id,
            film_data=film_data,
        )

        return {
            "success": True,
            "message": "Source ingested successfully.",
            "source_id": source.id,
            "scene": {
                "id": scene.id,
                "scene_number": scene.scene_number,
                "header": scene.header,
                "location": scene.location,
                "time_of_day": scene.time_of_day,
            },
            "film_data": film_data.model_dump(),
        }

    except HTTPException:
        raise

    except Exception as exc:
        await db.rollback()
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=f"Failed to ingest source: {str(exc)}",
        )


# =========================================================
# UPDATE SOURCE CONTENT
# =========================================================

@router.put(
    "/{project_id}/sources/{source_id}/content"
)
async def update_source_content(
    project_id: int,
    source_id: int,
    data: SourceContentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = await FilmService.get_project(
        db,
        project_id,
    )

    if project is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found.",
        )

    if project.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You do not have access to this project.",
        )

    source = await SourceService.get_source(
        db,
        source_id,
    )

    if source is None:
        raise HTTPException(
            status_code=404,
            detail="Source not found.",
        )

    if source.project_id != project_id:
        raise HTTPException(
            status_code=404,
            detail="Source does not belong to this project.",
        )

    try:
        source.content = data.content

        await db.commit()
        await db.refresh(source)

        return {
            "success": True,
            "message": "Source content saved successfully.",
            "source_id": source.id,
        }

    except Exception:
        await db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Failed to save source content.",
        )