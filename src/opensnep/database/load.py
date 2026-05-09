from sqlalchemy.orm import Session
from opensnep.database.connection import engine
from opensnep.database.models import Base, Certification, ChartEntry

#creates table if missing
def create_tables() -> None:
    Base.metadata.create_all(engine)

#load certifications
def load_certifications(df) -> None:
    create_tables()

    if df.empty:
        print("No rows to load")
        return
    
    df = df.drop_duplicates(
    subset=[
        "interprete",
        "titre",
        "certification",
        "categorie",
        "date_constat",
    ]
    ).copy()
    source_year = int(df["source_year"].iloc[0])
    source_category = df["categorie"].iloc[0]

    records = []

    for _, row in df.iterrows():
        record = Certification( 
            interprete=row["interprete"],
            interprete_principal=row["interprete_principal"],
            titre=row["titre"],
            editeur_distributeur=row["editeur_distributeur"],
            certification=row["certification"],
            categorie=row["categorie"],
            date_sortie=row["date_sortie"],
            date_constat=row["date_constat"],
            source_page=row["source_page"],
            source_year=row["source_year"],
        )

        records.append(record)

    with Session(engine) as session:
        deleted = (
            session.query(Certification)
            .filter(Certification.source_year == source_year)
            .filter(Certification.categorie == source_category)
            .delete()
        )
        session.add_all(records)
        session.commit()

    print(f"Replaced {deleted} existing rows for {source_year}")
    print(f"{len(records)} rows inserted into certifications table")

#load chart entries
def load_chart_entries(df) -> None:
    create_tables()

    if df.empty:
        print("No entries to load")
        return
    
   
    
    chart_name = df["chart_name"].iloc[0]
    year = int(df["year"].iloc[0])
    week = int(df["week"].iloc[0])

    records = []

    for _, row in df.iterrows():
        record = ChartEntry(
            chart_name=row["chart_name"],
            rank=row["rank"],
            artist=row["artist"],
            title=row["title"],
            label_distributor=row["label_distributor"],
            week=row["week"],
            year=row["year"],
        )
        records.append(record)

    with Session(engine) as session:
        deleted = (
            session.query(ChartEntry)
            .filter(ChartEntry.chart_name == chart_name)
            .filter(ChartEntry.year == year)
            .filter(ChartEntry.week == week)
            .delete()
        )
        session.add_all(records)
        session.commit()

    print(f"Replaced {deleted} rows for "
          f"{chart_name} | {year} | week {week}"
          )
    print(f"{len(records)} rows inserted")
