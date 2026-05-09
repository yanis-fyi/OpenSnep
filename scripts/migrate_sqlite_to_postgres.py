import os
import pandas as pd
from sqlalchemy import create_engine

from opensnep.database.models import Base

sqlite_engine = create_engine("sqlite:///data/opensnep.db")

postgres_url = os.environ["DATABASE_URL"]
postgres_engine = create_engine(postgres_url)

print("Source:", sqlite_engine.url)
print("Destination:", postgres_engine.url)

Base.metadata.drop_all(postgres_engine)
Base.metadata.create_all(postgres_engine)

for table in ["certifications", "charts"]:
    df = pd.read_sql_table(table, sqlite_engine)

    print(f"Migrating {table}: {len(df)} rows")

    df.to_sql(
        table,
        postgres_engine,
        if_exists="append",
        index=False,
        chunksize=500,
    )

print("Migration complete")