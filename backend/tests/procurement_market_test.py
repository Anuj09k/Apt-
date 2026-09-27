"""Tests for Aptimizer X: Smart Procurement & Ecosystem."""
import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import procurement_market as procurementlib
import autonomous_planning as autoplanning


@pytest.fixture
def sample_project():
    return autoplanning.one_click_generate({"plot_area_sqm": 12000.0, "floors": 12})


def test_live_material_prices():
    res = procurementlib.get_live_material_prices("Delhi-NCR")
    assert res["ok"] is True
    assert len(res["items"]) >= 8
    assert any("Fe 550D" in item["material"] for item in res["items"])

    res_mumbai = procurementlib.get_live_material_prices("Mumbai-MMR")
    assert res_mumbai["ok"] is True
    assert res_mumbai["selected_metro"] == "Mumbai-MMR"


def test_forecast_material_prices():
    res = procurementlib.forecast_material_prices("steel", horizon_months=12)
    assert res["ok"] is True
    assert len(res["forecast_series"]) == 12
    assert res["forecast_series"][0]["projected_price"] > 0
    assert res["forecast_series"][0]["confidence_pct"] > 70


def test_supplier_intelligence():
    res = procurementlib.get_supplier_intelligence()
    assert res["ok"] is True
    assert res["total_suppliers"] >= 4
    assert any(s["name"] == "Tata Steel Ltd (Tiscon)" for s in res["suppliers"])


def test_procurement_calendar(sample_project):
    res = procurementlib.get_procurement_calendar(sample_project)
    assert res["ok"] is True
    assert res["total_procurement_milestones"] >= 3
    assert any("RMC" in m["material"] for m in res["milestones"])


def test_calculate_inventory_plan(sample_project):
    res = procurementlib.calculate_inventory_plan(sample_project)
    assert res["ok"] is True
    assert len(res["inventory_items"]) >= 3
    assert any("TMT Steel" in item["material"] for item in res["inventory_items"])


def test_marketplace_catalog():
    res = procurementlib.get_marketplace_catalog()
    assert res["ok"] is True
    assert res["total_plugins"] >= 4
    assert res["total_apis"] >= 4
    assert any(p["id"] == "PLG-01" for p in res["plugins"])


def test_generate_tender_documents(sample_project):
    res = procurementlib.generate_tender_documents(sample_project)
    assert res["ok"] is True
    assert "APT/NIT/" in res["nit"]["tender_ref_no"]
    assert len(res["sections"]) == 6
    assert res["tender_package_status"] == "READY FOR ISSUANCE"


def test_generate_government_approval_dossier(sample_project):
    res = procurementlib.generate_government_approval_dossier(sample_project)
    assert res["ok"] is True
    assert res["total_clearance_agencies"] >= 3
    assert res["overall_submission_readiness_pct"] > 90
    assert any("RERA" in c["agency"] for c in res["clearances"])


def test_educational_mode_guide():
    res = procurementlib.get_educational_mode_guide("setbacks")
    assert res["ok"] is True
    assert "NBC 2016" in res["guide"]["governing_code"]
    assert "fire" in res["guide"]["principle"].lower()
