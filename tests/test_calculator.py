import pytest
from agentur_stundensatz_projektmarge_dach import (
    KSK_RATE_DE_2026,
    AgencyProjectInput,
    calculate_agency_margin,
)


def test_ksk_rate_de_2026_is_five_percent():
    assert KSK_RATE_DE_2026 == 0.05
    res = calculate_agency_margin(AgencyProjectInput(country="DE", external_freelancer_net=12_000.0, apply_ksk_de=True))
    assert res.ksk_fee == 600.0


def test_ksk_not_charged_in_austria_or_switzerland():
    at = calculate_agency_margin(AgencyProjectInput(country="AT", external_freelancer_net=10_000.0, apply_ksk_de=True))
    ch = calculate_agency_margin(AgencyProjectInput(country="CH", external_freelancer_net=10_000.0, apply_ksk_de=True))
    assert at.ksk_fee == 0.0
    assert ch.ksk_fee == 0.0
    assert ch.currency == "CHF"


def test_breakeven_and_target_hourly_rate_formula():
    res = calculate_agency_margin(
        AgencyProjectInput(
            country="DE",
            annual_gross_salary=60_000.0,
            employer_oncost_factor=1.20,
            overhead_per_head=28_000.0,
            net_workdays=200.0,
            daily_hours=8.0,
            billable_utilization_pct=62.5,
            target_ebit_margin_pct=20.0,
        )
    )
    # Total cost = 60k * 1.2 + 28k = 100,000; billable hours = 200 * 8 * 0.625 = 1,000 h
    assert res.total_annual_cost_per_head == 100_000.0
    assert res.billable_hours_per_year == 1_000.0
    assert res.breakeven_hourly_rate == 100.0
    assert res.target_hourly_rate == 125.0
    assert res.target_day_rate == 1_000.0


def test_zero_scope_creep_and_no_ksk_matches_target_ebit_margin():
    res = calculate_agency_margin(
        AgencyProjectInput(
            country="DE",
            annual_gross_salary=60_000.0,
            employer_oncost_factor=1.20,
            overhead_per_head=28_000.0,
            net_workdays=200.0,
            daily_hours=8.0,
            billable_utilization_pct=62.5,
            target_ebit_margin_pct=20.0,
            planned_project_hours=100.0,
            offered_hourly_rate=125.0,
            scope_creep_pct=0.0,
            external_freelancer_net=0.0,
            external_licenses_net=0.0,
            apply_ksk_de=False,
        )
    )
    assert res.db1_agency_gross_income == 12_500.0
    assert res.db2_real == 5_300.0
    assert res.db3_real == 2_500.0
    assert res.db3_margin_on_agi_pct == 20.0
    assert res.target_margin_achieved is True


def test_scope_creep_erodes_db3_and_effective_hourly_rate():
    no_creep = calculate_agency_margin(AgencyProjectInput(scope_creep_pct=0.0))
    high_creep = calculate_agency_margin(AgencyProjectInput(scope_creep_pct=35.0))
    assert high_creep.real_project_hours > no_creep.real_project_hours
    assert high_creep.db3_real < no_creep.db3_real
    assert high_creep.effective_hourly_rate_real < no_creep.effective_hourly_rate_real


def test_lower_utilization_increases_required_day_rate():
    high_u = calculate_agency_margin(AgencyProjectInput(billable_utilization_pct=80.0))
    low_u = calculate_agency_margin(AgencyProjectInput(billable_utilization_pct=55.0))
    assert low_u.breakeven_hourly_rate > high_u.breakeven_hourly_rate
    assert low_u.target_day_rate > high_u.target_day_rate


def test_austria_higher_default_oncost_factor_than_de_and_ch():
    de = calculate_agency_margin(AgencyProjectInput(country="DE"))
    at = calculate_agency_margin(AgencyProjectInput(country="AT"))
    ch = calculate_agency_margin(AgencyProjectInput(country="CH"))
    assert at.employer_oncost_factor > de.employer_oncost_factor > ch.employer_oncost_factor
    assert at.breakeven_hourly_rate > de.breakeven_hourly_rate > ch.breakeven_hourly_rate


def test_recommended_fixed_price_covers_scope_creep_and_target_margin():
    res = calculate_agency_margin(AgencyProjectInput(scope_creep_pct=25.0, external_freelancer_net=5_000.0))
    assert res.recommended_fixed_price_with_buffer > res.total_project_revenue


def test_invalid_country_raises():
    with pytest.raises(ValueError):
        calculate_agency_margin(AgencyProjectInput(country="UK"))


def test_invalid_utilization_raises():
    with pytest.raises(ValueError):
        calculate_agency_margin(AgencyProjectInput(billable_utilization_pct=0.0))
