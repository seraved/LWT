from sqlalchemy import Column, Integer, String, Boolean, Enum, DateTime, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from core.database import BaseModel
from typing import TYPE_CHECKING

from entities.media import MediaType

if TYPE_CHECKING:
    from .user import User


class Media(BaseModel):
    __tablename__ = "media"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    media_type: Mapped[MediaType] = mapped_column(Enum(MediaType))
    watched: Mapped[bool] = mapped_column(Boolean, default=False)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="media")
