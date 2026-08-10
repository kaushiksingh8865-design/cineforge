from backened.app.ai.schemas.scene import Scene


def validate_scene(scene: Scene) -> list[str]:
    errors =[]# now lets add rules here. ->
    if scene.scene_number <= 0:
        errors.append("Scene number must be greater than 0.")
    if not scene.location.strip():
        errors.append('Location must not be empty.')
    validate_time_of_day ={
        'morning',
        'afternoon',
        'evening',
        'night',
        'day'
    }  
    if scene.time_of_day.lower() not in validate_time_of_day:
        errors.append('invalid time of day. Must be one of: morning, afternoon, evening, night, day.')
    return errors



  