from scripts.update_certifications import main as update_certifications
from scripts.update_charts import main as update_charts


def main():
    print("Updating certifications...")
    cert_failures = update_certifications()

    if cert_failures:
        raise RuntimeError(
            f"Certification update failed: {cert_failures}"
        )

    print("Updating charts...")
    chart_failures = update_charts()

    if chart_failures:
        raise RuntimeError(
            f"Chart update failed: {chart_failures}"
        )

    print("Done.")


if __name__ == "__main__":
    main()