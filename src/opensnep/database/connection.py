from pathlib import Path
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DATABASE_PATH = PROJECT_ROOT / os.getenv(
    "DATABASE_PATH",
    "./data/opensnep.db",
)

DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

engine = create_engine(
    DATABASE_URL,
    echo=False,
)
