from typing import Any
from bot.keyboards.constants import (
    KEY_ANIME,
    KEY_MOVIE,
    KEY_SERIES,
    ANIME_TEXT,
    FILM_TEXT,
    SERIES_TEXT,
)
from entities.enum import MediaTypeEnum

MEDIA_TYPE_RUS_MAP = {
    MediaTypeEnum.MOVIE: "Фильм",
    MediaTypeEnum.SERIES: "Сериал",
    MediaTypeEnum.ANIME: "Аниме",
    MediaTypeEnum.CARTOON: "Мультфильм",
    MediaTypeEnum.ANIMATED_SERIES: "Мульт-сериал"
}

KEY_TO_MEDIA_TYPE_MAP = {
    KEY_MOVIE: MediaTypeEnum.MOVIE,
    KEY_SERIES: MediaTypeEnum.SERIES,
    KEY_ANIME: MediaTypeEnum.ANIME,
}

KEY_TO_TEXT_MAP = {
    KEY_MOVIE: FILM_TEXT,
    KEY_SERIES: SERIES_TEXT,
    KEY_ANIME: ANIME_TEXT,
}

KPOISK_TYPE_TO_MEDIA_TYPE = {
    "animated-series": MediaTypeEnum.ANIMATED_SERIES,
    "anime": MediaTypeEnum.ANIME,
    "cartoon": MediaTypeEnum.CARTOON,
    "movie": MediaTypeEnum.MOVIE,
    "tv-series": MediaTypeEnum.SERIES,
}


def media_type_to_text(
    m_type: MediaTypeEnum,
    default: str | None = None,
) -> str | None:
    return MEDIA_TYPE_RUS_MAP.get(m_type, default)


def key_to_media_type(
    key: str,
    default: MediaTypeEnum | None = None,
) -> MediaTypeEnum | None:
    return KEY_TO_MEDIA_TYPE_MAP.get(key, default)


def key_to_text(
    key: str,
    default: str | None = None,
) -> str | None:
    return KEY_TO_TEXT_MAP.get(key, default)


def kinopoisk_media_type(
    key: str,
    default: MediaTypeEnum | None = None,
) -> MediaTypeEnum | None:
    return KPOISK_TYPE_TO_MEDIA_TYPE.get(key, default)
