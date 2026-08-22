from app.ai.database.database import SessionLocal
from app.ai.models.film_project import FilmProject
from app.ai.models.scene1 import Scene


def test_project_scene_relationship():
    db = SessionLocal()

    try:
        project = FilmProject(
            title="Test Film",
            logline="A test film for CineForge.",
        )

        db.add(project)
        db.commit()
        db.refresh(project)

        scene = Scene(
            project_id=project.id,
            scene_number=1,
            header="INT. LABORATORY - NIGHT",
            location="Laboratory",
            time_of_day="night",
            visual_prompt="A dark laboratory at night.",
        )

        db.add(scene)
        db.commit()
        db.refresh(scene)

        print("Project ID:", project.id)
        print("Scene ID:", scene.id)

        loaded_project = (
            db.query(FilmProject)
            .filter(FilmProject.id == project.id)
            .first()
        )

        print("Project:", loaded_project.title)
        print("Number of scenes:", len(loaded_project.scenes))

        assert loaded_project is not None
        assert len(loaded_project.scenes) == 1
        assert loaded_project.scenes[0].scene_number == 1

        print("Database relationship test passed.")

    finally:
        db.close()


if __name__ == "__main__":
    test_project_scene_relationship()