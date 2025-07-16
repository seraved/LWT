
from db.models import Media
from db.repository.media import MediaFilter, MediaRepository, Pagination
from entities.media import MediaDTO, NewMediaDTO
from entities.user import UserDTO
from entities.enum import WatchedEnum, MediaTypeEnum


class MediaService:
    def __init__(self):
        self.media_repository = MediaRepository

    def model_to_dto(self, media: Media) -> MediaDTO:
        return MediaDTO(
            id=media.id,
            name=media.name,
            media_type=media.media_type,
            year=media.year,
            description=media.description,
            poster_url=media.poster_url,
            series_length=media.series_length,
            kinopoisk_id=media.kinopoisk_id,
            genres=media.genres,
            watched=media.watched,
        )

    def dto_to_model(self, media_content: NewMediaDTO, user: UserDTO) -> Media:
        return Media(
            name=media_content.name,
            media_type=media_content.media_type,
            year=media_content.year,
            description=media_content.description,
            poster_url=media_content.poster_url,
            series_length=media_content.series_length,
            kinopoisk_id=media_content.kinopoisk_id,
            genres=media_content.genres,
            user_id=user.user_id,
        )

    async def add_media_content(self, user: UserDTO, media_content: NewMediaDTO) -> None:
        media = self.dto_to_model(
            media_content=media_content,
            user=user,
        )
        async with self.media_repository() as repo:
            await repo.create_if_not_exists(media)

    async def get_media_count(
        self,
        user_id: int,
        media_type: MediaTypeEnum | None = None,
        watched_filter: WatchedEnum | None = None,
    ) -> int:
        async with self.media_repository() as repo:
            return await repo.get_count(
                filters=MediaFilter(
                    user_id=user_id,
                    media_type=media_type,
                    watched=watched_filter if watched_filter else WatchedEnum.ALL
                )
            )

    async def get_user_media(
        self,
        user_id: int,
        watched_filter: WatchedEnum | None = None,
        media_type: MediaTypeEnum | None = None,
        page: int = 1,
        per_page: int = 3,
    ) -> list[MediaDTO]:
        pagination = Pagination(
            page=page,
            per_page=per_page
        )
        filters = MediaFilter(
            user_id=user_id,
            media_type=media_type,
            watched=watched_filter if watched_filter else WatchedEnum.ALL
        )
        async with self.media_repository() as repo:
            user_media = await repo.get_user_media(
                filters=filters,
                pagination=pagination
            )
        return [self.model_to_dto(media) for media in user_media]

    async def toggle_watched_status(self, media_id: int) -> MediaDTO | None:
        async with self.media_repository() as repo:
            media = await repo.toggle_watched_status(media_id)
            return self.model_to_dto(media) if media else None
