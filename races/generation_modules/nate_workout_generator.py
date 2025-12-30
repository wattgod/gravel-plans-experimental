#!/usr/bin/env python3
"""
NATE WORKOUT GENERATOR - Full Integration
==========================================
Generates complete ZWO workouts from the Nate archetype library.

This generator uses ACTUAL workout structures from archetypes, not just descriptions.
It produces complete ZWO files with proper intervals, power targets, and progressions.

Features:
- 22 archetypes × 6 levels = 132 unique workouts
- Methodology-driven selection (POLARIZED, PYRAMIDAL, HIT)
- Full block generation (intervals, ramps, pyramids, etc.)
- Durability workouts for ultra-distance events
- Race simulation workouts

Categories:
- VO2max (4 archetypes): 5x3 Classic, Descending Pyramid, Norwegian 4x8, Loaded Recovery
- TT_Threshold (3 archetypes): Single Sustained, Threshold Ramps, Descending Threshold
- Sprint_Neuromuscular (4 archetypes): Attack Repeats, Sprint Buildups, Peak and Fade, ILT
- Anaerobic_Capacity (3 archetypes): 2min Killers, 90sec Repeats, 1min All-Out
- Durability (3 archetypes): Tired VO2max, Double Day Sim, Progressive Fatigue
- Endurance (2 archetypes): Pre-Race Openers, Terrain Simulation Z2
- Race_Simulation (3 archetypes): Breakaway Sim, Variable Pace Chaos, Sector Sim

Version: 1.0 (Full Nate Integration)
"""

import html
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

# Import Nate archetypes
sys.path.insert(0, str(Path(__file__).parent.parent / "nate_archetypes"))
from new_archetypes import (
    NEW_ARCHETYPES,
    VO2MAX_NEW,
    THRESHOLD_NEW,
    SPRINT_NEW,
    ANAEROBIC_CAPACITY,
    DURABILITY_NEW,
    ENDURANCE_NEW,
    RACE_SIMULATION
)

# =============================================================================
# ZWO TEMPLATE
# =============================================================================

ZWO_TEMPLATE = """<?xml version='1.0' encoding='UTF-8'?>
<workout_file>
  <author>Gravel God Training</author>
  <name>{name}</name>
  <description>{description}</description>
  <sportType>bike</sportType>
      <workout>
{blocks}  </workout>
</workout_file>"""


# =============================================================================
# TRAINING METHODOLOGY CONFIGURATION
# =============================================================================

TRAINING_METHODOLOGIES = {
    "POLARIZED": {
        "name": "Polarized (80/20)",
        "description": "75-80% Z1-Z2, 15-20% Z4-Z5+, <5% Z3",
        "primary_workouts": ["VO2max", "Sprint_Neuromuscular", "Anaerobic_Capacity"],
        "secondary_workouts": ["Durability", "Race_Simulation"],
        "avoid": [],  # No Sweet Spot
        "weekly_quality_sessions": 2,
        "allows_durability": True,
        "g_spot_usage": "durability_only"
    },
    "PYRAMIDAL": {
        "name": "Pyramidal",
        "description": "75-80% Z1-Z2, 10-15% Z3, 5-10% Z4-Z5+",
        "primary_workouts": ["TT_Threshold"],
        "secondary_workouts": ["VO2max", "Anaerobic_Capacity", "Race_Simulation"],
        "avoid": [],
        "weekly_quality_sessions": 2,
        "allows_durability": True,
        "g_spot_usage": "regular"
    },
    "HIT": {
        "name": "High Intensity Training",
        "description": "60-70% Z1-Z2, 20-30% Z4-Z5+",
        "primary_workouts": ["VO2max", "Anaerobic_Capacity", "Sprint_Neuromuscular"],
        "secondary_workouts": ["TT_Threshold"],
        "avoid": ["Durability"],  # Skip long durability for time-crunched
        "weekly_quality_sessions": 3,
        "allows_durability": False,
        "g_spot_usage": "minimal"
    }
}


# =============================================================================
# ARCHETYPE SELECTION
# =============================================================================

