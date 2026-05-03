from sqlalchemy import func
from sqlalchemy.orm import Session

from opensnep.database.connection import engine
from opensnep.database.models import Certification


def count_certifications(category: str | None = None) -> int:
    with Session(engine) as session:
        query = session.query(Certification)

        if category:
            query = query.filter(Certification.categorie == category)

        return query.count()


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


def count_by_year(category: str | None = None) -> list[tuple[int, int]]:
    with Session(engine) as session:
        query = session.query(
            Certification.source_year,
            func.count(Certification.id).label("count"),
        )

        if category:
            query = query.filter(Certification.categorie == category)

        return (
            query
            .group_by(Certification.source_year)
            .order_by(Certification.source_year.desc())
            .all()
        )


def get_artist(name: str, category: str | None = None) -> list[Certification]:
    with Session(engine) as session:
        query = session.query(Certification).filter(
            Certification.interprete.ilike(f"%{name}%")
        )

        if category:
            query = query.filter(Certification.categorie == category)

        return query.all()


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
            query = query.filter(Certification.categorie == category)

        return (
            query
            .group_by(Certification.interprete_principal)
            .order_by(func.count(Certification.id).desc())
            .limit(limit)
            .all()
        )


def search_title(
    keyword: str,
    category: str | None = None,
) -> list[Certification]:
    with Session(engine) as session:
        query = session.query(Certification).filter(
            Certification.titre.ilike(f"%{keyword}%")
        )

        if category:
            query = query.filter(Certification.categorie == category)

        return query.all()


def artist_certifications(
    name: str,
    category: str | None = None,
) -> list[tuple[str, int]]:
    with Session(engine) as session:
        query = session.query(
            Certification.certification,
            func.count(Certification.id).label("count"),
        ).filter(
            Certification.interprete_principal.ilike(f"%{name}%")
        )

        if category:
            query = query.filter(Certification.categorie == category)

        return (
            query
            .group_by(Certification.certification)
            .order_by(func.count(Certification.id).desc())
            .all()
        )
