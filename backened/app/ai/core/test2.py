import asyncio

from app.ai.core.image_generator import  ImageGenerator


async def main():

    generator = ImageGenerator()

    result = await generator.generate(
        prompt="""
Classic black-and-white film noir interior.

A detective in a trench coat stands inside
an old apartment at night.

Rain streaks across the fire escape window.
Venetian blind shadows fall across the room.
A damp matchbook lies on the wooden floor
beside a clear wet footprint.

High-contrast chiaroscuro lighting,
deep blacks, dramatic composition,
35mm film grain, realistic cinematic photography.
""",
        output_path="generated_images/test_noir.png",
    )

    print("=" * 80)
    print("IMAGE GENERATION RESULT")
    print("=" * 80)

    print("Prompt:")
    print(result.prompt)

    print("\nGenerated images:")

    for image in result.images:
        print("MIME type:", image.mime_type)
        print("File:", image.file_path)


if __name__ == "__main__":
    asyncio.run(main())