def get_archetype_by_category_and_index(category: str, index: int = 0) -> Optional[Dict]:
    """Get a specific archetype from a category by index."""
    if category not in NEW_ARCHETYPES:
        return None

    archetypes = NEW_ARCHETYPES[category]
    if index >= len(archetypes):
        index = 0

    return archetypes[index]


def get_all_archetypes_for_category(category: str) -> List[Dict]:
    """Get all archetypes for a category."""
    return NEW_ARCHETYPES.get(category, [])


def select_archetype_for_workout(
    workout_type: str,
    methodology: str = "POLARIZED",
    variation: int = 0
) -> Optional[Dict]:
    """
    Select an archetype based on workout type and methodology.

    Args:
        workout_type: The type of workout (vo2max, threshold, sprint, etc.)
        methodology: Training methodology (POLARIZED, PYRAMIDAL, HIT)
        variation: Which variation of the archetype to use (0-indexed)

    Returns:
        The selected archetype dictionary, or None if not found
    """
    # Map workout types to categories
    type_to_category = {
        "vo2max": "VO2max",
        "vo2": "VO2max",
        "threshold": "TT_Threshold",
        "tt": "TT_Threshold",
        "ftp": "TT_Threshold",
        "sprint": "Sprint_Neuromuscular",
        "neuromuscular": "Sprint_Neuromuscular",
        "anaerobic": "Anaerobic_Capacity",
        "durability": "Durability",
        "tired": "Durability",
        "endurance": "Endurance",
        "openers": "Endurance",
        "race_sim": "Race_Simulation",
        "race_simulation": "Race_Simulation",
        "breakaway": "Race_Simulation",
        "sector": "Race_Simulation"
    }

    category = type_to_category.get(workout_type.lower())
    if not category:
        return None

    # Check if this category is avoided by the methodology
    method_config = TRAINING_METHODOLOGIES.get(methodology, TRAINING_METHODOLOGIES["POLARIZED"])
    if category in method_config.get("avoid", []):
        return None

    return get_archetype_by_category_and_index(category, variation)


def calculate_level_from_week(
    week_num: int,
    total_weeks: int,
    taper_weeks: int = 2
) -> int:
    """
    Calculate the progression level (1-6) based on week position.

    Accounts for taper period at the end of the plan.
    """
    # Exclude taper weeks from progression
    build_weeks = total_weeks - taper_weeks

    if week_num >= build_weeks:
        # In taper - use level 3-4 (maintain without max stress)
        return 4

    # Linear progression through build phase
    progress = week_num / build_weeks

    if progress < 0.17:
        return 1
    elif progress < 0.33:
        return 2
    elif progress < 0.50:
        return 3
    elif progress < 0.67:
        return 4
    elif progress < 0.83:
        return 5
    else:
        return 6


def get_level_data(archetype: Dict, level: int) -> Optional[Dict]:
    """Get the data for a specific level of an archetype."""
    if not archetype or "levels" not in archetype:
        return None

    level_key = str(level)
    if level_key not in archetype["levels"]:
        # Fall back to closest available level
        available = sorted([int(k) for k in archetype["levels"].keys()])
        if not available:
            return None
        level_key = str(min(available, key=lambda x: abs(x - level)))

    return archetype["levels"].get(level_key)


# =============================================================================
# ZWO BLOCK GENERATION
# =============================================================================

def generate_warmup_block(duration: int = 900) -> str:
    """Generate warmup block."""
    return f'    <Warmup Duration="{duration}" PowerLow="0.50" PowerHigh="0.75"/>\n'


def generate_cooldown_block(duration: int = 600) -> str:
    """Generate cooldown block."""
    return f'    <Cooldown Duration="{duration}" PowerLow="0.70" PowerHigh="0.50"/>\n'


def generate_steady_state_block(duration: int, power: float, cadence: int = None) -> str:
    """Generate a steady state block."""
    cadence_attr = f' Cadence="{cadence}"' if cadence else ""
    return f'    <SteadyState Duration="{duration}" Power="{power:.2f}"{cadence_attr}/>\n'


