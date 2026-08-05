"""Smoke tests for the coverage-report generator."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from coverage_report import build_markdown, build_navigator_layer  # noqa: E402

SAMPLE = [
    {"id": "T1", "name": "A", "tactic": "Discovery", "executed": True, "detected": True, "rule": "1"},
    {"id": "T2", "name": "B", "tactic": "Execution", "executed": True, "detected": False, "gap": "x"},
    {"id": "T3", "name": "C", "tactic": "Discovery", "executed": False},
]


def test_markdown_reports_correct_percentage():
    md = build_markdown(SAMPLE)
    # 1 detected of 2 executed = 50%
    assert "1/2 executed techniques detected = 50%" in md
    assert "## Gaps found" in md
    assert "T2 B" in md


def test_navigator_only_includes_executed():
    layer = build_navigator_layer(SAMPLE)
    ids = [t["techniqueID"] for t in layer["techniques"]]
    assert ids == ["T1", "T2"]  # T3 not executed -> excluded


def test_navigator_colours_detected_vs_gap():
    layer = build_navigator_layer(SAMPLE)
    by_id = {t["techniqueID"]: t["color"] for t in layer["techniques"]}
    assert by_id["T1"] != by_id["T2"]  # detected and gap get different colours
