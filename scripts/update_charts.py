import time
from datetime import date
from pathlib import Path
import logging

from opensnep.ingestion.charts import crawl_chart, CHART_CATEGORIES
from opensnep.cleaning.charts import clean_charts
from opensnep.database.load import load_chart_entries

PROJECT_ROOT = Path(__file__).resolve().parents[1]
LOG_DIR = PROJECT_ROOT / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "update_charts.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

def update_charts(year: int, week: int) -> list[tuple[str, int, int, str]]:
    failed = []

    for chart_name in CHART_CATEGORIES:
        try:
            message = f"Updating {chart_name} | {year} week {week}"
            print(message)
            logging.info(message)

            df_raw = crawl_chart(chart_name, year, week)
            df_clean = clean_charts(df_raw)
            load_chart_entries(df_clean)

            time.sleep(2)

        except Exception as e:
            message = f"FAILED {chart_name} | {year} week {week}: {e}"
            print(message)
            logging.error(message)
            failed.append((chart_name, year, week, str(e)))

    message= f"Failed: {failed}"
    print(message)
    logging.info(message)

    return failed


if __name__ == "__main__":
    logging.info("=" * 60)
    logging.info("STARTING CHART UPDATE")
    logging.info("=" * 60)

    today = date.today()
    year, week, _ = today.isocalendar()
    
    failed = update_charts(year=year, week=week)

    if len(failed) == len(CHART_CATEGORIES):
        message= "Current week unavailable, trying previous week..."
        print(message)
        logging.warning(message)

        update_charts(year=year, week=week - 1)
    
    logging.info("=" * 60)
    logging.info("CHART UPDATE FINISHED")
    logging.info("=" * 60)