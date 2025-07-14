from enum import StrEnum
from dataclasses import dataclass


class MediaType(StrEnum):
    MOVIE = "movie"
    SERIES = "series"
    ANIME = "anime"


@dataclass(kw_only=True, frozen=True, slots=True)
class MediaDTO:
    title: str
    media_type: MediaType
    user_id: int
    watched: bool = False
