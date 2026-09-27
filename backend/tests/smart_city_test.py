"""Tests for Smart City Platform & Urban Intelligence (Aptimizer X+)."""
import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import smart_city as smartcitylib
import autonomous_planning as autoplanning


@pytest.fixture
def sample_project():
    return autoplanning.one_click_generate({"plot_area_sqm": 15000.0, "floors": 14})


def test_city_scale_plan(sample_project):
    res = smartcitylib.city_scale_plan(sample_project)
    assert res["ok"] is True
    assert len(res["land_use_distribution"]) == 5
    assert res["urban_fabric_metrics"]["permeability_index"] > 0


def test_simulate_traffic(sample_project):
    res = smartcitylib.simulate_traffic(sample_project)
    assert res["ok"] is True
    assert res["trip_generation"]["peak_am_trips_per_hour"] > 0
    assert res["level_of_service"]["volume_capacity_ratio"] > 0
    assert "PASS" in res["emergency_vehicle_clearance"]["status"]


def test_optimize_utility_network(sample_project):
    res = smartcitylib.optimize_utility_network(sample_project)
    assert res["ok"] is True
    assert res["stormwater"]["peak_discharge_m3_per_hr"] > 0
    assert res["water_supply"]["daily_water_demand_kl"] > 0
    assert res["sewerage"]["daily_sewage_generation_kl"] > 0
    assert res["electrical"]["connected_load_kva"] > 0


def test_urban_digital_twin(sample_project):
    res = smartcitylib.urban_digital_twin(sample_project)
    assert res["ok"] is True
    assert res["microclimate_simulation"]["annual_sun_exposure_hours"] > 2000
    assert res["microclimate_simulation"]["urban_heat_island_score"] > 50
    assert len(res["gis_boundary_layers"]) >= 3


def test_forecast_infrastructure_demand(sample_project):
    res = smartcitylib.forecast_infrastructure_demand(sample_project)
    assert res["ok"] is True
    assert len(res["forecast_timeline"]) == 5
    assert res["forecast_timeline"][-1]["year"] == 2040
    assert res["forecast_timeline"][-1]["water_demand_mld"] > 0
