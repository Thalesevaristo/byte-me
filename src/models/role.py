import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import db

class Role(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(sa.String, unique=True, nullable=False)
    users: Mapped[list["user.User"]] = relationship("User", back_populates="role")

    def __repr__(self) -> str:
        return f"Role(id={self.id!r}, name={self.name!r})"
