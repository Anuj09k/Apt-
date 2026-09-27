"""Tests for Aptimizer X: AI Civil Engineering Operating System."""
import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import ai_os as aioslib
import autonomous_planning as autoplanning


@pytest.fixture
def sample_project():
    return autoplanning.one_click_generate({"plot_area_sqm": 12000.0, "floors": 12})


def test_build_knowledge_graph(sample_project):
    res = aioslib.build_knowledge_graph(sample_project)
    assert res["ok"] is True
    assert res["metrics"]["total_nodes"] >= 10
    assert res["metrics"]["total_relationships"] >= 10
    assert any(n["id"] == "CODE-IS456" for n in res["nodes"])
    assert any(e["source"] == "CODE-NBC-P3" for e in res["edges"])


def test_get_engineering_memory(sample_project):
    res = aioslib.get_engineering_memory(sample_project)
    assert res["ok"] is True
    assert res["total_episodes"] >= 3
    assert res["memory_summary"]["avg_confidence"] > 0.85
    assert any("Shear Wall" in e["title"] for e in res["episodes"])


def test_audit_decision_log(sample_project):
    res = aioslib.audit_decision_log(sample_project)
    assert res["ok"] is True
    assert "APT-DEC-LOG-" in res["audit_hash"]
    assert res["total_decisions"] >= 4
    assert res["all_approved"] is True


def test_simulate_decision_sandbox(sample_project):
    res = aioslib.simulate_decision_sandbox(sample_project, {
        "floors": 16,
        "concrete_grade": "M40",
        "slab_type": "PT Flat Slab",
        "footprint_scale": 1.05
    })
    assert res["ok"] is True
    assert res["simulation"]["floors"] == 16
    assert res["simulation"]["concrete_grade"] == "M40"
    assert res["simulation"]["quantities"]["concrete_m3"] > 0
    assert res["simulation"]["quantities"]["steel_reinforcement_mt"] > 0
    assert res["deltas"]["builtup_area_sqm"] > 0


def test_compare_benchmarks(sample_project):
    res = aioslib.compare_benchmarks(sample_project)
    assert res["ok"] is True
    assert res["total_metrics_evaluated"] >= 4
    assert res["overall_efficiency_score"] >= 90.0
    assert any(b["metric"] == "Structural Steel Consumption" for b in res["benchmarks"])