def generate_intervals_block(
    repeats: int,
    on_duration: int,
    on_power: float,
    off_duration: int,
    off_power: float = 0.55,
    cadence: int = 90
) -> str:
    """Generate an IntervalsT block."""
    return (
        f'    <IntervalsT Repeat="{repeats}" '
        f'OnDuration="{on_duration}" OnPower="{on_power:.2f}" '
        f'Cadence="{cadence}" OffDuration="{off_duration}" '
        f'OffPower="{off_power:.2f}"/>\n'
    )


def generate_ramp_block(
    duration: int,
    power_low: float,
    power_high: float
) -> str:
    """Generate a ramp block."""
    return (
        f'    <Ramp Duration="{duration}" '
        f'PowerLow="{power_low:.2f}" PowerHigh="{power_high:.2f}"/>\n'
    )


def generate_blocks_from_archetype(archetype: Dict, level: int) -> str:
    """
    Generate ZWO XML blocks from a Nate archetype level.

    This is the main block generation function that handles all archetype types.
    """
    level_data = get_level_data(archetype, level)
    if not level_data:
        return generate_warmup_block() + generate_cooldown_block()

    blocks = []

    # Default warmup
    warmup_duration = level_data.get("warmup_duration", 900)

    # =====================================================================
    # DURABILITY WORKOUTS (Tired VO2, etc.)
    # =====================================================================
    if "tired_vo2" in level_data or "base_duration" in level_data:
        base_duration = level_data.get("base_duration", 7200)
        base_power = level_data.get("base_power", 0.70)

        blocks.append(generate_warmup_block())
        blocks.append(generate_steady_state_block(base_duration, base_power))

        if "intervals" in level_data and isinstance(level_data["intervals"], tuple):
            repeats, duration = level_data["intervals"]
            on_power = level_data.get("on_power", 1.10)
            off_duration = level_data.get("off_duration", 240)
            off_power = level_data.get("off_power", 0.55)
            blocks.append(generate_intervals_block(
                repeats, duration, on_power, off_duration, off_power
            ))

    # =====================================================================
    # STANDARD INTERVALS (VO2, Threshold, Anaerobic, Sprint)
    # =====================================================================
    elif "intervals" in level_data and isinstance(level_data["intervals"], tuple):
        repeats, duration = level_data["intervals"]
        on_power = level_data.get("on_power", 1.0)
        off_power = level_data.get("off_power", 0.55)
        off_duration = level_data.get("off_duration", level_data.get("duration", 180))
        actual_duration = level_data.get("duration", duration)
        cadence = level_data.get("cadence", 90)

        blocks.append(generate_warmup_block())
        blocks.append(generate_intervals_block(
            repeats, actual_duration, on_power, off_duration, off_power, cadence
        ))

    # =====================================================================
    # PYRAMID / DESCENDING EFFORTS
    # =====================================================================
    elif "pyramid" in level_data or "descending" in level_data:
        recovery_duration = level_data.get("recovery_duration", 180)
        efforts = level_data.get("efforts", [])
        sets = level_data.get("sets", 1)
        set_recovery = level_data.get("set_recovery", 300)

        blocks.append(generate_warmup_block())

        for set_num in range(int(sets)):
            for i, effort in enumerate(efforts):
                if isinstance(effort, dict):
                    duration = effort.get("duration", 300)
                    power = effort.get("power", 1.0)
                    blocks.append(generate_steady_state_block(duration, power))

                    if i < len(efforts) - 1:
                        blocks.append(generate_steady_state_block(recovery_duration, 0.55))

            # Set recovery (if multiple sets)
            if sets > 1 and set_num < int(sets) - 1:
                blocks.append(generate_steady_state_block(set_recovery, 0.55))

    # =====================================================================
    # SINGLE SUSTAINED EFFORT (Long Threshold)
    # =====================================================================
    elif "single_effort" in level_data:
        duration = level_data.get("duration", 1200)
        power = level_data.get("power", 1.0)

        blocks.append(generate_warmup_block(1200))  # Longer warmup for TT
        blocks.append(generate_steady_state_block(duration, power, cadence=90))

    # =====================================================================
    # RAMP INTERVALS (Threshold Ramps)
    # =====================================================================
    elif "ramp" in level_data:
        intervals_data = level_data.get("intervals", (2, 720))
        if isinstance(intervals_data, tuple):
            repeats, ramp_duration = intervals_data
        else:
            repeats = 2
            ramp_duration = 720

        start_power = level_data.get("start_power", 0.88)
        end_power = level_data.get("end_power", 1.00)
        off_duration = level_data.get("off_duration", 300)

        blocks.append(generate_warmup_block())

        for rep in range(repeats):
            blocks.append(generate_ramp_block(ramp_duration, start_power, end_power))
            if rep < repeats - 1:
                blocks.append(generate_steady_state_block(off_duration, 0.55))

    # =====================================================================
    # LOADED RECOVERY (VO2 + Tempo)
    # =====================================================================
    elif "loaded_recovery" in level_data:
        intervals_data = level_data.get("intervals", (3, 180))
        if isinstance(intervals_data, tuple):
            repeats = intervals_data[0]
        else:
            repeats = 3

        on_duration = level_data.get("duration", 180)
        on_power = level_data.get("on_power", 1.15)
        loaded_duration = level_data.get("loaded_duration", 120)
        loaded_power = level_data.get("loaded_power", 0.85)
        off_duration = level_data.get("off_duration", 180)

        blocks.append(generate_warmup_block())

        for rep in range(repeats):
            blocks.append(generate_steady_state_block(on_duration, on_power))
            blocks.append(generate_steady_state_block(loaded_duration, loaded_power))
            if rep < repeats - 1:
                blocks.append(generate_steady_state_block(off_duration, 0.50))

    # =====================================================================
    # PEAK AND FADE (Sprint)
    # =====================================================================
    elif "peak_fade" in level_data:
        intervals_data = level_data.get("intervals", (4, 30))
        if isinstance(intervals_data, tuple):
            repeats = intervals_data[0]
        else:
            repeats = 4

        peak_duration = level_data.get("peak_duration", 10)
        peak_power = level_data.get("peak_power", 2.0)
        fade_duration = level_data.get("fade_duration", 20)
        fade_power = level_data.get("fade_power", 1.2)
        off_duration = level_data.get("off_duration", 180)

        blocks.append(generate_warmup_block())

        for rep in range(repeats):
            blocks.append(generate_steady_state_block(peak_duration, peak_power))
            blocks.append(generate_steady_state_block(fade_duration, fade_power))
            if rep < repeats - 1:
                blocks.append(generate_steady_state_block(off_duration, 0.50))

    # =====================================================================
    # BREAKAWAY SIMULATION
    # =====================================================================
    elif "breakaway" in level_data:
        repeats = level_data.get("intervals", 2)
        attack_duration = level_data.get("attack_duration", 300)
        attack_power = level_data.get("attack_power", 1.10)
        hold_duration = level_data.get("hold_duration", 600)
        hold_power = level_data.get("hold_power", 0.88)
        recovery_duration = level_data.get("recovery_duration", 300)

        blocks.append(generate_warmup_block())

        for rep in range(repeats):
            blocks.append(generate_steady_state_block(attack_duration, attack_power))
            blocks.append(generate_steady_state_block(hold_duration, hold_power))
            if rep < repeats - 1:
                blocks.append(generate_steady_state_block(recovery_duration, 0.55))

    # =====================================================================
    # SECTOR SIMULATION
    # =====================================================================
    elif "sector_sim" in level_data:
        sectors_per_set = level_data.get("sectors_per_set", 2)
        sets = level_data.get("sets", 2)
        sector_duration = level_data.get("sector_duration", 90)
        sector_power = level_data.get("sector_power", 1.30)
        sector_recovery = level_data.get("sector_recovery", 180)
        sector_recovery_power = level_data.get("sector_recovery_power", 0.75)
        set_recovery = level_data.get("set_recovery", 300)

        blocks.append(generate_warmup_block())

        for set_num in range(sets):
            for sector in range(sectors_per_set):
                blocks.append(generate_steady_state_block(sector_duration, sector_power))
                blocks.append(generate_steady_state_block(sector_recovery, sector_recovery_power))

            if set_num < sets - 1:
                blocks.append(generate_steady_state_block(set_recovery, 0.65))

    # =====================================================================
    # OPENERS
    # =====================================================================
    elif "openers" in level_data:
        warmup_duration = level_data.get("warmup_duration", 1200)
        warmup_power = level_data.get("warmup_power", 0.65)
        efforts_data = level_data.get("efforts", (3, 30))
        if isinstance(efforts_data, tuple):
            effort_count, effort_duration = efforts_data
        else:
            effort_count, effort_duration = 3, 30
        effort_power = level_data.get("effort_power", 1.10)
        effort_recovery = level_data.get("effort_recovery", 120)
        cooldown_duration = level_data.get("cooldown_duration", 300)

        blocks.append(generate_steady_state_block(warmup_duration, warmup_power))

        for i in range(effort_count):
            blocks.append(generate_steady_state_block(effort_duration, effort_power))
            if i < effort_count - 1:
                blocks.append(generate_steady_state_block(effort_recovery, 0.55))

        blocks.append(generate_steady_state_block(cooldown_duration, 0.50))
        return "".join(blocks)  # Return early - no standard cooldown

    # =====================================================================
    # PROGRESSIVE FATIGUE
    # =====================================================================
    elif "progressive_fatigue" in level_data:
        num_intervals = level_data.get("intervals", 3)
        effort_duration = level_data.get("effort_duration", 600)
        on_power = level_data.get("on_power", 0.98)
        recovery_sequence = level_data.get("recovery_sequence", [300, 240, 180])

        blocks.append(generate_warmup_block())

        for i in range(num_intervals):
            blocks.append(generate_steady_state_block(effort_duration, on_power))
            if i < len(recovery_sequence):
                blocks.append(generate_steady_state_block(recovery_sequence[i], 0.55))

    # =====================================================================
    # DEFAULT FALLBACK
    # =====================================================================
    elif "on_power" in level_data:
        duration = level_data.get("duration", 300)
        on_power = level_data.get("on_power", 1.0)
        blocks.append(generate_warmup_block())
        blocks.append(generate_steady_state_block(duration, on_power))

    else:
        # No recognized structure - just warmup and cooldown
        blocks.append(generate_warmup_block())

    # Add cooldown
    blocks.append(generate_cooldown_block())

    return "".join(blocks)


