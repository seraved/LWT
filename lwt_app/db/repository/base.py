from contextlib import AbstractAsyncContextManager
from dataclasses import dataclass
from types import TracebackType
from typing import Generic, Self, TypeVar

from core.database import BaseModel, async_session_factory
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

ModelT = TypeVar("ModelT", bound=BaseModel)


@dataclass(kw_only=True, frozen=True, slots=True)
class Pagination:
    page: int = 1
    per_page: int = 3

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.per_page

    def apply(self, stmt: Select) -> Select:
        return stmt.offset(self.offset).limit(self.per_page)


class BaseRepository(AbstractAsyncContextManager, Generic[ModelT]):
    session: AsyncSession

    async def __aenter__(self) -> Self:
        self.session = async_session_factory()
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool | None:
        await self.session.close()
        return None

    async def create(self, model: ModelT) -> ModelT:
        self.session.add(model)
        await self.session.commit()
        return model

    async def create_all(self, models: list[ModelT]) -> list[ModelT]:
        self.session.add_all(models)
        await self.session.commit()
        return models

    async def update(self, model: ModelT) -> ModelT:
        self.session.add(model)
        await self.session.commit()
        return model

    async def update_all(self, models: list[ModelT]) -> list[ModelT]:
        self.session.add_all(models)
        await self.session.commit()
        return models

    async def delete(self, model: ModelT) -> None:
        await self.session.delete(model)
        await self.session.commit()
