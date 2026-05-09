import time

from opensnep.ingestion.charts import crawl_chart, CHART_CATEGORIES
from opensnep.cleaning.charts import clean_charts
from opensnep.database.load import load_chart_entries


START_YEAR = 2018
END_YEAR = 2026
SLEEP_SECONDS = 2


def backfill_charts() -> None:
    failed = []

    for chart_name in CHART_CATEGORIES:
        for year in range(START_YEAR, END_YEAR + 1):
            for week in range(1, 53):
                try:
                    print(f"Backfilling {chart_name} | {year} week {week}")

                    df_raw = crawl_chart(
                        chart_name=chart_name,
                        year=year,
                        week=week,
                    )

                    df_clean = clean_charts(df_raw)
                    load_chart_entries(df_clean)

                    time.sleep(SLEEP_SECONDS)

                except Exception as e:
                    print(f"FAILED {chart_name} | {year} week {week}: {e}")
                    failed.append((chart_name, year, week, str(e)))

    print("Backfill finished")
    print("Total failures:", len(failed))
    print("Failed:", failed[:50])


if __name__ == "__main__":
    backfill_charts()