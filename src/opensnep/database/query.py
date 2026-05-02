from sqlalchemy import func
from sqlalchemy.orm import Session

from opensnep.database.connection import engine
from opensnep.database.models import Single

#count rows
def count_singles() -> int:
    with Session(engine) as session:
        return session.query(Single).count()
    
#query db by artist name    
def get_artist(name: str) -> list[Single]:
    with Session(engine) as session:
        return (
            session.query(Single)
            .filter(Single.interprete.ilike(f"{name}%"))
            .all()
        )

#find artists who appear often (top 10)
def top_artists(limit: int = 10) -> list[tuple[str, int]]:
    with Session(engine) as session:
        return (
            session.query(
                Single.interprete_principal,
                func.count(Single.id).label("count")
            )
            .group_by(Single.interprete_principal)
            .order_by(func.count(Single.id).desc())
            .limit(limit)
            .all()
        )
    
#find song titles
def search_title(keyword: str) -> list[Single]:
    with Session(engine) as session:
        return (
            session.query(Single)
            .filter(Single.titre.ilike(f"%{keyword}%"))
            .all()
        )
        
#find nbr of certifications by type for artist
def artist_certifications(name: str) -> list[tuple[str, int]]:
    with Session(engine) as session:
        return (
            session.query(
                Single.certification,
                func.count(Single.id).label("count")
        )
        .filter(Single.interprete_principal.ilike(f"%{name}%"))
        .group_by(Single.certification)
        .order_by(func.count(Single.id).desc())
        .all()
        )
