import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import db


class User(db.Model):
    id: Mapped[int] = mapped_column(
        sa.Integer,
        primary_key=True,
        autoincrement=True,
    )
    username: Mapped[str] = mapped_column(
        sa.String,
        unique=True,
        nullable=False,
    )
    password: Mapped[str] = mapped_column(
        sa.String,
        nullable=False,
    )
    active: Mapped[bool] = mapped_column(
        sa.Boolean,
        default=True,
    )
    role_id: Mapped[int] = mapped_column(
        sa.Integer,
        sa.ForeignKey("role.id"),
        nullable=True,
    )
    role: Mapped["Role"] = relationship("Role", back_populates="users")

    def __repr__(self) -> str:
        return (
            f"User("
            f"id={self.id!r},\n"
            f"username={self.username!r},\n"
            f"active={self.active!r},\n"
            f"role={self.role!r}"
            ")"
        )
