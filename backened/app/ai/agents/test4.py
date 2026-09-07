import asyncio

from app.ai.agents.story_runner import run_story_agent


async def main():
    result = await run_story_agent(
        story_request=(
            "Continue the detective scene after he discovers "
            "that the photograph has disappeared."
        ),
        story_context="""
Scene: A private detective is investigating a murder.

The detective is alone in an old apartment at night.
A framed photograph was previously hanging above the desk.
He notices that the photograph is now missing.

Character:
- Detective Arjun: observant, cautious, persistent.
- Unknown suspect: has not yet been identified.

Tone:
- Dark
- Suspenseful
- Noir-inspired
""",
        research_context="""
Classic film noir commonly uses low-key lighting,
strong contrast, dramatic shadows, and visually
disorienting compositions.
""",
    )

    print("=" * 80)
    print("STORY RESULT")
    print("=" * 80)

    print("SUMMARY:")
    print(result.summary)

    print("\nSTORY BEATS:")
    for index, beat in enumerate(result.beats, start=1):
        print(f"\n{index}. {beat.description}")
        print(f"   Purpose: {beat.purpose}")

    print("\nDIALOGUE SUGGESTIONS:")
    for dialogue in result.dialogue_suggestions:
        print(f"- {dialogue}")

    print("\nCHARACTER ACTIONS:")
    for action in result.character_actions:
        print(f"- {action}")


if __name__ == "__main__":
    asyncio.run(main())