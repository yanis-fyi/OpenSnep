from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone

#create the parent class
class Base(DeclarativeBase):
    pass

#Define one table
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
            f"certification='{self.certification}'"
            f")>"
        )
