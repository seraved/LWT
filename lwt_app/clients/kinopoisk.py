from typing import Any
from aiohttp import ClientSession
from contextlib import AbstractAsyncContextManager
from entities.media import FoundMediaContent
from core.config import settings
from utils.logs import logger


KINOPOISK_URL = "https://api.kinopoisk.dev"

SEARCH_PATH = "v1.4/movie/search"


class KinopoiskClient(AbstractAsyncContextManager):

    def __init__(self) -> None:
        self.session = ClientSession(base_url=KINOPOISK_URL)
        self.session.headers.update(
            {"X-API-KEY": settings.KINOPOISK_API_TOKEN},
        )

    async def __aenter__(self) -> "KinopoiskClient":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    def parse_result(
        self,
        response_data: dict[str, list[dict[str, Any]]],
    ) -> list[FoundMediaContent]:
        result: list[FoundMediaContent] = []
        for row in response_data["docs"]:
            genres = ', '.join((g["name"] for g in row.get("genres", [])))
            poster_url = row.get("poster", {})
            if isinstance(poster_url, dict):
                poster_url = poster_url.get("previewUrl", "")
            try:
                result.append(
                    FoundMediaContent(
                        name=row["name"],
                        media_type=row["type"],
                        year=row["year"],
                        description=row["description"],
                        poster_url=poster_url,
                        series_length=row.get("seriesLength") or 0,
                        kinopoisk_id=row["id"],
                        genres=genres,
                    )
                )
            except KeyError as e:
                continue
        return result

    async def search(self, title_name: str) -> list[FoundMediaContent]:
        params = {
            "page": 1,
            "limit": settings.KINOPOISK_RESULT_LIMIT,
            "query": title_name
        }
        result: list[FoundMediaContent] = []
        async with self.session.get(SEARCH_PATH, params=params) as resp:
            if resp.status == 200:
                data = await resp.json()
                if not data:
                    return result
                result = self.parse_result(response_data=data)
            else:
                logger.error(
                    f"Ошибка при запросе к API Кинопоиска: "
                    f"{resp.status} - {await resp.text()}"
                )
                # Можно выбрать, что возвращать при ошибке:
                # - Пустой список: return []
                # - Исключение: raise Exception(f"Ошибка API: {resp.status}")
                # Здесь возвращаем пустой список для простоты.

        return result
