"""
ZWO XML Validation Tests
========================

Tests that validate the structural integrity and schema compliance
of generated ZWO workout files.

These tests go beyond string matching to actually parse and validate
the XML structure, ensuring generated files will work in Zwift.
"""

import sys
import os
import xml.etree.ElementTree as ET
from typing import Optional, List, Tuple

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'generation_modules'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'nate_archetypes'))

import unittest
from nate_workout_generator import (
    generate_nate_zwo,
    generate_nate_workout,
    NEW_ARCHETYPES,
    TRAINING_METHODOLOGIES,
)


# =============================================================================
# ZWO SCHEMA VALIDATION
# =============================================================================

# Valid ZWO block types
VALID_BLOCK_TYPES = {
    'Warmup',
    'Cooldown',
    'SteadyState',
    'IntervalsT',
    'Ramp',
    'FreeRide',
    'FreeRide',
}

# Required attributes per block type
REQUIRED_ATTRIBUTES = {
    'Warmup': ['Duration', 'PowerLow', 'PowerHigh'],
    'Cooldown': ['Duration', 'PowerLow', 'PowerHigh'],
    'SteadyState': ['Duration', 'Power'],
    'IntervalsT': ['Repeat', 'OnDuration', 'OnPower', 'OffDuration', 'OffPower'],
    'Ramp': ['Duration', 'PowerLow', 'PowerHigh'],
    'FreeRide': ['Duration'],
}

# Power limits (FTP fractions)
MIN_POWER = 0.30
MAX_POWER = 3.00

# Duration limits (seconds)
MIN_DURATION = 1
MAX_DURATION = 21600  # 6 hours
MIN_WORKOUT_DURATION = 900  # 15 minutes
MAX_WORKOUT_DURATION = 21600  # 6 hours


def validate_zwo_xml(zwo_content: str) -> Tuple[bool, List[str]]:
    """
    Validate a ZWO XML string for structural correctness.

    Args:
        zwo_content: The ZWO XML content as a string

    Returns:
        Tuple of (is_valid, list_of_errors)
    """
    errors = []

    # 1. Check XML is parseable
    try:
        root = ET.fromstring(zwo_content)
    except ET.ParseError as e:
        errors.append(f"XML parse error: {e}")
        return False, errors

    # 2. Check root element
    if root.tag != 'workout_file':
        errors.append(f"Root element should be 'workout_file', got '{root.tag}'")

    # 3. Check required top-level elements
    required_elements = ['name', 'workout']
    for elem_name in required_elements:
        elem = root.find(elem_name)
        if elem is None:
            errors.append(f"Missing required element: {elem_name}")

    # 4. Check workout name is not empty
    name_elem = root.find('name')
    if name_elem is not None and not name_elem.text:
        errors.append("Workout name is empty")

    # 5. Validate workout blocks
    workout_elem = root.find('workout')
    if workout_elem is None:
        errors.append("No workout element found")
        return len(errors) == 0, errors

    total_duration = 0
    block_count = 0

    for block in workout_elem:
        block_count += 1

        # Check block type is valid
        if block.tag not in VALID_BLOCK_TYPES:
            errors.append(f"Invalid block type: {block.tag}")
            continue

        # Check required attributes
        required_attrs = REQUIRED_ATTRIBUTES.get(block.tag, [])
        for attr in required_attrs:
            if attr not in block.attrib:
                errors.append(f"{block.tag} missing required attribute: {attr}")

        # Validate duration
        duration = block.attrib.get('Duration')
        if duration:
            try:
                dur_val = int(duration)
                if dur_val < MIN_DURATION:
                    errors.append(f"{block.tag} duration too short: {dur_val}s")
                if dur_val > MAX_DURATION:
                    errors.append(f"{block.tag} duration too long: {dur_val}s")
                total_duration += dur_val
            except ValueError:
                errors.append(f"{block.tag} invalid duration: {duration}")

        # Validate power values
        power_attrs = ['Power', 'PowerLow', 'PowerHigh', 'OnPower', 'OffPower']
        for power_attr in power_attrs:
            power = block.attrib.get(power_attr)
            if power:
                try:
                    power_val = float(power)
                    if power_val < MIN_POWER:
                        errors.append(f"{block.tag} {power_attr} too low: {power_val}")
                    if power_val > MAX_POWER:
                        errors.append(f"{block.tag} {power_attr} too high: {power_val}")
                except ValueError:
                    errors.append(f"{block.tag} invalid {power_attr}: {power}")

        # Validate IntervalsT repeats
        if block.tag == 'IntervalsT':
            repeat = block.attrib.get('Repeat')
            if repeat:
                try:
                    repeat_val = int(repeat)
                    if repeat_val < 1:
                        errors.append(f"IntervalsT repeat too low: {repeat_val}")
                    if repeat_val > 30:
                        errors.append(f"IntervalsT repeat too high: {repeat_val}")

                    # Add interval duration to total
                    on_dur = int(block.attrib.get('OnDuration', 0))
                    off_dur = int(block.attrib.get('OffDuration', 0))
                    total_duration += repeat_val * (on_dur + off_dur) - int(duration or 0)
                except ValueError:
                    errors.append(f"IntervalsT invalid repeat: {repeat}")

    # 6. Check we have at least one block
    if block_count == 0:
        errors.append("Workout has no blocks")

    # 7. Check total duration is reasonable (if we have blocks)
    if block_count > 0 and total_duration > 0:
        if total_duration < MIN_WORKOUT_DURATION:
            errors.append(f"Workout too short: {total_duration}s ({total_duration/60:.1f} min)")
        if total_duration > MAX_WORKOUT_DURATION:
            errors.append(f"Workout too long: {total_duration}s ({total_duration/3600:.1f} hours)")

    return len(errors) == 0, errors


