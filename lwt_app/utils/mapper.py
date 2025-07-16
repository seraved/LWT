from typing import Any
from bot.keyboards import constants as const

from entities.enum import MediaTypeEnum

MEDIA_TYPE_RUS_MAP = {
    MediaTypeEnum.MOVIE: "Фильм",
    MediaTypeEnum.SERIES: "Сериал",
    MediaTypeEnum.ANIME: "Аниме",
    MediaTypeEnum.CARTOON: "Мультфильм",
    MediaTypeEnum.ANIMATED_SERIES: "Мульт-сериал"
}

KEY_TO_MEDIA_TYPE_MAP = {
    const.KEY_TYPE_MOVIE: MediaTypeEnum.MOVIE,
    const.KEY_TYPE_SERIES: MediaTypeEnum.SERIES,
    const.KEY_TYPE_ANIME: MediaTypeEnum.ANIME,
}

KEY_TO_TEXT_MAP = {
    const.KEY_TYPE_MOVIE: const.MOVIE_TEXT,
    const.KEY_TYPE_SERIES: const.SERIES_TEXT,
    const.KEY_TYPE_ANIME: const.ANIME_TEXT,
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
