#!/usr/bin/env python3
"""
Regression Test Suite for Archetype Integration in gravel-plans-experimental

Run with: pytest tests/archetypes/test_regression.py -v
"""

import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List
import pytest

ROOT_DIR = Path(__file__).parent.parent.parent
ARCHETYPES_PATH = ROOT_DIR / "archetypes"


class TestArchetypeSubmodule:
    """Tests for submodule existence and structure."""

    def test_submodule_exists(self):
        assert ARCHETYPES_PATH.exists(), "Archetypes submodule not found"

    def test_white_paper_exists(self):
        white_paper = ARCHETYPES_PATH / "WORKOUT_ARCHETYPES_WHITE_PAPER.md"
        assert white_paper.exists(), "White paper not found"
        content = white_paper.read_text()
        assert len(content) > 1000, "White paper appears empty"

    def test_architecture_docs_exist(self):
        assert (ARCHETYPES_PATH / "ARCHITECTURE.md").exists()
        assert (ARCHETYPES_PATH / "CATEGORIZATION_RULES.md").exists()


class TestArchetypeDefinitions:
    """Tests for archetype definitions."""

    CRITICAL_ARCHETYPES = ["vo2", "threshold", "tempo", "endurance", "sfr", "sprint"]

    def test_critical_archetypes_documented(self):
        white_paper = ARCHETYPES_PATH / "WORKOUT_ARCHETYPES_WHITE_PAPER.md"
        content = white_paper.read_text().lower()
        missing = [a for a in self.CRITICAL_ARCHETYPES if a not in content]
        assert len(missing) == 0, f"Missing archetypes: {missing}"

    def test_six_level_progression_system(self):
        white_paper = ARCHETYPES_PATH / "WORKOUT_ARCHETYPES_WHITE_PAPER.md"
        content = white_paper.read_text().lower()
        assert "level 1" in content
        assert "level 6" in content

    def test_power_zones_documented(self):
        white_paper = ARCHETYPES_PATH / "WORKOUT_ARCHETYPES_WHITE_PAPER.md"
        content = white_paper.read_text().lower()
        assert "ftp" in content


class TestZWOFiles:
    """Tests for ZWO file validity."""

    @pytest.fixture
    def zwo_directory(self) -> Path:
        zwo_cleaned = ARCHETYPES_PATH / "zwo_output_cleaned"
        zwo_standard = ARCHETYPES_PATH / "zwo_output"
        if zwo_cleaned.exists():
            return zwo_cleaned
        elif zwo_standard.exists():
            return zwo_standard
        pytest.skip("No ZWO directory found")

    @pytest.fixture
    def sample_zwo_files(self, zwo_directory: Path) -> List[Path]:
        return list(zwo_directory.rglob("*.zwo"))[:100]

    def test_zwo_files_exist(self, zwo_directory: Path):
        zwo_files = list(zwo_directory.rglob("*.zwo"))
        assert len(zwo_files) >= 100, f"Expected 100+ ZWO files, found {len(zwo_files)}"

    def test_zwo_files_valid_xml(self, sample_zwo_files: List[Path]):
        invalid = []
        for zwo_file in sample_zwo_files:
            try:
                ET.parse(zwo_file)
            except ET.ParseError as e:
                invalid.append((zwo_file.name, str(e)))
        assert len(invalid) == 0, f"Invalid XML: {invalid[:5]}"

    def test_zwo_files_have_required_elements(self, sample_zwo_files: List[Path]):
        missing = []
        for zwo_file in sample_zwo_files:
            try:
                tree = ET.parse(zwo_file)
                root = tree.getroot()
                if root.find(".//workout") is None:
                    missing.append((zwo_file.name, "workout"))
                if root.find(".//name") is None:
                    missing.append((zwo_file.name, "name"))
            except ET.ParseError:
                pass
        assert len(missing) == 0, f"Missing elements: {missing[:5]}"

    def test_zwo_power_values_in_range(self, sample_zwo_files: List[Path]):
        out_of_range = []
        for zwo_file in sample_zwo_files:
            try:
                tree = ET.parse(zwo_file)
                root = tree.getroot()
                for elem in root.iter():
                    for attr in ['Power', 'PowerLow', 'PowerHigh', 'OnPower', 'OffPower']:
                        if attr in elem.attrib:
                            power = float(elem.attrib[attr])
                            if power < 0 or power > 2.5:
                                out_of_range.append((zwo_file.name, attr, power))
            except (ET.ParseError, ValueError):
                pass
        assert len(out_of_range) == 0, f"Out of range: {out_of_range[:5]}"


class TestPlanIntegration:
    """Tests for integration with training plan generation."""

    def test_plans_directory_exists(self):
        plans_dir = ROOT_DIR / "plans"
        assert plans_dir.exists(), "Plans directory not found"

    def test_plan_templates_exist(self):
        plans_dir = ROOT_DIR / "plans"
        plan_files = list(plans_dir.glob("*.json")) + list(plans_dir.glob("*.py"))
        assert len(plan_files) > 0, "No plan templates found"


class TestRegressionBaseline:
    """Baseline tests to catch regressions."""

    MIN_ARCHETYPE_COUNT = 15
    MIN_ZWO_FILE_COUNT = 500

    def test_minimum_archetype_count(self):
        white_paper = ARCHETYPES_PATH / "WORKOUT_ARCHETYPES_WHITE_PAPER.md"
        content = white_paper.read_text()
        archetype_pattern = r"^[-*]\s+\*?\*?([a-z0-9_]+)\*?\*?:"
        archetypes = re.findall(archetype_pattern, content, re.MULTILINE | re.IGNORECASE)
        assert len(archetypes) >= self.MIN_ARCHETYPE_COUNT, \
            f"Count {len(archetypes)} below baseline {self.MIN_ARCHETYPE_COUNT}"

    def test_minimum_zwo_file_count(self):
        zwo_cleaned = ARCHETYPES_PATH / "zwo_output_cleaned"
        zwo_standard = ARCHETYPES_PATH / "zwo_output"
        zwo_dir = zwo_cleaned if zwo_cleaned.exists() else zwo_standard
        if not zwo_dir.exists():
            pytest.skip("No ZWO directory")
        zwo_count = len(list(zwo_dir.rglob("*.zwo")))
        assert zwo_count >= self.MIN_ZWO_FILE_COUNT, \
            f"Count {zwo_count} below baseline {self.MIN_ZWO_FILE_COUNT}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
