from sqlalchemy import func
from sqlalchemy.orm import Session

from opensnep.database.connection import engine
from opensnep.database.models import Certification, ChartEntry

# ======================
# Certifications queries
# ======================

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


#get certifaction levels
def certification_by_levels(category: str | None = None) -> list[tuple[str, int]]:
    with Session(engine) as session:
            query = session.query(
                Certification.certification,
                func.count(Certification.id).label("count")
            )
            if category:
                query = query.filter(func.lower(Certification.categorie) == category.lower)

            return(
            query
            .group_by(Certification.certification)
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

def get_artist(
        name: str,
        category: str | None = None,
) -> list[Certification]:
    with Session(engine) as session:
        query = session.query(Certification).filter(
            func.lower(Certification.interprete_principal) == name.lower()
        )
        if category:
            query = query.filter(
                func.lower(Certification.categorie) == category.lower()
            )

        return query.all()
    
# ===============
# Charts queries
# ===============

#count chart rows by chart_name
def count_chart_entries(chart_name: str | None = None) -> int:
    with Session(engine) as session:
        query = session.query(ChartEntry)

        if chart_name:
            query = query.filter(func.lower(ChartEntry.chart_name) == chart_name.lower())
        
        return query.count()

#generic search of charts
def search_charts(
        chart_name: str | None = None,
        rank: int | None = None,
        artist: str | None = None,
        title: str | None = None,
        label_distributor: str | None = None,
        week: int | None = None,
        year: int | None = None,
                  
) -> list[ChartEntry]:
    with Session(engine) as session:
        query = session.query(ChartEntry)

        if chart_name:
            query = query.filter(
                func.lower(ChartEntry.chart_name) == chart_name.lower())
            
        if rank:
            query = query.filter(
                ChartEntry.rank == rank)
            
        if artist:
            query = query.filter(
                func.lower(ChartEntry.artist) == artist.lower())
            
        if title:
            query = query.filter(
                func.lower(ChartEntry.title) == title.lower())
            
        if label_distributor:
            query = query.filter(
                func.lower(ChartEntry.label_distributor) == label_distributor.lower())
            
        if week:
            query = query.filter(
                ChartEntry.week == week)
            
        if year:
            query = query.filter(
                ChartEntry.year == year)
            
        return query.all()

# get one chart snapshot
def get_chart_week(
        chart_name: str,
        week: int,
        year: int,
) -> list[ChartEntry]:
    with Session(engine) as session:
        return (
            session.query(ChartEntry)
            .filter(func.lower(ChartEntry.chart_name) == chart_name.lower())
            .filter(ChartEntry.week == week)
            .filter(ChartEntry.year == year)
            .order_by(ChartEntry.rank.asc())
            .all()
        )
    
# get top chart artists - most appearances in top 200 charts
def top_chart_artists(
        chart_name: str | None = None,
        limit: int=10,
) -> list[tuple[str, int]]:
    with Session(engine) as session:
        query = session.query(
            ChartEntry.artist,
            func.count(ChartEntry.id).label("count"),
        )
        if chart_name:
            query = query.filter(func.lower(chart_name) == chart_name.lower())
        
        return (
            query
            .group_by(ChartEntry.artist)
            .order_by(func.count(ChartEntry.id).desc())
            .limit(limit)
            .all()
        )
    
# get top chart label/distributors
def top_chart_distributors(
        chart_name: str | None = None,
        limit: int = 10,
) -> list[tuple[str, int]]:
    with Session(engine) as session:
        query = session.query(
            ChartEntry.label_distributor,
            func.count(ChartEntry.id).label("count"),
        )
        if chart_name:
            query = query.filter(func.lower(chart_name) == chart_name.lower)

        return (
            query
            .group_by(ChartEntry.label_distributor)
            .order_by(func.count(ChartEntry.id).desc())
            .limit(limit)
            .all()
        )
# find nbr of weeks at number one
def entries_at_number_one(
    artist: str | None = None,
    chart_name: str | None = None,
    limit: int = 10,
) -> int | list[tuple[str, int]]:
    with Session(engine) as session:
        query = session.query(ChartEntry).filter(
            ChartEntry.rank == 1
        )

        if chart_name:
            query = query.filter(
                func.lower(ChartEntry.chart_name) == chart_name.lower()
            )

        if artist:
            return (
                query
                .filter(func.lower(ChartEntry.artist) == artist.lower())
                .count()
            )

        return (
            query
            .with_entities(
                ChartEntry.artist,
                func.count(ChartEntry.id).label("count"),
            )
            .group_by(ChartEntry.artist)
            .order_by(func.count(ChartEntry.id).desc())
            .limit(limit)
            .all()
        )
# get artist chart history
def artist_chart_history(
    artist: str,
    chart_name: str | None = None,
) -> list[ChartEntry]:
    with Session(engine) as session:
        query = session.query(ChartEntry).filter(
            func.lower(ChartEntry.artist) == artist.lower()
        )

        if chart_name:
            query = query.filter(
                func.lower(ChartEntry.chart_name) == chart_name.lower()
            )

        return (
            query
            .order_by(
                ChartEntry.year.asc(),
                ChartEntry.week.asc(),
                ChartEntry.rank.asc(),
            )
            .all()
        )

        