# =============================================================================
# DESCRIPTION GENERATION
# =============================================================================

def generate_description(
    archetype: Dict,
    level: int,
    methodology: str = "POLARIZED",
    include_dimensions: bool = True
) -> str:
    """Generate a workout description from an archetype."""
    level_data = get_level_data(archetype, level)
    if not level_data:
        return ""

    lines = []

    # WARM-UP
    lines.append("WARM-UP:")
    lines.append("• 15min building from Z1 to Z2")
    lines.append("")

    # MAIN SET
    lines.append("MAIN SET:")
    lines.append(f"• {level_data.get('structure', 'See workout structure')}")

    # Dimensions
    if include_dimensions:
        cadence = level_data.get("cadence_prescription")
        position = level_data.get("position_prescription")

        if cadence:
            lines.append(f"• Cadence: {cadence}")
        if position:
            lines.append(f"• Position: {position}")

    lines.append("")

    # COOL-DOWN
    lines.append("COOL-DOWN:")
    lines.append("• 10min easy spin Z1-Z2")
    lines.append("")

    # PURPOSE
    lines.append("PURPOSE:")
    category_purpose = get_category_purpose(archetype["name"])
    lines.append(category_purpose)
    lines.append("")
    lines.append(f"Level {level}: {level_data.get('execution', 'Progressive development')}")

    # Fueling
    fueling = level_data.get("fueling")
    if fueling:
        lines.append("")
        lines.append(f"• FUELING: {fueling}")

    return "\n".join(lines)


