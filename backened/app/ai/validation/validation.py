from backened.app.ai.schemas.scene import Scene


VALID_TIME_OF_DAY = {
    "morning",
    "afternoon",
    "evening",
    "night",
    "day",
}


def validate_scene(scene: Scene) -> list[str]:
    errors: list[str] = []

    if scene.scene_number <= 0:
        errors.append("Scene number must be greater than 0.")

    if not scene.header or not scene.header.strip():
        errors.append("Scene header must not be empty.")

    if not scene.location.strip():
        errors.append("Location must not be empty.")

    if scene.time_of_day.lower() not in VALID_TIME_OF_DAY:
        errors.append(
            "Invalid time of day. "
            "Must be one of: morning, afternoon, evening, night, day."
        )

    for character in scene.characters:
        if not character.name.strip():
            errors.append("Character name must not be empty.")

    for prop in scene.props:
        if not prop.name.strip():
            errors.append("Prop name must not be empty.")

    return errors