from sqlalchemy.orm import Session
from opensnep.database.connection import engine
from opensnep.database.models import Base, Single

#creates table if missing
def create_tables() -> None:
    Base.metadata.create_all(engine)

#load data into
def load_singles(df) -> None:
    create_tables()

    records = []

    for _, row in df.iterrows():
        record = Single( 
            interprete=row["interprete"],
            interprete_principal=row["interprete_principal"],
            titre=row["titre"],
            editeur_distributeur=row["editeur_distributeur"],
            certification=row["certification"],
            date_sortie=row["date_sortie"],
            date_constat=row["date_constat"],
            source_page=row["source_page"],
            source_year=row["source_year"],
        )

        records.append(record)

    with Session(engine) as session:
        session.add_all(records)
        session.commit()

    print(f"{len(records)} rows inserted into singles table")
