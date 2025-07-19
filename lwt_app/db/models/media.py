from typing import TYPE_CHECKING

from entities.enum import MediaTypeEnum
from sqlalchemy import (
    BigInteger,
    Boolean,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import BaseModel

if TYPE_CHECKING:
    from .user import User


class Media(BaseModel):
    __tablename__ = "media"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    media_type: Mapped[MediaTypeEnum] = mapped_column(Enum(MediaTypeEnum))
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    poster_url: Mapped[str] = mapped_column(String(255), default="")
    series_length: Mapped[int] = mapped_column(Integer, default=1)
    kinopoisk_id: Mapped[int] = mapped_column(Integer, default=0)
    genres: Mapped[str] = mapped_column(Text, default="")
    watched: Mapped[bool] = mapped_column(Boolean, default=False)
    is_delete: Mapped[bool] = mapped_column(Boolean, default=False)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="media")
