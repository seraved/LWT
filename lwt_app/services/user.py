from db.repository import UserRepository
from db.models.user import User


class UserService:
    def __init__(self):
        self.user_repository = UserRepository

    async def create_user(self, user_id: int, username: str) -> User:
        user = User(user_id=user_id, username=username)

        async with self.user_repository() as repo:
            return await repo.create(user)

        return user

    async def get_user(self, user_id: int) -> User | None:
        async with self.user_repository() as repo:
            return await repo.get_by_id(user_id)
        return None

    