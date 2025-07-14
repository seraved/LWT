
from db.models import Media
from db.repository.media import MediaFilter, MediaRepository, Pagination
from entities.media import MediaDTO, NewMediaDTO, WatchedEnum


class MediaService:
    def __init__(self):
        self.media_repository = MediaRepository

    def to_dto(self, media: Media) -> MediaDTO:
        return MediaDTO(
            id=media.id,
            title=media.title,
            media_type=media.media_type,
            watched=media.watched,
            user_id=media.user_id,
        )

    async def add_media(self, media_data: NewMediaDTO) -> None:
        media = Media(
            title=media_data.title,
            media_type=media_data.media_type,
            watched=media_data.watched,
            user_id=media_data.user_id,
        )
        async with self.media_repository() as repo:
            await repo.create(media)

    async def get_media_count(
        self,
        user_id: int,
        watched_filter: str | None = None,
    ) -> int:
        async with self.media_repository() as repo:
            return await repo.get_count(
                filters=MediaFilter(
                    user_id=user_id,
                    watched=WatchedEnum[watched_filter] if watched_filter else WatchedEnum.ALL
                )
            )

    async def get_user_media(
        self,
        user_id: int,
        watched_filter: str | None = None,
        page: int = 1,
        per_page: int = 3,
    ) -> list[MediaDTO]:
        pagination = Pagination(
            page=page,
            per_page=per_page
        )
        filters = MediaFilter(
            user_id=user_id,
            watched=WatchedEnum[watched_filter] if watched_filter else WatchedEnum.ALL
        )
        async with self.media_repository() as repo:
            user_media = await repo.get_user_media(
                filters=filters,
                pagination=pagination
            )
        return [self.to_dto(media) for media in user_media]

    async def toggle_watched_status(self, media_id: int) -> None:
        async with self.media_repository() as repo:
            await repo.toggle_watched_status(media_id)