def parse_zwo_to_dict(zwo_content: str) -> Optional[dict]:
    """
    Parse ZWO content into a structured dictionary.

    Returns None if parsing fails.
    """
    try:
        root = ET.fromstring(zwo_content)
        result = {
            'name': '',
            'description': '',
            'author': '',
            'blocks': [],
            'total_duration': 0,
        }

        name_elem = root.find('name')
        if name_elem is not None:
            result['name'] = name_elem.text or ''

        desc_elem = root.find('description')
        if desc_elem is not None:
            result['description'] = desc_elem.text or ''

        author_elem = root.find('author')
        if author_elem is not None:
            result['author'] = author_elem.text or ''

        workout_elem = root.find('workout')
        if workout_elem is not None:
            for block in workout_elem:
                block_data = {
                    'type': block.tag,
                    'attributes': dict(block.attrib)
                }
                result['blocks'].append(block_data)

                # Calculate duration
                duration = int(block.attrib.get('Duration', 0))
                if block.tag == 'IntervalsT':
                    repeat = int(block.attrib.get('Repeat', 1))
                    on_dur = int(block.attrib.get('OnDuration', 0))
                    off_dur = int(block.attrib.get('OffDuration', 0))
                    duration = repeat * (on_dur + off_dur)
                result['total_duration'] += duration

        return result

    except ET.ParseError:
        return None


# =============================================================================
# TEST CASES
# =============================================================================

class TestZWOXMLParsing(unittest.TestCase):
    """Test that all generated ZWO files parse as valid XML."""

    def test_vo2max_parses(self):
        """VO2max workout should produce valid XML."""
        zwo = generate_nate_zwo('vo2max', 4, 'POLARIZED')
        self.assertIsNotNone(zwo)
        is_valid, errors = validate_zwo_xml(zwo)
        self.assertTrue(is_valid, f"Validation errors: {errors}")

    def test_threshold_parses(self):
        """Threshold workout should produce valid XML."""
        zwo = generate_nate_zwo('threshold', 4, 'PYRAMIDAL')
        self.assertIsNotNone(zwo)
        is_valid, errors = validate_zwo_xml(zwo)
        self.assertTrue(is_valid, f"Validation errors: {errors}")

    def test_g_spot_parses(self):
        """G-Spot workout should produce valid XML."""
        zwo = generate_nate_zwo('g_spot', 4, 'G_SPOT')
        self.assertIsNotNone(zwo)
        is_valid, errors = validate_zwo_xml(zwo)
        self.assertTrue(is_valid, f"Validation errors: {errors}")

    def test_recovery_parses(self):
        """Recovery workout should produce valid XML."""
        zwo = generate_nate_zwo('recovery', 4, 'POLARIZED')
        self.assertIsNotNone(zwo)
        is_valid, errors = validate_zwo_xml(zwo)
        self.assertTrue(is_valid, f"Validation errors: {errors}")

    def test_norwegian_parses(self):
        """Norwegian workout should produce valid XML."""
        zwo = generate_nate_zwo('norwegian', 4, 'NORWEGIAN')
        self.assertIsNotNone(zwo)
        is_valid, errors = validate_zwo_xml(zwo)
        self.assertTrue(is_valid, f"Validation errors: {errors}")


