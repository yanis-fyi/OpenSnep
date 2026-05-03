from sqlalchemy import func
from sqlalchemy.orm import Session

from opensnep.database.connection import engine
from opensnep.database.models import Certification

#count rows
def count_singles() -> int:
    with Session(engine) as session:
        return session.query(Certification).count()
    
#query db by artist name    
def get_artist(name: str) -> list[Certification]:
    with Session(engine) as session:
        return (
            session.query(Certification)
            .filter(Certification.interprete.ilike(f"{name}%"))
            .all()
        )

#find artists who appear often (top 10)
def top_artists(limit: int = 10) -> list[tuple[str, int]]:
    with Session(engine) as session:
        return (
            session.query(
                Certification.interprete_principal,
                func.count(Certification.id).label("count")
            )
            .group_by(Certification.interprete_principal)
            .order_by(func.count(Certification.id).desc())
            .limit(limit)
            .all()
        )
    
#find song titles
def search_title(keyword: str) -> list[Certification]:
    with Session(engine) as session:
        return (
            session.query(Certification)
            .filter(Certification.titre.ilike(f"%{keyword}%"))
            .all()
        )
        
#find nbr of certifications by type for artist
def artist_certifications(name: str) -> list[tuple[str, int]]:
    with Session(engine) as session:
        return (
            session.query(
                Certification.certification,
                func.count(Certification.id).label("count")
        )
        .filter(Certification.interprete_principal.ilike(f"%{name}%"))
        .group_by(Certification.certification)
        .order_by(func.count(Certification.id).desc())
        .all()
        )
