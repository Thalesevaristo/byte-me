from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from .base import db


class Post(db.Model):
    id: Mapped[int] = mapped_column(
        sa.Integer,
        primary_key=True,
        autoincrement=True,
    )
    title: Mapped[str] = mapped_column(
        sa.String,
        nullable=False,
    )
    body: Mapped[str] = mapped_column(
        sa.String,
        nullable=False,
    )
    created: Mapped[datetime] = mapped_column(
        sa.DateTime,
        server_default=sa.func.now(),
    )
    author_id: Mapped[int] = mapped_column(
        sa.ForeignKey("user.id"),
    )

    def __repr__(self) -> str:
        return (
            f"Post(\n"
            f"id={self.id!r},\n"
            f"title={self.title!r},\n"
            f"author_id={self.author_id!r}\n"
            ")"
        )
