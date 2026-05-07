import time

from opensnep.ingestion.charts import crawl_chart
from opensnep.cleaning.charts import clean_charts
from opensnep.database.load import load_chart_entries

failed = []
chart_name = "Top Radio"

for year in range(2018, 2027):
    for week in range(1, 53):
        try:
            print(f"Backfilling {chart_name} | {year} week {week}")

            df_raw = crawl_chart(chart_name, year, week)
            df_clean = clean_charts(df_raw)
            load_chart_entries(df_clean)

            time.sleep(2)

        except Exception as e:
            print(f"FAILED {chart_name} | {year} week {week}: {e}")
            failed.append((chart_name, year, week, str(e)))

print("Failed:", failed)
print("Total failures:", len(failed))