def get_category_purpose(archetype_name: str) -> str:
    """Get the purpose description for a workout category."""
    purposes = {
        "VO2": "VO2max development. Maximum aerobic power—the engine that drives race-winning attacks.",
        "Threshold": "Threshold development. The power you can sustain for 20-60 minutes.",
        "Sprint": "Neuromuscular power. Explosive capacity for attacks and race-winning moves.",
        "Anaerobic": "Anaerobic capacity. Lactate tolerance and race-breaking repeated power.",
        "Tired": "Durability training. Quality efforts when fatigued—ultra-distance racing demands this.",
        "Double": "Durability training. Stage race and back-to-back training simulation.",
        "Progressive": "Progressive fatigue. Building threshold under accumulating fatigue.",
        "Breakaway": "Race simulation. Attack-and-hold pattern that wins breakaways.",
        "Sector": "Gravel sector simulation. Hard efforts followed by recovery—the rhythm of gravel.",
        "Variable": "Variable pace training. Unpredictable power changes mirroring real race dynamics.",
        "Chaos": "Variable pace training. Unpredictable power changes mirroring real race dynamics.",
        "Opener": "Pre-race activation. Wake up the legs without creating fatigue.",
        "Terrain": "Terrain simulation. Variable power within Z2 for rolling course preparation.",
        "Attack": "Attack training. Race-breaking sprint efforts.",
        "Peak": "Sprint development. Explosive start with controlled fade.",
        "ILT": "Pedaling efficiency. Isolated leg training for smooth power delivery.",
        "Buildup": "Sprint development. Progressive duration at maximum power.",
        "Killer": "Lactate tolerance. 2-minute efforts at race-breaking intensity.",
        "90sec": "Anaerobic power. Short, sharp race-breaking efforts.",
        "1min": "Maximum power. All-out neuromuscular + anaerobic efforts.",
        "Ramp": "Threshold development. Progressive building teaches negative splitting.",
        "Descending": "Threshold development. Shorter and harder as you tire.",
        "Single": "Mental toughness. One long sustained effort, no breaks.",
        "Norwegian": "VO2max development. Research-backed Seiler format for masters athletes."
    }

    for key, purpose in purposes.items():
        if key.lower() in archetype_name.lower():
            return purpose

    return "Quality training. Building race-specific fitness through structured work."


