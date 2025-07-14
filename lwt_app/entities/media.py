from enum import StrEnum
from dataclasses import dataclass


class WatchedEnum(StrEnum):
    ALL = "all"
    WATCHED = "watched"
    UNWATCHED = "unwatched"


class MediaType(StrEnum):
    MOVIE = "movie"
    SERIES = "series"
    ANIME = "anime"


MEDIA_TYPE_RUS_MAP = {
    MediaType.MOVIE: "Фильм",
    MediaType.SERIES: "Сериал",
    MediaType.ANIME: "Аниме"
}


@dataclass(kw_only=True, frozen=True, slots=True)
class NewMediaDTO:
    title: str
    media_type: MediaType
    user_id: int
    watched: bool = False


@dataclass(kw_only=True, frozen=True, slots=True)
class MediaDTO(NewMediaDTO):
    id: int

    @property
    def status(self) -> str:
        return "✅" if self.watched else "🟡"

    def to_msg(self) -> str:
        m_type = MEDIA_TYPE_RUS_MAP.get(self.media_type, 'EMPTY')
        return f"{self.status} {self.title} ({m_type})"
