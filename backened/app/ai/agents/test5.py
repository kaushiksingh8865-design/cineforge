import asyncio

from app.ai.agents.visual_runner import run_visual_agent


async def main():

    result = await run_visual_agent(
        visual_request=(
            "Create the visual direction for the moment "
            "when the detective discovers the dropped matchbook."
        ),
        film_context="""
Film style:
Classic film noir.

Location:
Old apartment at night.

Important elements:
Rain outside.
Fire escape window.
Desk.
Missing photograph.
Detective Arjun.
""",
        story_context="""
Arjun returns to the desk and discovers a damp footprint
on the floorboards and a dropped matchbook from a local
night club.

He carefully secures the matchbook as a new clue.
""",
        research_context="""
Classic film noir commonly uses low-key lighting,
strong contrast, dramatic shadows, and rain-slicked
night environments.
""",
    )

    print("=" * 80)
    print("VISUAL RESULT")
    print("=" * 80)

    print("\nSUMMARY:")
    print(result.summary)

    print("\nSHOTS:")

    for index, shot in enumerate(result.shots, start=1):
        print(f"\nSHOT {index}")
        print("Shot type:", shot.shot_type)
        print("Camera angle:", shot.camera_angle)
        print("Composition:", shot.composition)
        print("Lighting:", shot.lighting)
        print("Environment:", shot.environment)
        print("Character positioning:", shot.character_positioning)
        print("Atmosphere:", shot.atmosphere)

    print("\nIMAGE PROMPT:")
    print(result.image_prompt)


if __name__ == "__main__":
    asyncio.run(main())