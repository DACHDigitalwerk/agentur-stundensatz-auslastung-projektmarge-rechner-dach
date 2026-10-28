"""Rechtsstand 2026: Agentur- & Consulting-Stundensatz, Billable Utilization, KSK 5,0 % (§ 24 KSVG) & Projekt-DB I/II/III."""
from dataclasses import dataclass
from typing import Dict, Optional

KSK_RATE_DE_2026: float = 0.05
DEFAULT_ONCOST_FACTOR: Dict[str, float] = {"DE": 1.215, "AT": 1.305, "CH": 1.155}


@dataclass(frozen=True)
class AgencyProjectInput:
    country: str = "DE"  # "DE", "AT", "CH"
    annual_gross_salary: float = 72_000.0
    employer_oncost_factor: Optional[float] = None
    overhead_per_head: float = 24_000.0
    net_workdays: float = 218.0
    daily_hours: float = 8.0
    billable_utilization_pct: float = 70.0
    target_ebit_margin_pct: float = 20.0
    planned_project_hours: float = 180.0
    offered_hourly_rate: float = 125.0
    scope_creep_pct: float = 15.0
    external_freelancer_net: float = 6_000.0
    external_licenses_net: float = 1_200.0
    apply_ksk_de: bool = True


@dataclass(frozen=True)
class AgencyProjectResult:
    country: str
    currency: str
    employer_oncost_factor: float
    employer_labor_cost: float
    total_annual_cost_per_head: float
    billable_hours_per_year: float
    direct_labor_hourly_rate: float
    overhead_hourly_rate: float
    breakeven_hourly_rate: float
    target_hourly_rate: float
    target_day_rate: float
    ksk_fee: float
    total_project_revenue: float
    db1_agency_gross_income: float
    real_project_hours: float
    db2_planned: float
    db2_real: float
    db3_planned: float
    db3_real: float
    db3_margin_on_agi_pct: float
    effective_hourly_rate_real: float
    recommended_fixed_price_with_buffer: float
    target_margin_achieved: bool


def calculate_agency_margin(inp: AgencyProjectInput) -> AgencyProjectResult:
    c = inp.country.upper().strip()
    if c not in DEFAULT_ONCOST_FACTOR:
        raise ValueError(f"Unsupported country: {c}")
    if inp.annual_gross_salary <= 0 or inp.overhead_per_head < 0:
        raise ValueError("Invalid salary or overhead_per_head")
    if inp.net_workdays <= 0 or inp.daily_hours <= 0 or not (0.0 < inp.billable_utilization_pct <= 100.0):
        raise ValueError("Invalid working time or utilization parameters")
    if not (0.0 <= inp.target_ebit_margin_pct < 90.0):
        raise ValueError("target_ebit_margin_pct must be in [0, 90)")
    if inp.planned_project_hours <= 0 or inp.offered_hourly_rate <= 0 or inp.scope_creep_pct < 0:
        raise ValueError("Invalid project hours, rate, or scope_creep_pct")
    if inp.external_freelancer_net < 0 or inp.external_licenses_net < 0:
        raise ValueError("External costs must be non-negative")

    factor = DEFAULT_ONCOST_FACTOR[c] if inp.employer_oncost_factor is None else float(inp.employer_oncost_factor)
    if factor < 1.0:
        raise ValueError("employer_oncost_factor must be >= 1.0")

    currency = "CHF" if c == "CH" else "EUR"
    emp_cost = inp.annual_gross_salary * factor
    tot_cost = emp_cost + inp.overhead_per_head
    billable_hrs = inp.net_workdays * inp.daily_hours * (inp.billable_utilization_pct / 100.0)

    labor_rate = emp_cost / billable_hrs
    oh_rate = inp.overhead_per_head / billable_hrs
    be_rate = tot_cost / billable_hrs
    margin_div = 1.0 - (inp.target_ebit_margin_pct / 100.0)
    target_rate = be_rate / margin_div
    target_day = target_rate * inp.daily_hours

    ksk_fee = (inp.external_freelancer_net * KSK_RATE_DE_2026) if (c == "DE" and inp.apply_ksk_de) else 0.0
    internal_rev = inp.planned_project_hours * inp.offered_hourly_rate
    total_rev = internal_rev + inp.external_freelancer_net + inp.external_licenses_net
    ext_total = inp.external_freelancer_net + inp.external_licenses_net + ksk_fee

    db1 = total_rev - ext_total
    real_hrs = inp.planned_project_hours * (1.0 + inp.scope_creep_pct / 100.0)

    db2_plan = db1 - (inp.planned_project_hours * labor_rate)
    db2_real = db1 - (real_hrs * labor_rate)

    db3_plan = db2_plan - (inp.planned_project_hours * oh_rate)
    db3_real = db2_real - (real_hrs * oh_rate)

    db3_margin_pct = ((db3_real / db1) * 100.0) if db1 > 0 else -100.0
    ehr_real = db1 / real_hrs
    rec_fixed = (real_hrs * target_rate) + (ext_total / margin_div)

    return AgencyProjectResult(
        country=c,
        currency=currency,
        employer_oncost_factor=round(factor, 4),
        employer_labor_cost=round(emp_cost, 2),
        total_annual_cost_per_head=round(tot_cost, 2),
        billable_hours_per_year=round(billable_hrs, 2),
        direct_labor_hourly_rate=round(labor_rate, 2),
        overhead_hourly_rate=round(oh_rate, 2),
        recommended_fixed_price_with_buffer=round(rec_fixed, 2),
        breakeven_hourly_rate=round(be_rate, 2),
        target_hourly_rate=round(target_rate, 2),
        target_day_rate=round(target_day, 2),
        ksk_fee=round(ksk_fee, 2),
        total_project_revenue=round(total_rev, 2),
        db1_agency_gross_income=round(db1, 2),
        real_project_hours=round(real_hrs, 2),
        db2_planned=round(db2_plan, 2),
        db2_real=round(db2_real, 2),
        db3_planned=round(db3_plan, 2),
        db3_real=round(db3_real, 2),
        db3_margin_on_agi_pct=round(db3_margin_pct, 2),
        effective_hourly_rate_real=round(ehr_real, 2),
        target_margin_achieved=(db3_margin_pct + 1e-6 >= inp.target_ebit_margin_pct),
    )
