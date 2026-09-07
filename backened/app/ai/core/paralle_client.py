from parallel import Parallel

from app.ai.core.settings import settings


class ParallelClient:
    def __init__(self):
        self.client = Parallel(
            api_key=settings.parallel_api_key
        )

    def search(
        self,
        objective: str,
        search_queries: list[str],
    ) -> list[dict]:
        response = self.client.search(
            objective=objective,
            search_queries=search_queries,
        )

        results = []

        for result in response.results:
            results.append(
                {
                    "title": result.title,
                    "url": result.url,
                    "excerpts": result.excerpts,
                    "publish_date": result.publish_date,
                }
            )

        return results