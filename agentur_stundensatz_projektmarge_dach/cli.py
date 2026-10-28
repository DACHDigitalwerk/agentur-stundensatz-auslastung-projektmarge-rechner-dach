import argparse
import json
from dataclasses import asdict
from .calculator import AgencyProjectInput, calculate_agency_margin


def main() -> None:
    p = argparse.ArgumentParser(description="DACH Agentur-Stundensatz-, Auslastungs- & Projektmarge-Rechner 2026")
    p.add_argument("--country", default="DE", choices=["DE", "AT", "CH"])
    p.add_argument("--salary", type=float, default=72000.0)
    p.add_argument("--utilization", type=float, default=70.0)
    p.add_argument("--hours", type=float, default=180.0)
    p.add_argument("--rate", type=float, default=125.0)
    args = p.parse_args()
    res = calculate_agency_margin(
        AgencyProjectInput(
            country=args.country,
            annual_gross_salary=args.salary,
            billable_utilization_pct=args.utilization,
            planned_project_hours=args.hours,
            offered_hourly_rate=args.rate,
        )
    )
    print(json.dumps(asdict(res), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
