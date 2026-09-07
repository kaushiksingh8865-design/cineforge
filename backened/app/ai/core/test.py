from app.ai.core.paralle_client import ParallelClient


def main():
    client = ParallelClient()

    results = client.search(
        objective=(
            "Find reliable information about visual characteristics "
            "of classic film noir cinematography."
        ),
        search_queries=[
            "classic film noir cinematography visual characteristics",
            "film noir lighting camera composition",
        ],
    )

    print("=" * 80)
    print("RESULT TYPE:", type(results))
    print("=" * 80)

    for index, result in enumerate(results, start=1):
        print(f"RESULT {index}")
        print("-" * 80)

        print("TITLE:", result["title"])
        print("URL:", result["url"])
        print("PUBLISH DATE:", result["publish_date"])

        print("EXCERPTS:")
        for excerpt in result["excerpts"]:
            print(excerpt)

        print("=" * 80)


if __name__ == "__main__":
    main()