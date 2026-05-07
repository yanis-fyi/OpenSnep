import logging
import time
from datetime import date
from pathlib import Path

from opensnep.ingestion.certifications import crawl_certifications
from opensnep.cleaning.certifications import clean_certifications
from opensnep.database.load import load_certifications


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "update_certifications.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


CATEGORIES = ["Singles", "Albums"]


def update_certifications(year: int) -> list[tuple[str, int, str]]:
    failed = []

    for category in CATEGORIES:
        try:
            message = f"Updating certifications | {category} | {year}"
            print(message)
            logging.info(message)

            df_raw = crawl_certifications(
                year=year,
                category=category,
                sleep_seconds=1,
            )

            df_clean = clean_certifications(df_raw)
            load_certifications(df_clean)

            time.sleep(2)

        except Exception as e:
            message = f"FAILED certifications | {category} | {year}: {e}"
            print(message)
            logging.error(message)
            failed.append((category, year, str(e)))

    message = f"Failed: {failed}"
    print(message)
    logging.info(message)

    return failed


if __name__ == "__main__":
    logging.info("=" * 60)
    logging.info("STARTING CERTIFICATIONS UPDATE")
    logging.info("=" * 60)

    current_year = date.today().year

    update_certifications(year=current_year)

    logging.info("=" * 60)
    logging.info("CERTIFICATIONS UPDATE FINISHED")
    logging.info("=" * 60)