class TestZWOStructure(unittest.TestCase):
    """Test ZWO structural requirements."""

    def test_has_workout_file_root(self):
        """ZWO should have workout_file as root element."""
        zwo = generate_nate_zwo('vo2max', 4, 'POLARIZED')
        root = ET.fromstring(zwo)
        self.assertEqual(root.tag, 'workout_file')

    def test_has_required_elements(self):
        """ZWO should have name and workout elements."""
        zwo = generate_nate_zwo('vo2max', 4, 'POLARIZED')
        root = ET.fromstring(zwo)
        self.assertIsNotNone(root.find('name'))
        self.assertIsNotNone(root.find('workout'))

    def test_has_author(self):
        """ZWO should have author element."""
        zwo = generate_nate_zwo('vo2max', 4, 'POLARIZED')
        root = ET.fromstring(zwo)
        author = root.find('author')
        self.assertIsNotNone(author)
        self.assertEqual(author.text, 'Gravel God Training')

    def test_has_sport_type(self):
        """ZWO should have sportType element set to bike."""
        zwo = generate_nate_zwo('vo2max', 4, 'POLARIZED')
        root = ET.fromstring(zwo)
        sport = root.find('sportType')
        self.assertIsNotNone(sport)
        self.assertEqual(sport.text, 'bike')


class TestZWOPowerTargets(unittest.TestCase):
    """Test that power targets are within valid ranges."""

    def test_recovery_power_is_low(self):
        """Recovery workout power should be around 50% FTP."""
        zwo = generate_nate_zwo('recovery', 4, 'POLARIZED')
        parsed = parse_zwo_to_dict(zwo)
        self.assertIsNotNone(parsed)

        # Find the main steady state block (not warmup/cooldown)
        for block in parsed['blocks']:
            if block['type'] == 'SteadyState':
                power = float(block['attributes'].get('Power', 1.0))
                self.assertLessEqual(power, 0.60, "Recovery power should be <= 60%")
                self.assertGreaterEqual(power, 0.45, "Recovery power should be >= 45%")
                break

    def test_vo2max_power_is_high(self):
        """VO2max workout power should be above FTP."""
        zwo = generate_nate_zwo('vo2max', 4, 'POLARIZED')
        parsed = parse_zwo_to_dict(zwo)
        self.assertIsNotNone(parsed)

        # Find interval block
        for block in parsed['blocks']:
            if block['type'] == 'IntervalsT':
                on_power = float(block['attributes'].get('OnPower', 0))
                self.assertGreater(on_power, 1.0, "VO2max on power should be > 100%")
                break

    def test_g_spot_power_in_range(self):
        """G-Spot workout power should be 87-92% FTP."""
        zwo = generate_nate_zwo('g_spot', 4, 'G_SPOT')
        parsed = parse_zwo_to_dict(zwo)
        self.assertIsNotNone(parsed)

        # Find G-Spot power in either SteadyState or IntervalsT blocks
        found_g_spot_power = False
        for block in parsed['blocks']:
            if block['type'] == 'SteadyState':
                power = float(block['attributes'].get('Power', 0))
                # G-Spot range is 0.85-0.95 (allowing some tolerance)
                if 0.85 <= power <= 0.95:
                    found_g_spot_power = True
                    break
            elif block['type'] == 'IntervalsT':
                on_power = float(block['attributes'].get('OnPower', 0))
                # G-Spot intervals should be in the 87-92% range
                if 0.85 <= on_power <= 0.95:
                    found_g_spot_power = True
                    break

        self.assertTrue(found_g_spot_power, "Should find G-Spot power in 85-95% range")


