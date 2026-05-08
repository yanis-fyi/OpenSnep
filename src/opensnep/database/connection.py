from pathlib import Path
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

db_path = os.getenv("DATABASE_PATH", "./data/opensnep.db")
DATABASE_PATH = Path(db_path)

if not DATABASE_PATH.is_absolute():
    PROJECT_ROOT = Path(__file__).resolve().parents[3]
    DATABASE_PATH = PROJECT_ROOT / DATABASE_PATH

DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

engine = create_engine(
    DATABASE_URL,
    echo=False,
)