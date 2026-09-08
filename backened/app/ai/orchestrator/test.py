import asyncio

from app.ai.orchestrator.runner import run_story_visual_pipeline


async def main():
    events = await run_story_visual_pipeline(
        request=(
            "Continue the detective scene after he discovers "
            "the dropped matchbook and create the visual direction "
            "for that moment."
        ),
        context="""
Film style:
Classic film noir.

Location:
Old apartment at night.

Characters:
- Detective Arjun: observant, cautious, persistent.

Important elements:
- Missing photograph
- Desk
- Fire escape window
- Rain outside

Research:
Classic film noir commonly uses low-key lighting,
strong contrast, dramatic shadows, and rain-soaked
night environments.
""",
    )

    print("=" * 80)
    print("ORCHESTRATION EVENTS")
    print("=" * 80)

    for index, event in enumerate(events, start=1):
        print(f"\nEVENT {index}")
        print("-" * 80)

        print("AUTHOR:", event.author)

        if event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    print("TEXT:")
                    print(part.text)


if __name__ == "__main__":
    asyncio.run(main())