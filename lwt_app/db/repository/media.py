from db.repository.base import BaseRepository
from db.models.media import Media
from typing import Sequence
from sqlalchemy import select
from sqlalchemy.orm import joinedload


class MediaRepository(BaseRepository[Media]):
    async def get_by_id(self, media_id: int) -> Media | None:
        return await self.session.get(Media, media_id)

    async def get_by_user_id(self, user_id: int) -> Sequence[Media]:
        stmt = select(Media).where(Media.user_id == user_id).options(
            joinedload(Media.user)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
