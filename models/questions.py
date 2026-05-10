from datetime import datetime

from sqlalchemy import String, Text, DateTime, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base


class Question(Base):
    __tablename__ = "questions"

    title: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    category_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("category.id"),
        nullable=False
    )

    category: Mapped["Category"] = relationship(
        "Category",
        back_populates="questions"
    )

    answers: Mapped[list["Answer"]] = relationship(
        "Answer",
        back_populates="question"
    )

    statistics: Mapped["QuestionStatistics"] = relationship(
        "QuestionStatistics",
        back_populates="question"
    )


class QuestionOption(Base):
    __tablename__ = "question_options"

    question_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("questions.id"),
        nullable=False
    )

    text: Mapped[str] = mapped_column(String(255), nullable=False)

    answers: Mapped[list["Answer"]] = relationship(
        "Answer",
        back_populates="option"
    )

    option_statistics: Mapped[list["OptionStatistics"]] = relationship(
        "OptionStatistics"
    )