class TestZWODurations(unittest.TestCase):
    """Test that workout durations are reasonable."""

    def test_recovery_is_short(self):
        """Recovery workout should be relatively short."""
        zwo = generate_nate_zwo('recovery', 4, 'POLARIZED')
        parsed = parse_zwo_to_dict(zwo)
        self.assertIsNotNone(parsed)

        # Recovery should be 30-60 minutes
        self.assertLessEqual(parsed['total_duration'], 3600, "Recovery should be <= 60 min")
        self.assertGreaterEqual(parsed['total_duration'], 1800, "Recovery should be >= 30 min")

    def test_vo2max_has_reasonable_duration(self):
        """VO2max workout should be 45-90 minutes."""
        zwo = generate_nate_zwo('vo2max', 4, 'POLARIZED')
        parsed = parse_zwo_to_dict(zwo)
        self.assertIsNotNone(parsed)

        self.assertGreaterEqual(parsed['total_duration'], 2700, "VO2max should be >= 45 min")
        self.assertLessEqual(parsed['total_duration'], 5400, "VO2max should be <= 90 min")


class TestAllArchetypesGenerateValidZWO(unittest.TestCase):
    """Test that every archetype category generates valid ZWO."""

    def test_all_categories_generate_valid_xml(self):
        """Every archetype category should produce valid XML."""
        # Map categories to workout types
        category_to_type = {
            'VO2max': 'vo2max',
            'TT_Threshold': 'threshold',
            'Sprint_Neuromuscular': 'sprint',
            'Anaerobic_Capacity': 'anaerobic',
            'Durability': 'durability',
            'Endurance': 'endurance',
            'Race_Simulation': 'race_sim',
            'G_Spot': 'g_spot',
            'LT1_MAF': 'lt1',
            'Critical_Power': 'cp',
            'Norwegian_Double': 'norwegian',
            'HVLI_Extended': 'hvli',
            'Testing': 'test',
            'Recovery': 'recovery',
            'INSCYD': 'inscyd',
        }

        for category, workout_type in category_to_type.items():
            with self.subTest(category=category):
                # Skip categories that return None for some methodologies
                zwo = generate_nate_zwo(workout_type, 4, 'POLARIZED')
                if zwo is not None:  # Some may be None if methodology avoids them
                    is_valid, errors = validate_zwo_xml(zwo)
                    self.assertTrue(is_valid, f"{category} errors: {errors}")


class TestZWORoundTrip(unittest.TestCase):
    """Test that ZWO can be parsed and key values extracted correctly."""

    def test_name_survives_roundtrip(self):
        """Workout name should survive generation and parsing."""
        custom_name = "Test VO2max Workout"
        zwo = generate_nate_zwo('vo2max', 4, 'POLARIZED', 0, custom_name)
        parsed = parse_zwo_to_dict(zwo)

        self.assertIsNotNone(parsed)
        self.assertEqual(parsed['name'], custom_name)

    def test_blocks_are_preserved(self):
        """Workout blocks should be preserved in parsing."""
        zwo = generate_nate_zwo('vo2max', 4, 'POLARIZED')
        parsed = parse_zwo_to_dict(zwo)

        self.assertIsNotNone(parsed)
        self.assertGreater(len(parsed['blocks']), 0)

        # Should have warmup, intervals, cooldown at minimum
        block_types = [b['type'] for b in parsed['blocks']]
        self.assertIn('Warmup', block_types)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions."""

    def test_level_1_generates_valid_xml(self):
        """Level 1 (minimum) should generate valid XML."""
        zwo = generate_nate_zwo('vo2max', 1, 'POLARIZED')
        self.assertIsNotNone(zwo)
        is_valid, errors = validate_zwo_xml(zwo)
        self.assertTrue(is_valid, f"Level 1 errors: {errors}")

    def test_level_6_generates_valid_xml(self):
        """Level 6 (maximum) should generate valid XML."""
        zwo = generate_nate_zwo('vo2max', 6, 'POLARIZED')
        self.assertIsNotNone(zwo)
        is_valid, errors = validate_zwo_xml(zwo)
        self.assertTrue(is_valid, f"Level 6 errors: {errors}")

    def test_special_characters_in_name_escaped(self):
        """Special characters in workout name should be XML-escaped."""
        name_with_special = "Test <VO2> & 'Threshold' \"Workout\""
        zwo = generate_nate_zwo('vo2max', 4, 'POLARIZED', 0, name_with_special)
        self.assertIsNotNone(zwo)

        # Should still parse
        is_valid, errors = validate_zwo_xml(zwo)
        self.assertTrue(is_valid, f"Special char errors: {errors}")


if __name__ == '__main__':
    unittest.main(verbosity=2)
