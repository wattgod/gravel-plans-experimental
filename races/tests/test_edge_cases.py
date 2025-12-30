"""
Edge Case and Negative Tests
============================

Tests for boundary conditions, invalid inputs, and error handling.
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'generation_modules'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'nate_archetypes'))

import unittest
from nate_workout_generator import (
    generate_nate_workout,
    generate_nate_zwo,
    select_archetype_for_workout,
    calculate_level_from_week,
    is_recovery_week,
    get_level_data,
    get_archetype_by_category_and_index,
    TRAINING_METHODOLOGIES,
    NEW_ARCHETYPES,
)


class TestInvalidInputs(unittest.TestCase):
    """Test handling of invalid inputs."""

    def test_unknown_workout_type_returns_none(self):
        """Unknown workout type should return None, not crash."""
        name, desc, blocks = generate_nate_workout('nonexistent_workout_type', 4, 'POLARIZED')
        self.assertIsNone(name)
        self.assertIsNone(desc)
        self.assertIsNone(blocks)

    def test_empty_workout_type_returns_none(self):
        """Empty workout type should return None."""
        name, desc, blocks = generate_nate_workout('', 4, 'POLARIZED')
        self.assertIsNone(name)

    def test_unknown_methodology_falls_back(self):
        """Unknown methodology should fall back to POLARIZED."""
        # Should not crash, should use POLARIZED as fallback
        name, desc, blocks = generate_nate_workout('vo2max', 4, 'NONEXISTENT_METHOD')
        self.assertIsNotNone(name)
        self.assertIn('VO2', name)

    def test_negative_level_clamped(self):
        """Negative level should be clamped to 1."""
        name, desc, blocks = generate_nate_workout('vo2max', -5, 'POLARIZED')
        self.assertIsNotNone(name)
        self.assertIn('L1', name)  # Should be level 1

    def test_level_zero_clamped(self):
        """Level 0 should be clamped to 1."""
        name, desc, blocks = generate_nate_workout('vo2max', 0, 'POLARIZED')
        self.assertIsNotNone(name)
        self.assertIn('L1', name)

    def test_level_above_max_clamped(self):
        """Level above 6 should be clamped to 6."""
        name, desc, blocks = generate_nate_workout('vo2max', 100, 'POLARIZED')
        self.assertIsNotNone(name)
        self.assertIn('L6', name)

    def test_negative_variation_wraps(self):
        """Negative variation should wrap around."""
        # Should not crash
        archetype = select_archetype_for_workout('vo2max', 'POLARIZED', -1)
        self.assertIsNotNone(archetype)


class TestBoundaryConditions(unittest.TestCase):
    """Test boundary conditions."""

    def test_week_zero(self):
        """Week 0 should not crash."""
        level = calculate_level_from_week(0, 12, 2, 'POLARIZED')
        self.assertGreaterEqual(level, 1)
        self.assertLessEqual(level, 6)

    def test_week_exceeds_total(self):
        """Week exceeding total should return taper level."""
        level = calculate_level_from_week(15, 12, 2, 'POLARIZED')
        self.assertEqual(level, 4)  # Taper level

    def test_total_weeks_zero(self):
        """Total weeks of 0 should not crash (division by zero protection)."""
        try:
            level = calculate_level_from_week(1, 0, 2, 'POLARIZED')
            # If it doesn't crash, any level 1-6 is acceptable
            self.assertGreaterEqual(level, 1)
        except ZeroDivisionError:
            self.fail("calculate_level_from_week should handle total_weeks=0")

    def test_taper_weeks_equals_total(self):
        """Taper weeks equal to total should still work."""
        level = calculate_level_from_week(1, 12, 12, 'POLARIZED')
        self.assertEqual(level, 4)  # All weeks are taper

    def test_single_week_plan(self):
        """Single week plan should not crash."""
        level = calculate_level_from_week(1, 1, 0, 'POLARIZED')
        self.assertGreaterEqual(level, 1)
        self.assertLessEqual(level, 6)


class TestRecoveryWeekLogic(unittest.TestCase):
    """Test recovery week detection."""

    def test_3_1_pattern_week_4_is_recovery(self):
        """Week 4 in 3:1 pattern should be recovery."""
        self.assertTrue(is_recovery_week(4, "3:1"))

    def test_3_1_pattern_week_3_is_not_recovery(self):
        """Week 3 in 3:1 pattern should not be recovery."""
        self.assertFalse(is_recovery_week(3, "3:1"))

    def test_3_1_pattern_week_8_is_recovery(self):
        """Week 8 in 3:1 pattern should be recovery."""
        self.assertTrue(is_recovery_week(8, "3:1"))

    def test_4_1_pattern_week_5_is_recovery(self):
        """Week 5 in 4:1 pattern should be recovery."""
        self.assertTrue(is_recovery_week(5, "4:1"))

    def test_4_1_pattern_week_4_is_not_recovery(self):
        """Week 4 in 4:1 pattern should not be recovery."""
        self.assertFalse(is_recovery_week(4, "4:1"))

    def test_invalid_pattern_uses_default(self):
        """Invalid pattern should use 3:1 default."""
        # Should not crash, should use 3:1 default
        result = is_recovery_week(4, "invalid")
        self.assertIsInstance(result, bool)

    def test_empty_pattern_uses_default(self):
        """Empty pattern should use 3:1 default."""
        result = is_recovery_week(4, "")
        self.assertIsInstance(result, bool)


class TestArchetypeSelection(unittest.TestCase):
    """Test archetype selection edge cases."""

    def test_avoided_category_returns_none(self):
        """Category avoided by methodology should return None."""
        # Polarized avoids G_Spot
        archetype = select_archetype_for_workout('g_spot', 'POLARIZED', 0)
        self.assertIsNone(archetype)

    def test_invalid_category_returns_none(self):
        """Invalid category should return None."""
        archetype = get_archetype_by_category_and_index('NonexistentCategory', 0)
        self.assertIsNone(archetype)

    def test_variation_exceeds_available_wraps(self):
        """Variation exceeding available archetypes should wrap."""
        # Get category with known count
        vo2max_count = len(NEW_ARCHETYPES.get('VO2max', []))
        if vo2max_count > 0:
            archetype = get_archetype_by_category_and_index('VO2max', vo2max_count + 5)
            self.assertIsNotNone(archetype)

    def test_all_methodologies_are_valid(self):
        """All defined methodologies should have required fields."""
        required_fields = ['name', 'description', 'primary_workouts', 'progression_style']
        for method_name, method_config in TRAINING_METHODOLOGIES.items():
            for field in required_fields:
                self.assertIn(
                    field, method_config,
                    f"Methodology {method_name} missing required field: {field}"
                )


class TestLevelDataRetrieval(unittest.TestCase):
    """Test level data retrieval edge cases."""

    def test_missing_level_falls_back(self):
        """Missing level should fall back to closest available."""
        # Create a test archetype with only some levels
        test_archetype = {
            'name': 'Test',
            'levels': {
                '3': {'structure': 'test'},
                '5': {'structure': 'test'},
            }
        }
        # Request level 4, should get 3 or 5
        level_data = get_level_data(test_archetype, 4)
        self.assertIsNotNone(level_data)

    def test_empty_levels_returns_none(self):
        """Empty levels dict should return None."""
        test_archetype = {'name': 'Test', 'levels': {}}
        level_data = get_level_data(test_archetype, 4)
        self.assertIsNone(level_data)

    def test_no_levels_key_returns_none(self):
        """Archetype without levels key should return None."""
        test_archetype = {'name': 'Test'}
        level_data = get_level_data(test_archetype, 4)
        self.assertIsNone(level_data)

    def test_none_archetype_returns_none(self):
        """None archetype should return None."""
        level_data = get_level_data(None, 4)
        self.assertIsNone(level_data)


class TestZWOGenerationEdgeCases(unittest.TestCase):
    """Test ZWO generation edge cases."""

    def test_special_characters_in_custom_name(self):
        """Special characters in custom name should be escaped."""
        zwo = generate_nate_zwo('vo2max', 4, 'POLARIZED', 0, "Test <>&\"' Workout")
        self.assertIsNotNone(zwo)
        # Should not contain unescaped special chars
        self.assertNotIn('<>&', zwo.split('<name>')[1].split('</name>')[0])

    def test_very_long_workout_name(self):
        """Very long workout name should be handled."""
        long_name = "A" * 500
        zwo = generate_nate_zwo('vo2max', 4, 'POLARIZED', 0, long_name)
        self.assertIsNotNone(zwo)

    def test_unicode_in_workout_name(self):
        """Unicode characters in workout name should be handled."""
        zwo = generate_nate_zwo('vo2max', 4, 'POLARIZED', 0, "Test 🚴 Workout")
        self.assertIsNotNone(zwo)


class TestConstantsIntegration(unittest.TestCase):
    """Test that constants are properly integrated."""

    def test_warmup_uses_constants(self):
        """Warmup should use power values from constants."""
        zwo = generate_nate_zwo('vo2max', 4, 'POLARIZED')
        self.assertIsNotNone(zwo)
        # Should contain 0.50 (WARMUP_POWER_LOW) and 0.75 (WARMUP_POWER_HIGH)
        self.assertIn('0.50', zwo)
        self.assertIn('0.75', zwo)

    def test_cooldown_uses_constants(self):
        """Cooldown should use power values from constants."""
        zwo = generate_nate_zwo('vo2max', 4, 'POLARIZED')
        self.assertIsNotNone(zwo)
        # Cooldown should be present
        self.assertIn('Cooldown', zwo)


if __name__ == '__main__':
    unittest.main(verbosity=2)
