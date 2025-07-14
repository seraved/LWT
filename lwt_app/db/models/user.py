from sqlalchemy import BigInteger
from core.database import BaseModel
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .media import Media


class User(BaseModel):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )
    username: Mapped[str] = mapped_column(default="")

    media: Mapped[List["Media"]] = relationship(back_populates="user")
