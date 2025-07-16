from sqlalchemy import BigInteger
from core.database import BaseModel
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import List, TYPE_CHECKING

from core.config import settings

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
