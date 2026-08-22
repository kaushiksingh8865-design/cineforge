from fastapi import FastAPI
app = FastAPI()


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


