import asyncio

from app.ai.agents.continuity_runner import run_continuity_agent


context = {
    "previous_state": {
        "scene_id": 1,
        "character_states": [
            {
                "character_id": 10,
                "status": "healthy",
                "injuries": [],
                "wardrobe": ["black jacket"],
            }
        ],
        "prop_states": [
            {
                "prop_id": 20,
                "holder": "John",
                "location": "kitchen",
                "status": "intact",
            }
        ],
    },
    "current_state": {
        "scene_id": 2,
        "character_states": [
            {
                "character_id": 10,
                "status": "injured",
                "injuries": ["broken arm"],
                "wardrobe": ["black jacket"],
            }
        ],
        "prop_states": [
            {
                "prop_id": 20,
                "holder": "Mary",
                "location": "bedroom",
                "status": "broken",
            }
        ],
    },
    "transition": {
        "characters": {
            "changed": [
                {
                    "entity_id": 10,
                    "changes": {
                        "status": {
                            "previous": "healthy",
                            "current": "injured",
                        },
                        "injuries": {
                            "previous": [],
                            "current": ["broken arm"],
                        },
                    },
                }
            ]
        },
        "props": {
            "changed": [
                {
                    "entity_id": 20,
                    "changes": {
                        "holder": {
                            "previous": "John",
                            "current": "Mary",
                        },
                        "location": {
                            "previous": "kitchen",
                            "current": "bedroom",
                        },
                        "status": {
                            "previous": "intact",
                            "current": "broken",
                        },
                    },
                }
            ]
        },
    },
}


async def main():
    result = await run_continuity_agent(context)

    print(result)


if __name__ == "__main__":
    asyncio.run(main())