# =============================================================================
# MAIN WORKOUT GENERATION
# =============================================================================

def generate_nate_workout(
    workout_type: str,
    level: int = 3,
    methodology: str = "POLARIZED",
    variation: int = 0,
    workout_name: str = None
) -> Tuple[str, str, str]:
    """
    Generate a complete Nate workout.

    Args:
        workout_type: Type of workout (vo2max, threshold, sprint, etc.)
        level: Progression level (1-6)
        methodology: Training methodology (POLARIZED, PYRAMIDAL, HIT)
        variation: Which archetype variation to use (0-indexed)
        workout_name: Optional custom name for the workout

    Returns:
        Tuple of (name, description, blocks)
    """
    archetype = select_archetype_for_workout(workout_type, methodology, variation)

    if not archetype:
        return None, None, None

    # Generate name
    name = workout_name or f"{archetype['name']} L{level}"

    # Generate description
    description = generate_description(archetype, level, methodology)

    # Generate blocks
    blocks = generate_blocks_from_archetype(archetype, level)

    return name, description, blocks


def generate_nate_zwo(
    workout_type: str,
    level: int = 3,
    methodology: str = "POLARIZED",
    variation: int = 0,
    workout_name: str = None
) -> str:
    """
    Generate a complete ZWO file from a Nate archetype.

    Returns the complete ZWO XML content.
    """
    name, description, blocks = generate_nate_workout(
        workout_type, level, methodology, variation, workout_name
    )

    if not name:
        return None

    # Escape XML
    name_escaped = html.escape(name, quote=False)
    desc_escaped = html.escape(description, quote=False)

    return ZWO_TEMPLATE.format(
        name=name_escaped,
        description=desc_escaped,
        blocks=blocks
    )


# =============================================================================
# WEEKLY PLAN GENERATION
# =============================================================================

