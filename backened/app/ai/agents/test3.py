import asyncio

from app.ai.agents.research_runner import run_research_agent


async def main():

    result = await run_research_agent(
        "What are the common visual characteristics "
        "of classic film noir cinematography?"
    )

    print(result)


if __name__ == "__main__":
    asyncio.run(main())