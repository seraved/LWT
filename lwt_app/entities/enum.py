from enum import StrEnum


class WatchedEnum(StrEnum):
    ALL = "all"
    WATCHED = "watched"
    UNWATCHED = "unwatched"


class MediaTypeEnum(StrEnum):
    MOVIE = "movie"
    SERIES = "series"
    ANIME = "anime"
    CARTOON = "cartoon"
    ANIMATED_SERIES = "animated-series"
