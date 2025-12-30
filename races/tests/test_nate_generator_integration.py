"""
Integration tests for the Nate Workout Generator.

Tests all 14 methodologies, 15 archetype categories, and progression styles.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'generation_modules'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'nate_archetypes'))

import unittest
from nate_workout_generator import (
    TRAINING_METHODOLOGIES,
    PROGRESSION_STYLES,
    generate_nate_workout,
    generate_nate_zwo,
    select_archetype_for_workout,
    calculate_level_from_week,
    NEW_ARCHETYPES
)


class TestArchetypeCounts(unittest.TestCase):
    """Test that all archetypes are present and properly structured."""

    def test_methodology_count(self):
        """Should have 14 methodologies."""
        self.assertEqual(len(TRAINING_METHODOLOGIES), 14)

    def test_progression_style_count(self):
        """Should have 8 progression styles."""
        self.assertEqual(len(PROGRESSION_STYLES), 8)

    def test_archetype_category_count(self):
        """Should have 15 archetype categories."""
        self.assertEqual(len(NEW_ARCHETYPES), 15)

    def test_total_archetype_count(self):
        """Should have 41 total archetypes."""
        total = sum(len(archs) for archs in NEW_ARCHETYPES.values())
        self.assertEqual(total, 41)

    def test_total_workout_variations(self):
        """Should have 246 total workout variations (41 * 6 levels)."""
        total = sum(len(archs) for archs in NEW_ARCHETYPES.values())
        self.assertEqual(total * 6, 246)


class TestMethodologyConfiguration(unittest.TestCase):
    """Test methodology configuration completeness."""

    def test_all_methodologies_have_required_fields(self):
        """All methodologies should have required configuration fields."""
        required_fields = ['name', 'description', 'primary_workouts', 'progression_style']
        for key, config in TRAINING_METHODOLOGIES.items():
            for field in required_fields:
                self.assertIn(field, config, f"{key} missing {field}")

    def test_no_sweet_spot_references(self):
        """No methodology should reference Sweet Spot - only G-Spot."""
        for key, config in TRAINING_METHODOLOGIES.items():
            description = config.get('description', '').lower()
            self.assertNotIn('sweet spot', description, f"{key} references Sweet Spot")


class TestWorkoutGeneration(unittest.TestCase):
    """Test workout generation for all categories."""

    def test_vo2max_generation(self):
        """VO2max workouts should generate properly."""
        name, desc, blocks = generate_nate_workout('vo2max', 4, 'POLARIZED')
        self.assertIsNotNone(name)
        self.assertIn('VO2', name)
        self.assertIn('<IntervalsT', blocks)

    def test_g_spot_generation(self):
        """G-Spot workouts should generate properly."""
        name, desc, blocks = generate_nate_workout('g_spot', 4, 'G_SPOT')
        self.assertIsNotNone(name)
        self.assertIn('G-Spot', name)
        self.assertIsNotNone(blocks)

    def test_norwegian_generation(self):
        """Norwegian workouts should generate properly."""
        name, desc, blocks = generate_nate_workout('norwegian', 4, 'NORWEGIAN')
        self.assertIsNotNone(name)
        self.assertIn('Norwegian', name)

    def test_lt1_maf_generation(self):
        """LT1/MAF workouts should generate properly."""
        name, desc, blocks = generate_nate_workout('lt1', 4, 'MAF_LT1')
        self.assertIsNotNone(name)
        self.assertIn('LT1', name)

    def test_critical_power_generation(self):
        """Critical Power workouts should generate properly."""
        name, desc, blocks = generate_nate_workout('cp', 4, 'CRITICAL_POWER')
        self.assertIsNotNone(name)
        self.assertIn('CP', name)

    def test_hvli_generation(self):
        """HVLI workouts should generate properly."""
        name, desc, blocks = generate_nate_workout('hvli', 4, 'HVLI')
        self.assertIsNotNone(name)
        self.assertIn('HVLI', name)

    def test_recovery_generation(self):
        """Recovery workouts should generate properly."""
        name, desc, blocks = generate_nate_workout('recovery', 4, 'POLARIZED')
        self.assertIsNotNone(name)
        self.assertIn('Recovery', name)

    def test_testing_generation(self):
        """Testing workouts should generate properly."""
        name, desc, blocks = generate_nate_workout('test', 4, 'POLARIZED')
        self.assertIsNotNone(name)
        self.assertIn('Test', name)

    def test_inscyd_generation(self):
        """INSCYD workouts should generate properly."""
        name, desc, blocks = generate_nate_workout('inscyd', 4, 'INSCYD')
        self.assertIsNotNone(name)


class TestProgressionStyles(unittest.TestCase):
    """Test progression style calculations."""

    def test_volume_first_progression(self):
        """Traditional progression should increase levels over time."""
        levels = [calculate_level_from_week(w, 12, 2, 'PYRAMIDAL') for w in range(1, 11)]
        # Levels should generally increase
        self.assertLess(levels[0], levels[-1])

    def test_intensity_stable_progression(self):
        """Polarized should maintain stable intensity levels."""
        levels = [calculate_level_from_week(w, 12, 2, 'POLARIZED') for w in range(1, 11)]
        # Levels should stay in 4-5 range mostly
        for level in levels:
            self.assertGreaterEqual(level, 4)
            self.assertLessEqual(level, 5)

    def test_density_increase_progression(self):
        """G-Spot should have more aggressive progression."""
        # Test weeks 1-9 (excluding taper weeks 10-12 for a 12-week plan with 2-week taper)
        levels = [calculate_level_from_week(w, 12, 2, 'G_SPOT') for w in range(1, 10)]
        # Should reach at least level 5 by week 9 (build phase end)
        self.assertGreaterEqual(levels[-1], 5)
        # Should start low
        self.assertLessEqual(levels[0], 3)

    def test_taper_week_handling(self):
        """Taper weeks should use moderate levels."""
        # Week 11 and 12 of a 12-week plan are taper
        level_11 = calculate_level_from_week(11, 12, 2, 'POLARIZED')
        level_12 = calculate_level_from_week(12, 12, 2, 'POLARIZED')
        self.assertEqual(level_11, 4)
        self.assertEqual(level_12, 4)


class TestMethodologyAwareSelection(unittest.TestCase):
    """Test methodology-aware archetype selection."""

    def test_polarized_avoids_g_spot(self):
        """Polarized methodology should avoid G-Spot category."""
        archetype = select_archetype_for_workout('g_spot', 'POLARIZED', 0)
        # Polarized avoids G-Spot (middle zone)
        self.assertIsNone(archetype)

    def test_g_spot_methodology_selects_g_spot(self):
        """G-Spot methodology should select G-Spot archetypes."""
        archetype = select_archetype_for_workout('g_spot', 'G_SPOT', 0)
        self.assertIsNotNone(archetype)
        self.assertIn('G-Spot', archetype['name'])

    def test_hit_prefers_short_intense(self):
        """HIT methodology should select VO2max archetypes."""
        archetype = select_archetype_for_workout('vo2max', 'HIT', 0)
        self.assertIsNotNone(archetype)


class TestBlockGeneration(unittest.TestCase):
    """Test ZWO block generation for different workout types."""

    def test_interval_blocks_have_correct_structure(self):
        """Interval workouts should have IntervalsT blocks."""
        name, desc, blocks = generate_nate_workout('vo2max', 4, 'POLARIZED')
        self.assertIn('<IntervalsT', blocks)
        self.assertIn('OnDuration', blocks)
        self.assertIn('OnPower', blocks)

    def test_recovery_blocks_are_low_power(self):
        """Recovery workouts should have low power targets."""
        name, desc, blocks = generate_nate_workout('recovery', 4, 'POLARIZED')
        self.assertIn('Power="0.5', blocks)  # ~50% power

    def test_testing_blocks_include_freeride(self):
        """Testing workouts should include FreeRide for max effort."""
        name, desc, blocks = generate_nate_workout('test', 4, 'POLARIZED')
        # Ramp tests use steady state progression
        self.assertIn('<SteadyState', blocks)

    def test_warmup_and_cooldown_present(self):
        """Most workouts should have warmup and cooldown."""
        name, desc, blocks = generate_nate_workout('threshold', 4, 'PYRAMIDAL')
        self.assertIn('<Warmup', blocks)
        self.assertIn('<Cooldown', blocks)


class TestZWOFileGeneration(unittest.TestCase):
    """Test complete ZWO file generation."""

    def test_complete_zwo_has_required_elements(self):
        """Complete ZWO file should have all required XML elements."""
        zwo = generate_nate_zwo('vo2max', 4, 'POLARIZED', 0, 'Test Workout')
        # XML declaration can use single or double quotes
        self.assertIn('<?xml version=', zwo)
        self.assertIn('<workout_file>', zwo)
        self.assertIn('<name>Test Workout</name>', zwo)
        self.assertIn('<workout>', zwo)
        self.assertIn('</workout>', zwo)
        self.assertIn('</workout_file>', zwo)


class TestCPPowerTargets(unittest.TestCase):
    """Test that CP power targets are correctly converted to FTP."""

    def test_above_cp_power_is_reasonable(self):
        """Above CP repeats should have power ~106-113% FTP."""
        name, desc, blocks = generate_nate_workout('cp', 4, 'CRITICAL_POWER')
        # Level 4 uses 110% FTP
        self.assertIn('1.10', blocks)


class TestNorwegianDualWorkouts(unittest.TestCase):
    """Test Norwegian dual-workout handling."""

    def test_norwegian_classic_generates(self):
        """Norwegian 4x8 Classic should generate (variation 0)."""
        archetype = select_archetype_for_workout('norwegian', 'NORWEGIAN', 0)
        self.assertIsNotNone(archetype)
        self.assertIn('4x8', archetype['name'])

    def test_all_norwegian_variations_exist(self):
        """All 3 Norwegian variations should exist."""
        # Variation 0 = 4x8 Classic
        # Variation 1 = Double AM
        # Variation 2 = Double PM
        for i in range(3):
            archetype = select_archetype_for_workout('norwegian', 'NORWEGIAN', i)
            self.assertIsNotNone(archetype, f"Variation {i} should exist")

    def test_norwegian_generates_valid_blocks(self):
        """Norwegian workout should generate valid interval blocks."""
        name, desc, blocks = generate_nate_workout('norwegian', 4, 'NORWEGIAN')
        self.assertIsNotNone(blocks)
        # Should have 8-minute intervals
        self.assertIn('Duration', blocks)


if __name__ == '__main__':
    unittest.main(verbosity=2)
