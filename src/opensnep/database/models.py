from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone

#create the parent class
class Base(DeclarativeBase):
    pass

#Define one table
class Single(Base): 
    __tablename__ = "singles"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    interprete: Mapped[str] = mapped_column(String)
    titre: Mapped[str] = mapped_column(String)
    editeur_distributeur: Mapped[str] = mapped_column(String)
    certification: Mapped[str] = mapped_column(String)

    date_sortie: Mapped[datetime] = mapped_column(DateTime)
    date_constat: Mapped[datetime] = mapped_column(DateTime)

    source_page: Mapped[int] = mapped_column(Integer)
    source_year: Mapped[int] = mapped_column(Integer)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

