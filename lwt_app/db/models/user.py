from sqlalchemy import BigInteger
from sqlalchemy.sql import func, cast, text
from core.database import BaseModel
from sqlalchemy.orm import mapped_column, Mapped
from datetime import datetime, date


class User(BaseModel):
    __tablename__ = 'users'

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
    )
    username: Mapped[str] = mapped_column(default="")
