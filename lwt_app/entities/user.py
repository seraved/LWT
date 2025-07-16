from dataclasses import dataclass, field


@dataclass(slots=True, kw_only=True, frozen=True)
class NewUserDTO():
    user_id: int
    username: str = field(default_factory=str)
    full_name: str = field(default_factory=str)
    phone: str = field(default_factory=str)

    def __repr__(self) -> str:
        return """
        user_id: {self.user_id},
        username: {self.username},
        full_name: {self.full_name},
        phone: {self.phone},
        """


@dataclass(slots=True, kw_only=True, frozen=True)
class UserDTO(NewUserDTO):
    is_approved: bool = False
    is_admin: bool = False
