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


@dataclass(kw_only=True, frozen=True, slots=True)
class NewMediaDTO:
    title: str
    media_type: MediaType
    user_id: int
    watched: bool = False


@dataclass(kw_only=True, frozen=True, slots=True)
class MediaDTO(NewMediaDTO):
    id: int
