from app.ai.service.filmstartengine import FilmStateEngine


def serialize_scene_state(scene_state):
    if scene_state is None:
        return None

    return {
        "state_data": scene_state.state_data,
    }


def serialize_character_state(character_state):
    return {
        "character_id": character_state.character_id,
        "status": character_state.status,
        "injuries": character_state.injuries,
        "wardrobe": character_state.wardrobe,
    }


def serialize_prop_state(prop_state):
    return {
        "prop_id": prop_state.prop_id,
        "holder": prop_state.holder,
        "location": prop_state.location,
        "status": prop_state.status,
    }


def serialize_scene(scene):
    if scene is None:
        return None

    return {
        "scene_number": scene.scene_number,
        "header": scene.header,
        "location": scene.location,
        "time_of_day": scene.time_of_day,
        "visual_prompt": scene.visual_prompt,
        "scene_state": serialize_scene_state(scene.state),
        "character_states": [
            serialize_character_state(state)
            for state in scene.character_states
        ],
        "prop_states": [
            serialize_prop_state(state)
            for state in scene.prop_states
        ],
    }


def build_film_context(continuity_context):
    if continuity_context is None:
        return None

    previous_state = continuity_context.get("previous_state")
    current_state = continuity_context.get("current_state")
    transition = continuity_context.get("transition")

    return {
        "previous_scene": (
            serialize_scene(previous_state["scene"])
            if previous_state
            else None
        ),
        "current_scene": (
            serialize_scene(current_state["scene"])
            if current_state
            else None
        ),
        "transition": transition,
    }