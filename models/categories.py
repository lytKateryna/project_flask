from models.base import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Category(Base):
    __tablename__ = 'category'

    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    questions: Mapped[list["Question"]] = relationship(
        "Question", back_populates="category")