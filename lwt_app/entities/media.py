
from dataclasses import dataclass

from utils.mapper import media_type_to_text, kinopoisk_media_type
from entities.enum import MediaTypeEnum


@dataclass(kw_only=True, frozen=True, slots=True)
class BaseMedia:
    name: str
    media_type: str
    year: int
    description: str
    poster_url: str
    series_length: int
    kinopoisk_id: int
    genres: str


@dataclass(kw_only=True, frozen=True, slots=True)
class FoundMediaContent(BaseMedia):
    pass

    def to_msg(self) -> str:
        return (
            f"<b>{self.name}</b> ({self.year})\n"
            f"<b>Тип</b>: {self.media_type}\n"
            f"<b>Жанр</b>: {self.genres}\n"
            f"\n{self.description}"
        )


@dataclass(kw_only=True, frozen=True, slots=True)
class NewMediaDTO(BaseMedia):
    name: str
    media_type: MediaTypeEnum
    year: int
    description: str
    poster_url: str
    series_length: int
    kinopoisk_id: int
    genres: str

    @classmethod
    def from_found_content(cls, found_content: FoundMediaContent) -> "NewMediaDTO":
        media_type = kinopoisk_media_type(found_content.media_type)
        return NewMediaDTO(
            name=found_content.name,
            media_type=media_type or MediaTypeEnum.MOVIE,
            year=found_content.year,
            description=found_content.description,
            poster_url=found_content.poster_url,
            series_length=found_content.series_length,
            kinopoisk_id=found_content.kinopoisk_id,
            genres=found_content.genres,
        )


@dataclass(kw_only=True, frozen=True, slots=True)
class MediaDTO(NewMediaDTO):
    id: int
    watched: bool

    @property
    def status(self) -> str:
        return "✅" if self.watched else "🟡"

    def to_msg(self) -> str:
        m_type = media_type_to_text(self.media_type, 'EMPTY')
        return (
            f"Просмотрено: {self.status}\n"
            f"<b>{self.name}</b> ({self.year})\n"
            f"<b>Тип</b>: {m_type}\n"
            f"<b>Жанр</b>: {self.genres}\n"
            f"\n{self.description}"
        )
