"""Tests for Digital Twin & Smart Construction Platform (Aptimizer V5)."""
import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import digital_twin as digitaltwinlib
import bim as bimlib
import autonomous_planning as autoplanning


@pytest.fixture
def sample_project():
    return autoplanning.one_click_generate({"plot_area_sqm": 12000.0, "floors": 12})


def test_iot_registry(sample_project):
    res = digitaltwinlib.iot_registry(sample_project)
    assert res["ok"] is True
    assert res["total_sensors_deployed"] >= 5
    assert res["devices_online"] >= 3
    assert any(d["id"] == "IOT-CONC-01" for d in res["devices"])


def test_sensor_telemetry(sample_project):
    res = digitaltwinlib.sensor_telemetry(sample_project)
    assert res["ok"] is True
    conc = res["concrete_curing_maturity"]
    assert conc["curing_age_hours"] == 72
    assert conc["estimated_compressive_strength_mpa"] > 20.0
    assert "SAFE TO STRIP" in conc["formwork_stripping_advisory"]


def test_track_progress_4d(sample_project):
    res = digitaltwinlib.track_progress_4d(sample_project)
    assert res["ok"] is True
    assert res["earned_value_metrics"]["schedule_performance_index_spi"] > 0
    assert len(res["floor_4d_breakdown"]) == 12


def test_quality_safety_audit(sample_project):
    res = digitaltwinlib.quality_safety_audit(sample_project)
    assert res["ok"] is True
    assert len(res["cube_tests"]) >= 3
    assert res["safety"]["safe_man_hours_worked"] > 100000
    assert res["safety"]["lost_time_injuries_lti"] == 0


def test_predict_delays(sample_project):
    res = digitaltwinlib.predict_delays(sample_project)
    assert res["ok"] is True
    assert res["on_time_probability_pct"] > 80.0
    assert len(res["risk_factors_analyzed"]) == 3


def test_facility_management(sample_project):
    res = digitaltwinlib.facility_management(sample_project)
    assert res["ok"] is True
    assert len(res["assets"]) >= 3
    assert res["overall_facility_health_pct"] > 90.0
    assert len(res["preventive_maintenance_calendar"]) >= 2


def test_dwg_export(sample_project):
    dwg_bytes = bimlib.export_siteplan_dwg(sample_project)
    assert len(dwg_bytes) > 100
    assert b"SECTION" in dwg_bytes or b"HEADER" in dwg_bytes
