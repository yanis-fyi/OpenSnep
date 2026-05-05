from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone

#create the parent class
class Base(DeclarativeBase):
    pass

#Define certifications table
class Certification(Base): 
    __tablename__ = "certifications"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    interprete: Mapped[str] = mapped_column(String)
    interprete_principal: Mapped[str] = mapped_column(String)
    titre: Mapped[str] = mapped_column(String)
    editeur_distributeur: Mapped[str | None] = mapped_column(String, nullable=True)
    certification: Mapped[str] = mapped_column(String)
    categorie: Mapped[str] = mapped_column(String)

    date_sortie: Mapped[datetime] = mapped_column(DateTime)
    date_constat: Mapped[datetime] = mapped_column(DateTime)

    source_page: Mapped[int] = mapped_column(Integer)
    source_year: Mapped[int] = mapped_column(Integer)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )
    #representation of an object    
    def __repr__(self) -> str:
        return (
            f"<Certification("
            f"interprete='{self.interprete}', "
            f"interprete_principal='{self.interprete_principal}', "
            f"titre='{self.titre}', "
            f"certification='{self.certification}', "
            f"categorie='{self.categorie}'"
            f")>"
        )

#define charts table
class ChartEntry(Base):
    __tablename__ = "charts"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    chart_name: Mapped[str] = mapped_column(String)
    rank: Mapped[int] = mapped_column(Integer)

    artist: Mapped[str] = mapped_column(String)
    title: Mapped[str] = mapped_column(String)
    label_distributor: Mapped[str | None] = mapped_column(String, nullable=True)

    week: Mapped[int] = mapped_column(Integer)
    year: Mapped[int] = mapped_column(Integer)

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc)
    )
    #representation of an object charts
    def __repr__(self) -> str:
        return (
            f"<ChartEntry("
            f"chart_name='{self.chart_name}', "
            f"rank={self.rank}, "
            f"artist='{self.artist}', "
            f"title='{self.title}'"
            f")>"
    )