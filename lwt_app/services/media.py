
from db.repository import MediaRepository
from db.models import Media
from entities.media import MediaDTO
from entities.system import Pagination


class MediaService:
    def __init__(self):
        self.media_repository = MediaRepository

    def to_dto(self, media: Media) -> MediaDTO:
        return MediaDTO(
            title=media.title,
            media_type=media.media_type,
            watched=media.watched,
            user_id=media.user_id,
        )

    async def add_media(self, media_data: MediaDTO) -> None:
        media = Media(
            title=media_data.title,
            media_type=media_data.media_type,
            watched=media_data.watched,
            user_id=media_data.user_id,
        )
        async with self.media_repository() as repo:
            await repo.create(media)

    async def get_media_count(self, user_id: int) -> int:
        async with self.media_repository() as repo:
            return await repo.get_count(user_id)

    async def get_user_media(
        self,
        user_id: int,
        page: int = 1,
        per_page: int = 3,
    ) -> list[MediaDTO]:
        async with self.media_repository() as repo:
            user_media = await repo.get_by_user_id(
                user_id=user_id,
                pagination=Pagination(
                    page=page,
                    per_page=per_page
                )
            )
        return [self.to_dto(media) for media in user_media]
