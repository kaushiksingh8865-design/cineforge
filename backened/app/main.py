from fastapi import FastAPI
app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/projects/{projects_id}")
def get_projects(projects_id: int):
    return {"projects": projects_id}

@app.get("/projects")
def get_projects(limit: int = 10):
    return {
        "limit": limit
    }