def generate_weekly_workout_schedule(
    methodology: str = "POLARIZED",
    week_num: int = 6,
    total_weeks: int = 12,
    days_available: int = 6
) -> List[Dict]:
    """
    Generate a week's worth of workouts based on methodology.

    Returns a list of workout specifications for each day.
    """
    method_config = TRAINING_METHODOLOGIES.get(methodology, TRAINING_METHODOLOGIES["POLARIZED"])
    level = calculate_level_from_week(week_num, total_weeks)

    # Base structure for polarized training
    if methodology == "POLARIZED":
        schedule = [
            {"day": "Mon", "type": "rest", "name": "Rest Day"},
            {"day": "Tue", "type": "vo2max", "name": "VO2max Session"},
            {"day": "Wed", "type": "endurance", "name": "Easy Endurance"},
            {"day": "Thu", "type": "threshold", "name": "Threshold Touch"},
            {"day": "Fri", "type": "endurance", "name": "Easy Endurance"},
            {"day": "Sat", "type": "endurance", "name": "Long Endurance"},
            {"day": "Sun", "type": "endurance", "name": "Easy Endurance"}
        ]
    elif methodology == "PYRAMIDAL":
        schedule = [
            {"day": "Mon", "type": "rest", "name": "Rest Day"},
            {"day": "Tue", "type": "threshold", "name": "Threshold Session"},
            {"day": "Wed", "type": "endurance", "name": "Easy Endurance"},
            {"day": "Thu", "type": "vo2max", "name": "VO2max Touch"},
            {"day": "Fri", "type": "endurance", "name": "Easy Endurance"},
            {"day": "Sat", "type": "endurance", "name": "Long Endurance"},
            {"day": "Sun", "type": "threshold", "name": "Threshold/Tempo"}
        ]
    else:  # HIT
        schedule = [
            {"day": "Mon", "type": "rest", "name": "Rest Day"},
            {"day": "Tue", "type": "vo2max", "name": "VO2max Session"},
            {"day": "Wed", "type": "rest", "name": "Rest Day"},
            {"day": "Thu", "type": "anaerobic", "name": "Anaerobic Session"},
            {"day": "Fri", "type": "endurance", "name": "Easy Endurance"},
            {"day": "Sat", "type": "sprint", "name": "Sprint Session"},
            {"day": "Sun", "type": "rest", "name": "Rest Day"}
        ]

    # Add level to each workout
    for workout in schedule:
        workout["level"] = level
        workout["week"] = week_num

    return schedule[:days_available + 1]


# =============================================================================
# MAIN / TESTING
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("NATE WORKOUT GENERATOR - Full Integration Test")
    print("=" * 70)

    # Test archetype counts
    total = sum(len(archs) for archs in NEW_ARCHETYPES.values())
    print(f"\nArchetypes loaded: {total}")
    print(f"Total variations: {total * 6}")

    print("\n" + "-" * 70)
    print("SAMPLE WORKOUT GENERATION:")
    print("-" * 70)

    # Generate a sample VO2max workout
    zwo_content = generate_nate_zwo(
        workout_type="vo2max",
        level=4,
        methodology="POLARIZED",
        variation=0
    )

    if zwo_content:
        print("\nGenerated VO2max Workout (Level 4, POLARIZED):")
        print("-" * 40)
        print(zwo_content[:2000])  # First 2000 chars
        if len(zwo_content) > 2000:
            print("... [truncated]")

    print("\n" + "-" * 70)
    print("DURABILITY WORKOUT:")
    print("-" * 70)

    # Generate a durability workout
    zwo_durability = generate_nate_zwo(
        workout_type="durability",
        level=4,
        methodology="POLARIZED",
        variation=0
    )

    if zwo_durability:
        print("\nGenerated Durability Workout (Tired VO2max, Level 4):")
        print("-" * 40)
        print(zwo_durability[:2000])

    print("\n" + "-" * 70)
    print("RACE SIMULATION:")
    print("-" * 70)

    # Generate a race simulation
    zwo_race = generate_nate_zwo(
        workout_type="race_sim",
        level=3,
        methodology="POLARIZED",
        variation=0  # Breakaway Simulation
    )

    if zwo_race:
        print("\nGenerated Race Simulation (Breakaway, Level 3):")
        print("-" * 40)
        print(zwo_race[:2000])

    print("\n" + "=" * 70)
    print("TEST COMPLETE")
    print("=" * 70)
