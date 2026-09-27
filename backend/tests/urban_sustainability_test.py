"""Tests for Aptimizer X: Urban Intelligence & Sustainability Engine."""
import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import urban_sustainability as urbansustlib
import autonomous_planning as autoplanning


@pytest.fixture
def sample_project():
    return autoplanning.one_click_generate({"plot_area_sqm": 12000.0, "floors": 12})


def test_predict_urban_growth_and_value(sample_project):
    res = urbansustlib.predict_urban_growth_and_value(sample_project)
    assert res["ok"] is True
    assert res["five_year_cagr_pct"] > 0
    assert len(res["appreciation_projections"]) == 5
    assert res["appreciation_projections"][-1]["cumulative_gain_pct"] > 0


def test_analyze_climate_and_disasters(sample_project):
    res = urbansustlib.analyze_climate_and_disasters(sample_project)
    assert res["ok"] is True
    assert res["composite_resilience_score"] > 50
    assert len(res["hazards"]) >= 3
    assert any(h["hazard_type"] == "Seismic Hazard" for h in res["hazards"])


def test_analyze_noise_and_pollution(sample_project):
    res = urbansustlib.analyze_noise_and_pollution(sample_project)
    assert res["ok"] is True
    assert res["noise_analysis"]["front_facade_noise_dba"] < res["noise_analysis"]["curb_noise_level_dba"]
    assert "POOR" in res["air_quality_analysis"]["site_air_quality_index_aqi"]


def test_calculate_green_building_scorecard(sample_project):
    res = urbansustlib.calculate_green_building_scorecard(sample_project, "IGBC")
    assert res["ok"] is True
    assert res["total_points_achieved"] >= 60
    assert "PLATINUM" in res["certification_tier"] or "GOLD" in res["certification_tier"]
    assert len(res["categories"]) >= 5


def test_generate_esg_report(sample_project):
    res = urbansustlib.generate_esg_report(sample_project)
    assert res["ok"] is True
    assert res["carbon_accounting_tco2e"]["total_footprint_tco2e"] > 0
    assert res["social_metrics"]["worker_welfare_compliance_pct"] == 100.0
    assert "AAA" in res["esg_composite_rating"]


def test_calculate_lifecycle_cost(sample_project):
    res = urbansustlib.calculate_lifecycle_cost(sample_project, years=30)
    assert res["ok"] is True
    assert res["analysis_horizon_years"] == 30
    assert res["total_lifecycle_cost_inr"] > res["initial_capital_expenditure_capex_inr"]
    assert len(res["rehabilitation_schedule"]) >= 4


def test_get_executive_dashboard_kpis(sample_project):
    res = urbansustlib.get_executive_dashboard_kpis(sample_project)
    assert res["ok"] is True
    assert res["kpis"]["project_internal_rate_of_return_irr_pct"] > 15.0
    assert res["kpis"]["equity_multiple"] > 1.5
    assert "ON TRACK" in res["kpis"]["project_health_status"]


def test_schedule_equipment_and_risks(sample_project):
    res = urbansustlib.schedule_equipment_and_risks(sample_project)
    assert res["ok"] is True
    assert len(res["equipment_fleet"]) >= 3
    assert len(res["identified_delay_risks"]) >= 3
    assert res["recommended_float_buffer_days"] > 10
