
from db.repository import MediaRepository
from db.models import Media
from entities.media import MediaDTO


class MediaService:
    def __init__(self):
        self.media_repository = MediaRepository

    async def add_media(self, media_data: MediaDTO) -> Media:
        media = Media(
            title=media_data.title,
            media_type=media_data.media_type,
            watched=media_data.watched,
            user_id=media_data.user_id,
        )
        async with self.media_repository() as repo:
            return await repo.create(media)
        return media
