from dataclasses import dataclass
from typing import Sequence

from db.repository.base import BaseRepository, Pagination
from db.models.media import Media
from sqlalchemy import func, select, Select

from entities.media import MediaType, WatchedEnum


@dataclass(kw_only=True, frozen=True, slots=True)
class MediaFilter:
    user_id: int | None = None
    title: str | None = None
    media_type: MediaType | None = None
    watched: WatchedEnum = WatchedEnum.ALL

    def apply(self, stmt: Select) -> Select:
        if self.user_id is not None:
            stmt = stmt.where(Media.user_id == self.user_id)
        if self.title is not None:
            stmt = stmt.where(Media.title.ilike(f"%{self.title}%"))
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
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def toggle_watched_status(self, media_id: int) -> None:
        media = await self.get_by_id(media_id)
        if media is None:
            return None
        media.watched = not media.watched
        await self.update(media)
