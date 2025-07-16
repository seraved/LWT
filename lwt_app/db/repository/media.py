from dataclasses import dataclass
from typing import Sequence

from db.repository.base import BaseRepository, Pagination
from db.models.media import Media
from sqlalchemy import func, select, Select, exists, desc

from entities.media import MediaTypeEnum
from entities.enum import WatchedEnum


@dataclass(kw_only=True, frozen=True, slots=True)
class MediaFilter:
    user_id: int | None = None
    name: str | None = None
    year: int | None = None
    media_type: MediaTypeEnum | None = None
    watched: WatchedEnum = WatchedEnum.ALL

    def apply(self, stmt: Select) -> Select:
        if self.user_id is not None:
            stmt = stmt.where(Media.user_id == self.user_id)
        if self.name is not None:
            stmt = stmt.where(Media.name.ilike(f"%{self.name}%"))
        if self.media_type is not None:
            stmt = stmt.where(Media.media_type == self.media_type)
        if self.watched is WatchedEnum.UNWATCHED:
            stmt = stmt.where(Media.watched == False)
        elif self.watched is WatchedEnum.WATCHED:
            stmt = stmt.where(Media.watched == True)

        return stmt


class MediaRepository(BaseRepository[Media]):
    async def get_by_id(self, media_id: int) -> Media | None:
        return await self.session.get(Media, media_id)

    async def get_count(
        self,
        filters: MediaFilter | None = None,
    ) -> int:
        stmt = select(
            func.count(Media.id)
        )
        if filters is not None:
            stmt = filters.apply(stmt)

        return await self.session.scalar(stmt) or 0

    async def get_user_media(
        self,
        filters: MediaFilter | None = None,
        pagination: Pagination | None = None
    ) -> Sequence[Media]:
        stmt = select(Media)
        if filters is not None:
            stmt = filters.apply(stmt)
        if pagination is not None:
            stmt = stmt.offset(
                pagination.offset
            ).limit(
                pagination.per_page
            )
        stmt = stmt.order_by(desc(Media.id))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def toggle_watched_status(self, media_id: int) -> Media | None:
        media = await self.get_by_id(media_id)
        if media is None:
            return None
        media.watched = not media.watched
        return await self.update(media)

    async def exist(self, media_filter: MediaFilter) -> bool:
        stmt = media_filter.apply(select(Media.id))
        result = await self.session.scalar(stmt)
        return bool(result)

    async def create_if_not_exists(self, media: Media) -> Media | None:
        exists_filter = MediaFilter(
            name=media.name,
            year=media.year,
            user_id=media.user_id,
        )
        if await self.exist(exists_filter):
            return None
        return await self.create(media)
