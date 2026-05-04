from sqlalchemy import func
from sqlalchemy.orm import Session

from opensnep.database.connection import engine
from opensnep.database.models import Certification

#count total certifications per category
def count_certifications(category: str | None = None) -> int:
    with Session(engine) as session:
        query = session.query(Certification)

        if category:
            query = query.filter(func.lower(Certification.categorie) == category.lower())

        return query.count()

#count certifications by category
def count_by_category() -> list[tuple[str, int]]:
    with Session(engine) as session:
        return (
            session.query(
                Certification.categorie,
                func.count(Certification.id).label("count"),
            )
            .group_by(Certification.categorie)
            .order_by(func.count(Certification.id).desc())
            .all()
        )


#count nbr of certifications per year and category 
def count_by_year(category: str | None = None) -> list[tuple[int, int]]:
    with Session(engine) as session:
        query = session.query(
            Certification.source_year,
            func.count(Certification.id).label("count"),
        )

        if category:
            query = query.filter(func.lower(Certification.categorie) == category.lower())

        return (
            query
            .group_by(Certification.source_year)
            .order_by(Certification.source_year.desc())
            .all()
        )

#get list of top artists by category certifications
def top_artists(
    limit: int = 10,
    category: str | None = None,
) -> list[tuple[str, int]]:
    with Session(engine) as session:
        query = session.query(
            Certification.interprete_principal,
            func.count(Certification.id).label("count"),
        )

        if category:
            query = query.filter(func.lower(Certification.categorie) == category.lower())

        return (
            query
            .group_by(Certification.interprete_principal)
            .order_by(func.count(Certification.id).desc())
            .limit(limit)
            .all()
        )

#get top editeurs/distributeurs 
def top_distributors(category: str | None = None, limit: int = 10) -> list[tuple[str, int]]:
    with Session(engine) as session:
        query = session.query(
            Certification.editeur_distributeur,
            func.count(Certification.id).label("count")
        )
        if category:
            query = query.filter(func.lower(Certification.categorie) == category.lower())

        return(
            query
            .group_by(Certification.editeur_distributeur)
            .order_by(func.count(Certification.id).desc())
            .limit(limit)
            .all()
        )
    

#find artist's certifications
def artist_certifications(
    name: str,
    category: str | None = None,
) -> list[tuple[str, int]]:
    with Session(engine) as session:
        query = session.query(
            Certification.certification,
            func.count(Certification.id).label("count"),
        ).filter(
            func.lower(Certification.interprete_principal) == name.lower()
        )

        if category:
            query = query.filter(func.lower(Certification.categorie) == category.lower())

        return (
            query
            .group_by(Certification.certification)
            .order_by(func.count(Certification.id).desc())
            .all()
        )

           
#get certification api
def search_certifications(
        artist: str | None = None,
        title: str | None = None,
        category: str | None = None,
        year: int | None = None,
        certification: str | None = None, 
) -> list[Certification]:
    with Session(engine) as session:
        query = session.query(Certification)

        if artist:
            query = query.filter(
                func.lower(Certification.interprete_principal) == artist.lower()
            )

        if title:
            query = query.filter(
                Certification.titre.ilike(f"%{title}%")
            )

        if category:
            query = query.filter(
                func.lower(Certification.categorie) == category.lower()
            )

        if year:
            query = query.filter(
                Certification.source_year == year
            )

        if certification:
            query = query.filter(
                func.lower(Certification.certification) == certification.lower()
            )

        return query.all()
