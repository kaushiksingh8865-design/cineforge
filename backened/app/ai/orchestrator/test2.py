from app.ai.orchestrator.film_context import build_film_context



from app.ai.orchestrator.film_context import (
    serialize_scene_state,
    serialize_character_state,
    serialize_prop_state,
)


class FakeSceneState:
    state_data = {
        "weather": "rain",
        "door": "open",
    }


class FakeCharacterState:
    character_id = 1
    status = "injured"
    injuries = ["cut on left hand"]
    wardrobe = ["dark coat"]


class FakePropState:
    prop_id = 2
    holder = "Detective Arjun"
    location = "desk"
    status = "present"


def main():
    scene_state = serialize_scene_state(FakeSceneState())
    character_state = serialize_character_state(FakeCharacterState())
    prop_state = serialize_prop_state(FakePropState())

    print("=" * 80)
    print("FILM CONTEXT SERIALIZER TEST")
    print("=" * 80)

    print("\nSCENE STATE:")
    print(scene_state)

    print("\nCHARACTER STATE:")
    print(character_state)

    print("\nPROP STATE:")
    print(prop_state)


if __name__ == "__main__":
    main()

    
class FakeScene:
    scene_number = 2
    header = "INT. APARTMENT - NIGHT"
    location = "Old apartment"
    time_of_day = "Night"
    visual_prompt = None
    state = FakeSceneState()
    character_states = [FakeCharacterState()]
    prop_states = [FakePropState()]


def test_build_film_context():
    continuity_context = {
        "previous_state": {
            "scene": FakeScene(),
        },
        "current_state": {
            "scene": FakeScene(),
        },
        "transition": {
            "characters": {
                "changed": [],
                "added": [],
                "removed": [],
            },
            "props": {
                "changed": [],
                "added": [],
                "removed": [],
            },
        },
    }

    context = build_film_context(continuity_context)

    print("=" * 80)
    print("BUILD FILM CONTEXT TEST")
    print("=" * 80)
    print(context)


if __name__ == "__main__":
    test_build_film_context()