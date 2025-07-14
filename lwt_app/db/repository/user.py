from db.repository.base import BaseRepository
from db.models.user import User

class UserRepository(BaseRepository[User]):
    async def get_by_id(self, user_id: int) -> User | None:
        return await self.session.get(User, user_id)
    