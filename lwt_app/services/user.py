from db.repository import UserRepository
from db.models.user import User

from entities.user import UserDTO, NewUserDTO


class UserService:
    def __init__(self):
        self.user_repository = UserRepository

    def model_to_dto(self, user: User) -> UserDTO:
        return UserDTO(
            user_id=user.user_id,
            username=user.username,
            full_name=user.full_name,
            phone=user.phone,
            is_approved=user.is_approved,
            is_admin=user.is_admin,
        )

    def dto_to_model(self, user_data: NewUserDTO) -> User:
        return User(
            user_id=user_data.user_id,
            username=user_data.username,
            full_name=user_data.full_name,
            phone=user_data.phone,
        )

    async def create_user(self, user_data: NewUserDTO) -> User:
        user = self.dto_to_model(user_data)

        async with self.user_repository() as repo:
            return await repo.create(user)

        return user

    async def get_user(self, user_id: int) -> UserDTO | None:
        async with self.user_repository() as repo:
            user = await repo.get_by_id(user_id)
            return self.model_to_dto(user) if user else None
        return None
