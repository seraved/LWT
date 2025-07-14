from db.repository.base import BaseRepository
from db.models.media import Media
from typing import Sequence
from sqlalchemy import func, select

from sqlalchemy.orm import joinedload
from entities.system import Pagination


class MediaRepository(BaseRepository[Media]):
    async def get_by_id(self, media_id: int) -> Media | None:
        return await self.session.get(Media, media_id)

    async def get_count(self, user_id: int) -> int:
        stmt = select(
            func.count(Media.id)
        ).where(Media.user_id == user_id)
        return await self.session.scalar(stmt) or 0

    async def get_by_user_id(
        self,
        user_id: int,
        pagination: Pagination | None = None
    ) -> Sequence[Media]:
        stmt = select(
            Media
        ).where(
            Media.user_id == user_id
        ).options(
            joinedload(Media.user)
        )
        if pagination is not None:
            stmt = stmt.offset(
                pagination.offset
            ).limit(
                pagination.per_page
            )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    # async def get_rows(
    #     self,
    # ) -> Sequence[Media]:
    #     # async def get_user_media(user_id: int, page: int = 1, per_page: int = 3):
    # async with async_session() as session:
    #     offset = (page - 1) * per_page
    #     stmt = (
    #         select(Media)
    #         .where(Media.user_id == user_id)
    #         .offset(offset)
    #         .limit(per_page)
    #     result=await session.execute(stmt)
    #     return result.scalars().all()
    #     return []
