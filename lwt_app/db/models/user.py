from typing import TYPE_CHECKING, List

from core.config import settings
from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import BaseModel

if TYPE_CHECKING:
    from .media import Media


class User(BaseModel):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )
    username: Mapped[str] = mapped_column(default="")
    full_name: Mapped[str] = mapped_column(default="")
    phone: Mapped[str] = mapped_column(default="")

    is_approved: Mapped[bool] = mapped_column(default=False)

    media: Mapped[List["Media"]] = relationship(back_populates="user")

    @property
    def is_admin(self):
        return self.user_id == settings.BOT_ADMIN_USER_ID
