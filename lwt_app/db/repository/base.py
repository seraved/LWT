from types import TracebackType
from typing import TypeVar, Generic, Self

from sqlalchemy.ext.asyncio import AsyncSession

from core.database import async_session_factory, BaseModel
from contextlib import AbstractAsyncContextManager

ModelT = TypeVar("ModelT", bound=BaseModel)


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
