from fastapi import FastAPI
from app.ai.api.save import router as save_router
from app.ai.api.sourceapi import router as source_router
from fastapi.middleware.cors import CORSMiddleware
from app.ai.api.research import router as research_router
from app.ai.api.story import router as story_router
from app.ai.api.visual import router as visual_router 
from app.ai.api.auth import router as auth_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(save_router)

app.include_router(save_router)
app.include_router(source_router)
app.include_router(research_router)
app.include_router(story_router)
app.include_router(visual_router)
app.include_router(auth_router)
@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }


@app.get("/projects/{project_id}")
def get_project(project_id: int):
    return {
        "project_id": project_id
    }


@app.get("/projects")
def list_projects(limit: int = 10):
    return {
        "limit": limit
    }


