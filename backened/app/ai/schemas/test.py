from app.ai.schemas.scene import Scene


scene = Scene(
    scene_number=7,
    header="INT. LABORATORY - NIGHT",
    location="Laboratory",
    time_of_day="night",
    characters=[
        {
            "name": "Maya",
            "status": "active",
            "injuries": [],
            "wardrobe": ["black jacket"],
        }
    ],
    props=[
        {
            "name": "Rifle",
            "holder": "Maya",
            "location": "laboratory table",
        }
    ],
)

print(scene)