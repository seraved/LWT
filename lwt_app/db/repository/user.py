from db.models.user import User
from db.repository.base import BaseRepository


class UserRepository(BaseRepository[User]):
    async def get_by_id(self, user_id: int) -> User | None:
        return await self.session.get(User, user_id)
