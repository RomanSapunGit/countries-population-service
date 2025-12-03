from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.databases.base import Base


class CountryModel(Base):
    __tablename__ = "countries"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    name: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        unique=True
    )
    region: Mapped[str] = mapped_column(
        String(32),
        nullable=False
    )

    population: Mapped[int] = mapped_column(Integer, nullable=False)

    def __repr__(self):
        return (
            f"<CountryModel(id={self.id}, name={self.name}, "
            f"region={self.region}, "
            f"population={self.population})>"
        )
