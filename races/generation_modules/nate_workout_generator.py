#!/usr/bin/env python3
"""
NATE WORKOUT GENERATOR - Full Integration
==========================================

Generates complete ZWO workouts from the Nate archetype library.

This generator uses ACTUAL workout structures from archetypes, not just descriptions.
It produces complete ZWO files with proper intervals, power targets, and progressions.

Features
--------
- 41 archetypes × 6 levels = 246 unique workout variations
- 14 training methodologies (POLARIZED, PYRAMIDAL, G_SPOT, HIT, etc.)
- 8 progression styles for periodization
- Full block generation (intervals, ramps, pyramids, etc.)
- Methodology-aware archetype selection
- Durability workouts for ultra-distance events
- Race simulation workouts

Categories
----------
- VO2max (4 archetypes): 5x3 Classic, Descending Pyramid, Norwegian 4x8, Loaded Recovery
- TT_Threshold (3 archetypes): Single Sustained, Threshold Ramps, Descending Threshold
- Sprint_Neuromuscular (4 archetypes): Attack Repeats, Sprint Buildups, Peak and Fade, ILT
- Anaerobic_Capacity (3 archetypes): 2min Killers, 90sec Repeats, 1min All-Out
- Durability (3 archetypes): Tired VO2max, Double Day Sim, Progressive Fatigue
- Endurance (2 archetypes): Pre-Race Openers, Terrain Simulation Z2
- Race_Simulation (3 archetypes): Breakaway Sim, Variable Pace Chaos, Sector Sim
- G_Spot (3 archetypes): Standard, Extended, Criss-Cross
- LT1_MAF (3 archetypes): LT1 Capped, MAF Test, Aerobic Base
- Critical_Power (3 archetypes): Above CP Repeats, W' Depletion, CP Test
- Norwegian_Double (3 archetypes): 4x8 Classic, Double AM, Double PM
- HVLI_Extended (2 archetypes): Extended Z2, Terrain Simulation
- Testing (3 archetypes): Ramp Test, 20min FTP, CP Test Protocol
- Recovery (3 archetypes): Active Recovery, Flush Ride, Rest Day
- INSCYD (2 archetypes): VLamax Reduction, Carb Tolerance

Notes
-----
G-Spot (87-92% FTP) replaces Sweet Spot throughout this generator.

Version: 2.0 (Full Methodology Support)
"""

import html
import logging
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Union

# Import constants
from constants import (
    PowerZones,
    CriticalPower,
    Durations,
    Cadence,
    Levels,
    ValidationLimits,
    ZWODefaults,
    MethodologyDefaults,
)

# =============================================================================
# LOGGING CONFIGURATION
# =============================================================================

def configure_logging(level: int = logging.INFO) -> logging.Logger:
    """
    Configure logging for the workout generator.

    Args:
        level: Logging level (default: INFO)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(__name__)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    logger.setLevel(level)
    return logger

logger = configure_logging(logging.WARNING)  # Default to WARNING to reduce noise

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
# TRAINING METHODOLOGY CONFIGURATION - ALL 14 SYSTEMS
# =============================================================================
# Based on endurance_training_systems_master_table.xlsx
# NO Sweet Spot - G-Spot (87-92% FTP) only

TRAINING_METHODOLOGIES = {
    # =========================================================================
    # 1. TRADITIONAL PYRAMIDAL
    # =========================================================================
    "PYRAMIDAL": {
        "name": "Traditional Pyramidal",
        "description": "Build large aerobic base, then sharpen with intensity. 75-80% Z1-Z2, 10-15% Z3, 5-10% Z4-Z5+",
        "philosophy": "Volume → intensity → density (then specificity)",
        "primary_workouts": ["TT_Threshold", "G_Spot"],
        "secondary_workouts": ["VO2max", "Anaerobic_Capacity", "Race_Simulation"],
        "avoid": [],
        "weekly_quality_sessions": 2,
        "allows_durability": True,
        "progression_style": "volume_first",  # Volume increases, then intensity
        "load_metric": "CTL + decoupling",
        "best_for": "≥10 h/wk + multi-hour sessions",
        "macro_phases": ["base", "build", "peak", "taper"],
        "meso_pattern": "3:1",  # 3 weeks load, 1 week deload
    },

    # =========================================================================
    # 2. POLARIZED (80/20)
    # =========================================================================
    "POLARIZED": {
        "name": "Polarized (80/20)",
        "description": "Most training easy, small amount very hard, minimal middle zone. ~80% Z1-Z2, ~20% Z4-Z5+",
        "philosophy": "Strict hard/easy separation - keep easy truly easy",
        "primary_workouts": ["VO2max", "Sprint_Neuromuscular", "Anaerobic_Capacity"],
        "secondary_workouts": ["Durability", "Race_Simulation"],
        "avoid": ["G_Spot"],  # Minimal Z3 work
        "weekly_quality_sessions": 2,
        "allows_durability": True,
        "progression_style": "intensity_stable",  # Increment intensity while keeping volume/ratio stable
        "load_metric": "% time in Zone1 + interval power",
        "best_for": "8-15 h/wk",
        "macro_phases": ["year_round_80_20"],
        "meso_pattern": "maintain_ratio",
    },

    # =========================================================================
    # 3. G-SPOT / THRESHOLD (NOT Sweet Spot)
    # =========================================================================
    "G_SPOT": {
        "name": "G-Spot / Threshold",
        "description": "Emphasize sub-threshold intervals at 87-92% FTP (reality-adjusted zone). Time-efficient FTP gains.",
        "philosophy": "Maximize threshold adaptation without the lies of 'Sweet Spot'",
        "primary_workouts": ["G_Spot", "TT_Threshold"],
        "secondary_workouts": ["VO2max", "Endurance"],
        "avoid": [],
        "weekly_quality_sessions": 3,
        "allows_durability": False,
        "progression_style": "density_increase",  # More minutes at G-Spot, more sessions
        "load_metric": "TSS/hr + FTP increases",
        "best_for": "6-10 h/wk (moderate hours)",
        "macro_phases": ["compressed_base", "build", "peak"],
        "meso_pattern": "progressive_density",
    },

    # =========================================================================
    # 4. HIIT-FOCUSED
    # =========================================================================
    "HIT": {
        "name": "HIIT-Focused",
        "description": "Frequent maximal intervals, minimal volume. 60-70% Z1-Z2, 20-30% Z4-Z5+",
        "philosophy": "Leverage stimulus of high intensity for fast gains",
        "primary_workouts": ["VO2max", "Anaerobic_Capacity", "Sprint_Neuromuscular"],
        "secondary_workouts": ["TT_Threshold"],
        "avoid": ["Durability", "HVLI"],
        "weekly_quality_sessions": 4,
        "allows_durability": False,
        "progression_style": "intensity_increase",  # More intervals rather than more volume
        "load_metric": "MAP / VO2max / W'",
        "best_for": "<6 h/wk, short events",
        "macro_phases": ["short_blocks"],  # 2-4 weeks intense + recovery
        "meso_pattern": "block_recovery",
    },

    # =========================================================================
    # 5. BLOCK PERIODIZATION
    # =========================================================================
    "BLOCK": {
        "name": "Block Periodization",
        "description": "Target one capacity intensely per block, then shift focus. Rapid limiter fixes.",
        "philosophy": "Focused overload → consolidation → next block (stair-step)",
        "primary_workouts": ["block_specific"],  # Varies by block type
        "secondary_workouts": ["maintenance"],
        "avoid": [],
        "weekly_quality_sessions": 4,
        "allows_durability": True,
        "progression_style": "block_staircase",  # Overload → consolidate → next
        "load_metric": "Block-specific KPI",
        "best_for": "Advanced athletes with coaching/monitoring",
        "macro_phases": ["accumulation", "transmutation", "realization"],
        "meso_pattern": "2-6_week_blocks",
        "block_types": ["VO2max_block", "Threshold_block", "Sprint_block", "Volume_block"],
    },

    # =========================================================================
    # 6. REVERSE PERIODIZATION
    # =========================================================================
    "REVERSE": {
        "name": "Reverse Periodization",
        "description": "Emphasize intensity early, then shift to volume/endurance later. Winter-friendly.",
        "philosophy": "Intensity early → volume later",
        "primary_workouts": ["VO2max", "Anaerobic_Capacity"],  # Early season
        "secondary_workouts": ["Endurance", "Durability"],  # Later season
        "avoid": [],
        "weekly_quality_sessions": 3,
        "allows_durability": True,
        "progression_style": "intensity_to_volume",  # Opposite of traditional
        "load_metric": "Early MAP/FTP, later decoupling",
        "best_for": "Athletes constrained in winter or short lead-in",
        "macro_phases": ["intensity_block", "volume_block", "specificity", "taper"],
        "meso_pattern": "phase_shift",
    },

    # =========================================================================
    # 7. AUTOREGULATED (HRV-BASED)
    # =========================================================================
    "HRV_AUTO": {
        "name": "Autoregulated (HRV-Based)",
        "description": "Use daily readiness (HRV/RHR/RPE) to adjust intensity/volume. Highly individualized.",
        "philosophy": "More load when green, less when red",
        "primary_workouts": ["readiness_dependent"],  # Any zone based on HRV
        "secondary_workouts": ["recovery"],
        "avoid": [],
        "weekly_quality_sessions": "variable",
        "allows_durability": True,
        "progression_style": "readiness_guided",
        "load_metric": "HRV trend + RPE + performance",
        "best_for": "Stress-variable athletes, masters, job/family constraints",
        "macro_phases": ["flexible"],
        "meso_pattern": "adaptive",
        "readiness_rules": {
            "green": ["VO2max", "Anaerobic_Capacity", "Sprint_Neuromuscular"],
            "amber": ["G_Spot", "TT_Threshold", "Endurance"],
            "red": ["Recovery", "Rest"],
        },
    },

    # =========================================================================
    # 8. MAF / LOW-HR (LT1)
    # =========================================================================
    "MAF_LT1": {
        "name": "MAF / Low-HR (LT1)",
        "description": "Build aerobic engine by staying under LT1. Single zone for most sessions.",
        "philosophy": "Long base of LT1 rides; minimal higher zones until base built",
        "primary_workouts": ["LT1_Capped", "Endurance"],
        "secondary_workouts": [],  # Minimal intensity
        "avoid": ["VO2max", "Anaerobic_Capacity", "Sprint_Neuromuscular"],
        "weekly_quality_sessions": 0,  # No quality sessions in pure MAF
        "allows_durability": True,
        "progression_style": "duration_increase",  # Duration ↑ while HR cap constant
        "load_metric": "Decoupling + pace at HR cap",
        "best_for": "Long events, rebuild phases",
        "macro_phases": ["long_base", "intensity_intro"],
        "meso_pattern": "4-6_week_duration_blocks",
        "hr_cap": "LT1",  # Or MAF formula
    },

    # =========================================================================
    # 9. CRITICAL POWER / W'
    # =========================================================================
    "CRITICAL_POWER": {
        "name": "Critical Power / W'",
        "description": "Structure training around CP and anaerobic work capacity (W'). High precision for surge events.",
        "philosophy": "Work above CP uses W', ≤CP targets endurance",
        "primary_workouts": ["Above_CP", "W_Prime"],
        "secondary_workouts": ["Below_CP_Endurance"],
        "avoid": [],
        "weekly_quality_sessions": 2,
        "allows_durability": False,
        "progression_style": "cp_w_prime_balance",  # >CP work ↑, W' recharge ↑, then raise CP
        "load_metric": "W' balance + CP trend",
        "best_for": "Events with repeated surges (crit, CX, some road)",
        "macro_phases": ["w_prime_development", "cp_raise", "specificity"],
        "meso_pattern": "test_adjust",
    },

    # =========================================================================
    # 10. INSCYD / METABOLIC PROFILING
    # =========================================================================
    "INSCYD": {
        "name": "INSCYD / Metabolic Profiling",
        "description": "Sculpt VO2max/VLamax profile to match event demands. High specificity.",
        "philosophy": "Shifts in VO2max and/or reduction in VLamax to 'fit' event",
        "primary_workouts": ["VO2max_Targeted", "VLamax_Reduction"],
        "secondary_workouts": ["Endurance", "FatMax"],
        "avoid": [],
        "weekly_quality_sessions": 2,
        "allows_durability": True,
        "progression_style": "metabolic_marker",  # VO2max ↑ or VLamax ↓
        "load_metric": "VO2max, VLamax, glycolytic rate, fatmax",
        "best_for": "Athletes needing fine metabolic tuning (triathlon, elite road)",
        "macro_phases": ["vo2max_phase", "vlamax_phase", "integration"],
        "meso_pattern": "marker_driven",
    },

    # =========================================================================
    # 11. DOUBLE-THRESHOLD (NORWEGIAN MODEL)
    # =========================================================================
    "NORWEGIAN": {
        "name": "Norwegian Double-Threshold",
        "description": "Two threshold sessions per day aimed at raising LT1/LT2 power while controlling lactate.",
        "philosophy": "Lactate-capped threshold dominates; high volume threshold blocks",
        "primary_workouts": ["Norwegian_Double", "TT_Threshold"],
        "secondary_workouts": ["Endurance"],
        "avoid": ["Sprint_Neuromuscular"],  # Minimal sprint work
        "weekly_quality_sessions": 4,  # 2 sessions/day on threshold days
        "allows_durability": True,
        "progression_style": "lactate_threshold_drift",  # Threshold power ↑ incrementally
        "load_metric": "Lactate test + threshold power trend",
        "best_for": "Elite athletes with full support team",
        "macro_phases": ["high_volume_threshold", "taper"],
        "meso_pattern": "daily_doubles",
        "lactate_cap": 4.0,  # mmol/L cap during sessions
    },

    # =========================================================================
    # 12. HVLI / LSD-CENTRIC
    # =========================================================================
    "HVLI": {
        "name": "HVLI / LSD-Centric",
        "description": "Very large volume of low intensity (Z1-Z2) to build durability and fat-oxidation. 3-5+ hour rides.",
        "philosophy": "Extreme durability, fuel efficiency, resilience through volume",
        "primary_workouts": ["HVLI_Extended", "Endurance"],
        "secondary_workouts": [],  # Minimal intensity
        "avoid": ["VO2max", "Anaerobic_Capacity", "Sprint_Neuromuscular"],
        "weekly_quality_sessions": 0,
        "allows_durability": True,
        "progression_style": "volume_accumulation",  # Volume ↑ over weeks
        "load_metric": "Weekly volume + decoupling",
        "best_for": "Athletes with ≥15 h/wk, multiday/endurance events",
        "macro_phases": ["very_long_base", "minimal_intensity", "taper"],
        "meso_pattern": "volume_blocks",
    },

    # =========================================================================
    # 13. GOAT (Gravel Optimized Adaptive Training)
    # =========================================================================
    "GOAT": {
        "name": "GOAT (Gravel Optimized Adaptive)",
        "description": "Integrates pyramidal base, polarized weeks, limiter-blocks, G-Spot when needed, autoregulation & signal-triggered testing.",
        "philosophy": "Block + polarized progression + volume/intensity modulation",
        "primary_workouts": ["block_rotation"],  # Rotates based on phase/signals
        "secondary_workouts": ["all"],
        "avoid": [],
        "weekly_quality_sessions": 2,
        "allows_durability": True,
        "progression_style": "adaptive_composite",  # Multi-signal driven
        "load_metric": "CTL + HRV + HR drift + power durability + block KPIs",
        "best_for": "Most athletes who can monitor & adjust",
        "macro_phases": ["pyramidal_base", "polarized_build", "limiter_blocks", "race_specific"],
        "meso_pattern": "signal_triggered",
        "block_triggers": {
            "vo2max_plateau": "VO2max_block",
            "threshold_limiter": "Threshold_block",
            "durability_weak": "Durability_block",
            "sprint_limiter": "Sprint_block",
        },
    },

    # =========================================================================
    # 14. TIME-CRUNCHED (Alias for backwards compatibility)
    # =========================================================================
    "TIME_CRUNCHED": {
        "name": "Time-Crunched",
        "description": "Alias for HIT - maximum adaptation from minimal time.",
        "philosophy": "Same as HIT",
        "primary_workouts": ["VO2max", "Anaerobic_Capacity", "Sprint_Neuromuscular"],
        "secondary_workouts": ["G_Spot"],
        "avoid": ["Durability", "HVLI"],
        "weekly_quality_sessions": 4,
        "allows_durability": False,
        "progression_style": "intensity_increase",
        "load_metric": "MAP / VO2max / W'",
        "best_for": "<6 h/wk",
        "macro_phases": ["short_blocks"],
        "meso_pattern": "block_recovery",
    },
}

# =============================================================================
# PROGRESSION STYLES - How intensity/volume progress through the plan
# =============================================================================

PROGRESSION_STYLES = {
    "volume_first": {
        "description": "Traditional: Volume increases, then intensity sharpens",
        "phase_1": {"volume": "high", "intensity": "low"},
        "phase_2": {"volume": "moderate", "intensity": "moderate"},
        "phase_3": {"volume": "low", "intensity": "high"},
        "phase_4": {"volume": "very_low", "intensity": "moderate"},  # Taper
    },
    "intensity_first": {
        "description": "Reverse: Intensity early, volume later",
        "phase_1": {"volume": "low", "intensity": "high"},
        "phase_2": {"volume": "moderate", "intensity": "moderate"},
        "phase_3": {"volume": "high", "intensity": "low"},
        "phase_4": {"volume": "moderate", "intensity": "moderate"},  # Taper
    },
    "intensity_stable": {
        "description": "Polarized: Maintain 80/20 ratio throughout",
        "phase_1": {"volume": "moderate", "intensity": "20%_high"},
        "phase_2": {"volume": "high", "intensity": "20%_high"},
        "phase_3": {"volume": "high", "intensity": "20%_high"},
        "phase_4": {"volume": "low", "intensity": "20%_high"},  # Taper
    },
    "density_increase": {
        "description": "G-Spot: Increase time-in-zone, then sessions per week",
        "phase_1": {"tiz_minutes": 20, "sessions": 2},
        "phase_2": {"tiz_minutes": 30, "sessions": 2},
        "phase_3": {"tiz_minutes": 40, "sessions": 3},
        "phase_4": {"tiz_minutes": 20, "sessions": 2},  # Taper
    },
    "block_staircase": {
        "description": "Block: Focused overload → consolidation → next block",
        "pattern": ["overload", "overload", "consolidation", "transition"],
    },
    "readiness_guided": {
        "description": "HRV: Load based on daily readiness signals",
        "green_day": "high_intensity",
        "amber_day": "moderate_intensity",
        "red_day": "recovery_or_rest",
    },
    "duration_increase": {
        "description": "MAF: Duration increases while intensity stays capped",
        "week_1_4": {"duration_multiplier": 1.0},
        "week_5_8": {"duration_multiplier": 1.15},
        "week_9_12": {"duration_multiplier": 1.30},
    },
    "volume_accumulation": {
        "description": "HVLI: Massive volume accumulation over weeks",
        "weekly_hours_target": [12, 14, 16, 12, 18, 20, 15, 22, 24, 18, 12, 8],
    },
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
) -> Optional[Dict[str, Any]]:
    """
    Select an archetype based on workout type and methodology.

    This function maps workout types to archetype categories, then applies
    methodology-specific overrides to select the most appropriate archetype.

    Args:
        workout_type: The type of workout (e.g., 'vo2max', 'threshold', 'sprint',
            'g_spot', 'recovery'). Case-insensitive.
        methodology: Training methodology from TRAINING_METHODOLOGIES
            (e.g., 'POLARIZED', 'PYRAMIDAL', 'G_SPOT', 'HIT'). Defaults to 'POLARIZED'.
        variation: Which variation of the archetype to use (0-indexed).
            Defaults to 0 (first/primary archetype in the category).

    Returns:
        The selected archetype dictionary containing 'name', 'levels', and
        workout structure data, or None if:
        - The workout_type is not recognized
        - The methodology explicitly avoids this workout category
        - The category has no archetypes

    Raises:
        No exceptions are raised; None is returned for all failure cases.
        Use logging to diagnose selection issues.

    Examples:
        >>> archetype = select_archetype_for_workout('vo2max', 'POLARIZED')
        >>> archetype['name']
        'VO2max 5x3 Classic'

        >>> # Polarized avoids G-Spot (middle zone)
        >>> select_archetype_for_workout('g_spot', 'POLARIZED')
        None
    """
    # Map workout types to categories
    type_to_category = {
        # Original categories
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
        "sector": "Race_Simulation",
        # G-Spot (87-92% FTP) - NOT Sweet Spot
        "g_spot": "G_Spot",
        "gspot": "G_Spot",
        "g-spot": "G_Spot",
        "tempo": "G_Spot",  # Map tempo to G-Spot instead of SS
        # LT1/MAF
        "lt1": "LT1_MAF",
        "maf": "LT1_MAF",
        "lt1_capped": "LT1_MAF",
        "aerobic_base": "LT1_MAF",
        # Critical Power
        "cp": "Critical_Power",
        "critical_power": "Critical_Power",
        "w_prime": "Critical_Power",
        "above_cp": "Critical_Power",
        # Norwegian Double-Threshold
        "norwegian": "Norwegian_Double",
        "norwegian_am": "Norwegian_Double",
        "norwegian_pm": "Norwegian_Double",
        "double_threshold": "Norwegian_Double",
        "seiler": "Norwegian_Double",
        # HVLI/LSD
        "hvli": "HVLI_Extended",
        "lsd": "HVLI_Extended",
        "long_slow": "HVLI_Extended",
        "extended_z2": "HVLI_Extended",
        # Testing
        "test": "Testing",
        "ftp_test": "Testing",
        "ramp_test": "Testing",
        "cp_test": "Testing",
        "testing": "Testing",
        # Recovery
        "recovery": "Recovery",
        "rest": "Recovery",
        "active_recovery": "Recovery",
        "easy": "Recovery",
        # INSCYD/Metabolic
        "inscyd": "INSCYD",
        "vlamax": "INSCYD",
        "fatmax": "INSCYD",
        "metabolic": "INSCYD",
    }

    category = type_to_category.get(workout_type.lower())
    if not category:
        logger.warning(
            f"Unknown workout type '{workout_type}'. "
            f"Valid types: {list(type_to_category.keys())[:10]}..."
        )
        return None

    # ==========================================================================
    # METHODOLOGY-AWARE ARCHETYPE SELECTION
    # ==========================================================================
    # Different methodologies should prefer different archetypes for the same
    # workout type. This is where the magic happens.

    method_config = TRAINING_METHODOLOGIES.get(methodology)
    if not method_config:
        logger.warning(
            f"Unknown methodology '{methodology}'. "
            f"Falling back to POLARIZED. Valid: {list(TRAINING_METHODOLOGIES.keys())}"
        )
        method_config = TRAINING_METHODOLOGIES["POLARIZED"]

    # Check if this category is avoided by the methodology
    avoided_categories = method_config.get("avoid", [])
    if category in avoided_categories:
        logger.debug(
            f"Methodology '{methodology}' avoids category '{category}'. "
            f"Avoided categories: {avoided_categories}"
        )
        return None

    # Methodology-specific archetype selection overrides
    methodology_overrides = {
        "POLARIZED": {
            # Polarized prefers hard VO2max, avoids middle zone
            "default_variation": 0,  # Classic formats
        },
        "PYRAMIDAL": {
            # Pyramidal prefers threshold work
            "TT_Threshold": 0,  # Single sustained threshold
            "G_Spot": 0,  # G-Spot intervals
        },
        "G_SPOT": {
            # G-Spot methodology - prioritize G-Spot archetypes
            "G_Spot": 0,  # Standard G-Spot intervals
            "TT_Threshold": 2,  # Descending threshold (more variety)
        },
        "NORWEGIAN": {
            # Norwegian - prioritize 4x8 format
            "Norwegian_Double": 0,  # Classic 4x8
            "TT_Threshold": 0,  # Sustained threshold
        },
        "HIT": {
            # HIT - prioritize shorter, more intense
            "VO2max": 0,  # Classic 5x3
            "Anaerobic_Capacity": 0,  # 2min killers
        },
        "MAF_LT1": {
            # MAF - prioritize LT1 capped work
            "LT1_MAF": 0,  # LT1 capped endurance
            "Endurance": 1,  # Terrain simulation Z2
        },
        "CRITICAL_POWER": {
            # CP model - prioritize above-CP work
            "Critical_Power": 0,  # Above CP repeats
        },
        "HVLI": {
            # HVLI - prioritize extended Z2
            "HVLI_Extended": 0,  # Extended Z2
            "Endurance": 1,  # Terrain simulation
        },
        "INSCYD": {
            # INSCYD - prioritize metabolic work
            "INSCYD": 0,  # VLamax reduction
        },
    }

    # Get methodology-specific variation if available
    method_overrides = methodology_overrides.get(methodology, {})
    if category in method_overrides:
        variation = method_overrides[category]

    return get_archetype_by_category_and_index(category, variation)


def is_recovery_week(week_num: int, recovery_pattern: str = "3:1") -> bool:
    """
    Determine if a given week is a recovery/deload week.

    Args:
        week_num: Current week number (1-indexed)
        recovery_pattern: Pattern string like "3:1" (3 load weeks, 1 recovery)
            or "4:1" (4 load weeks, 1 recovery)

    Returns:
        True if this week should be a recovery week

    Examples:
        >>> is_recovery_week(4, "3:1")  # Week 4 of 3:1 pattern
        True
        >>> is_recovery_week(3, "3:1")  # Week 3 of 3:1 pattern
        False
        >>> is_recovery_week(5, "4:1")  # Week 5 of 4:1 pattern
        True
    """
    try:
        load_weeks, recovery_weeks = map(int, recovery_pattern.split(":"))
        cycle_length = load_weeks + recovery_weeks
        position_in_cycle = (week_num - 1) % cycle_length
        return position_in_cycle >= load_weeks
    except (ValueError, AttributeError):
        # Default to 3:1 if pattern is invalid
        return (week_num - 1) % 4 == 3


def calculate_level_from_week(
    week_num: int,
    total_weeks: int,
    taper_weeks: int = MethodologyDefaults.DEFAULT_TAPER_WEEKS,
    methodology: str = MethodologyDefaults.DEFAULT_METHODOLOGY,
    recovery_pattern: str = "3:1"
) -> int:
    """
    Calculate the progression level (1-6) based on week position and methodology.

    This function uses the progression style from the methodology configuration
    to determine the appropriate workout difficulty level. Different methodologies
    have different progression patterns:

    - volume_first (PYRAMIDAL): Linear progression 1→6
    - intensity_first (REVERSE): 6→3 (high to moderate)
    - intensity_stable (POLARIZED): Stays at 4-5
    - density_increase (G_SPOT): Aggressive 2→6
    - block_staircase (BLOCK): 2-week overload, 1-week recovery pattern

    Also handles:
    - Recovery weeks (3:1 or 4:1 patterns) - reduces level by 2
    - Taper weeks at end of plan - returns moderate level

    Args:
        week_num: Current week number (1-indexed).
        total_weeks: Total weeks in the training plan.
        taper_weeks: Number of weeks reserved for tapering at plan end.
            Defaults to 2. During taper, returns a moderate level (typically 4).
        methodology: Training methodology from TRAINING_METHODOLOGIES.
            Defaults to 'POLARIZED'.
        recovery_pattern: Recovery week pattern (e.g., "3:1" = 3 load, 1 recovery).
            Set to "" or None to disable mid-plan recovery weeks.

    Returns:
        Integer level from 1 to 6:
        - 1: Introductory / recovery week
        - 2: Base building / recovery week
        - 3: Moderate development
        - 4: Standard training load
        - 5: High training load
        - 6: Peak / race preparation

    Examples:
        >>> # Early in a polarized plan
        >>> calculate_level_from_week(2, 12, 2, 'POLARIZED')
        4

        >>> # Recovery week (week 4 in 3:1 pattern)
        >>> calculate_level_from_week(4, 12, 2, 'PYRAMIDAL', '3:1')
        2

        >>> # Taper week always returns moderate level
        >>> calculate_level_from_week(11, 12, 2, 'POLARIZED')
        4
    """
    # Get progression style from methodology
    method_config = TRAINING_METHODOLOGIES.get(methodology, TRAINING_METHODOLOGIES["POLARIZED"])
    progression_style = method_config.get("progression_style", "volume_first")
    meso_pattern = method_config.get("meso_pattern", "3:1")

    # Exclude taper weeks from progression
    build_weeks = total_weeks - taper_weeks

    # Check for taper weeks first
    if week_num > build_weeks:
        # In taper - use appropriate level based on progression style
        if progression_style == "intensity_first":
            return Levels.DEFAULT_LEVEL  # Reverse - volume phase at end, use moderate level
        else:
            return Levels.TAPER_LEVEL  # Standard - maintain fitness without max stress

    # Check for recovery week (mid-plan deload)
    # Use methodology's meso_pattern if no explicit recovery_pattern provided
    effective_pattern = recovery_pattern if recovery_pattern else meso_pattern
    is_recovery = False
    if effective_pattern and effective_pattern not in ("maintain_ratio", "adaptive", "flexible"):
        is_recovery = is_recovery_week(week_num, effective_pattern)

    # Calculate base progress through build phase
    progress = week_num / build_weeks

    # Calculate base level from progression style
    if progression_style == "intensity_first":
        # Reverse periodization: Start hard, end easier
        if progress < 0.25:
            base_level = Levels.MAX_LEVEL  # Peak intensity early
        elif progress < 0.50:
            base_level = 5
        elif progress < 0.75:
            base_level = 4
        else:
            base_level = 3  # Back off before taper

    elif progression_style == "intensity_stable":
        # Polarized: Maintain consistent intensity level
        if progress < 0.33:
            base_level = 4
        else:
            base_level = 5

    elif progression_style == "density_increase":
        # G-Spot: More aggressive progression for threshold work
        if progress < 0.20:
            base_level = 2
        elif progress < 0.40:
            base_level = 3
        elif progress < 0.60:
            base_level = 4
        elif progress < 0.80:
            base_level = 5
        else:
            base_level = Levels.MAX_LEVEL

    elif progression_style == "block_staircase":
        # Block: 2-week overload, 1-week consolidation pattern
        block_position = week_num % 3  # 0, 1, 2 pattern
        block_base = min(Levels.MAX_LEVEL, 2 + (week_num // 3))
        if block_position < 2:  # Overload weeks
            base_level = min(Levels.MAX_LEVEL, block_base + 1)
        else:  # Consolidation week
            base_level = max(Levels.MIN_LEVEL, block_base - 1)

    elif progression_style == "duration_increase":
        # MAF/LT1: Level represents duration, not intensity
        if progress < 0.25:
            base_level = 2
        elif progress < 0.50:
            base_level = 3
        elif progress < 0.75:
            base_level = 4
        else:
            base_level = 5

    elif progression_style == "volume_accumulation":
        # HVLI: Volume builds progressively
        if progress < 0.20:
            base_level = Levels.MIN_LEVEL
        elif progress < 0.40:
            base_level = 2
        elif progress < 0.60:
            base_level = 3
        elif progress < 0.80:
            base_level = 4
        else:
            base_level = 5

    else:
        # Default: Traditional linear progression (volume_first)
        if progress < Levels.LEVEL_1_THRESHOLD:
            base_level = Levels.MIN_LEVEL
        elif progress < Levels.LEVEL_2_THRESHOLD:
            base_level = 2
        elif progress < Levels.LEVEL_3_THRESHOLD:
            base_level = 3
        elif progress < Levels.LEVEL_4_THRESHOLD:
            base_level = 4
        elif progress < Levels.LEVEL_5_THRESHOLD:
            base_level = 5
        else:
            base_level = Levels.MAX_LEVEL

    # Apply recovery week adjustment (reduce by 2 levels, minimum 1)
    if is_recovery:
        return max(Levels.MIN_LEVEL, base_level - 2)

    return base_level


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

def generate_text_event(offset: int, message: str) -> str:
    """
    Generate a text event for coaching cues during workout.

    Args:
        offset: Time offset in seconds from start of parent block
        message: Coaching message to display

    Returns:
        XML textevent element
    """
    escaped_message = html.escape(message, quote=True)
    return f'      <textevent timeoffset="{offset}" message="{escaped_message}"/>\n'


def generate_warmup_block(
    duration: int = Durations.WARMUP_EXTENDED,
    include_text: bool = True
) -> str:
    """
    Generate warmup block with optional coaching text.

    Args:
        duration: Warmup duration in seconds (default: 15 min)
        include_text: Whether to include coaching text events

    Returns:
        XML warmup block with optional text events
    """
    block = (
        f'    <Warmup Duration="{duration}" '
        f'PowerLow="{ZWODefaults.WARMUP_POWER_LOW:.2f}" '
        f'PowerHigh="{ZWODefaults.WARMUP_POWER_HIGH:.2f}"'
    )

    if include_text:
        block += '>\n'
        block += generate_text_event(0, "Begin warmup - easy spinning")
        block += generate_text_event(duration // 3, "Gradually increase effort")
        block += generate_text_event(duration - 60, "Warmup complete in 1 minute")
        block += '    </Warmup>\n'
    else:
        block += '/>\n'

    return block


def generate_cooldown_block(
    duration: int = Durations.COOLDOWN_STANDARD,
    include_text: bool = True
) -> str:
    """
    Generate cooldown block with optional coaching text.

    Args:
        duration: Cooldown duration in seconds (default: 10 min)
        include_text: Whether to include coaching text events

    Returns:
        XML cooldown block with optional text events
    """
    block = (
        f'    <Cooldown Duration="{duration}" '
        f'PowerLow="{ZWODefaults.COOLDOWN_POWER_LOW:.2f}" '
        f'PowerHigh="{ZWODefaults.COOLDOWN_POWER_HIGH:.2f}"'
    )

    if include_text:
        block += '>\n'
        block += generate_text_event(0, "Cool down - great work!")
        block += generate_text_event(duration - 60, "Almost done - easy spin")
        block += '    </Cooldown>\n'
    else:
        block += '/>\n'

    return block


def generate_steady_state_block(
    duration: int,
    power: float,
    cadence: Optional[int] = None,
    text: Optional[str] = None
) -> str:
    """
    Generate a steady state block.

    Args:
        duration: Duration in seconds
        power: Power target as FTP fraction
        cadence: Optional cadence target in RPM
        text: Optional coaching text to display at start

    Returns:
        XML steady state block
    """
    cadence_attr = f' Cadence="{cadence}"' if cadence else ""

    if text:
        escaped_text = html.escape(text, quote=True)
        return (
            f'    <SteadyState Duration="{duration}" Power="{power:.2f}"{cadence_attr}>\n'
            f'      <textevent timeoffset="0" message="{escaped_text}"/>\n'
            f'    </SteadyState>\n'
        )
    else:
        return f'    <SteadyState Duration="{duration}" Power="{power:.2f}"{cadence_attr}/>\n'


def generate_intervals_block(
    repeats: int,
    on_duration: int,
    on_power: float,
    off_duration: int,
    off_power: float = ZWODefaults.RECOVERY_POWER,
    cadence: int = Cadence.STANDARD,
    include_text: bool = True
) -> str:
    """
    Generate an IntervalsT block with optional coaching text.

    Args:
        repeats: Number of interval repeats
        on_duration: Work interval duration in seconds
        on_power: Work interval power as FTP fraction
        off_duration: Recovery interval duration in seconds
        off_power: Recovery interval power as FTP fraction
        cadence: Cadence target during work intervals
        include_text: Whether to include coaching text

    Returns:
        XML intervals block with optional text events
    """
    block = (
        f'    <IntervalsT Repeat="{repeats}" '
        f'OnDuration="{on_duration}" OnPower="{on_power:.2f}" '
        f'Cadence="{cadence}" OffDuration="{off_duration}" '
        f'OffPower="{off_power:.2f}"'
    )

    if include_text:
        block += '>\n'
        block += generate_text_event(0, f"Interval 1 of {repeats} - GO!")
        block += generate_text_event(on_duration, "Recovery - breathe deep")
        block += '    </IntervalsT>\n'
    else:
        block += '/>\n'

    return block


def generate_ramp_block(
    duration: int,
    power_low: float,
    power_high: float,
    text: Optional[str] = None
) -> str:
    """
    Generate a ramp block.

    Args:
        duration: Ramp duration in seconds
        power_low: Starting power as FTP fraction
        power_high: Ending power as FTP fraction
        text: Optional coaching text

    Returns:
        XML ramp block
    """
    if text:
        escaped_text = html.escape(text, quote=True)
        return (
            f'    <Ramp Duration="{duration}" '
            f'PowerLow="{power_low:.2f}" PowerHigh="{power_high:.2f}">\n'
            f'      <textevent timeoffset="0" message="{escaped_text}"/>\n'
            f'    </Ramp>\n'
        )
    else:
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
    # G-SPOT CRISS-CROSS
    # =====================================================================
    elif "criss_cross" in level_data:
        total_duration = level_data.get("total_duration", 1200)
        high_power = level_data.get("high_power", 0.92)
        low_power = level_data.get("low_power", 0.85)
        interval_duration = level_data.get("interval_duration", 120)
        sets = level_data.get("sets", 1)
        set_recovery = level_data.get("set_recovery", 300)

        blocks.append(generate_warmup_block())

        for set_num in range(sets):
            num_intervals = total_duration // (interval_duration * 2)
            for i in range(int(num_intervals)):
                blocks.append(generate_steady_state_block(interval_duration, high_power))
                blocks.append(generate_steady_state_block(interval_duration, low_power))
            if sets > 1 and set_num < sets - 1:
                blocks.append(generate_steady_state_block(set_recovery, 0.55))

    # =====================================================================
    # LT1/MAF CAPPED ENDURANCE
    # =====================================================================
    elif "lt1_capped" in level_data or "maf_test" in level_data:
        duration = level_data.get("duration", 3600)
        power = level_data.get("power", 0.70)
        test_duration = level_data.get("test_duration", 0)
        warmup_dur = level_data.get("warmup_duration", 600)

        if test_duration > 0:  # MAF test protocol
            blocks.append(generate_steady_state_block(warmup_dur, 0.60))
            blocks.append(generate_steady_state_block(test_duration, power))
            blocks.append(generate_cooldown_block(300))
            return "".join(blocks)
        else:
            blocks.append(generate_warmup_block(600))
            blocks.append(generate_steady_state_block(duration, power))

    # =====================================================================
    # HVLI EXTENDED Z2
    # =====================================================================
    elif "hvli" in level_data:
        duration = level_data.get("duration", 10800)
        power = level_data.get("power", 0.68)

        blocks.append(generate_warmup_block(900))
        blocks.append(generate_steady_state_block(duration - 1500, power))  # Duration minus warmup/cooldown

    # =====================================================================
    # HVLI TERRAIN SIMULATION
    # =====================================================================
    elif "hvli_terrain" in level_data:
        duration = level_data.get("duration", 10800)
        high_power = level_data.get("high_power", 0.72)
        low_power = level_data.get("low_power", 0.65)
        interval_duration = level_data.get("interval_duration", 600)

        blocks.append(generate_warmup_block(900))

        # Alternating terrain blocks
        remaining = duration - 1500
        while remaining > 0:
            high_dur = min(interval_duration, remaining)
            blocks.append(generate_steady_state_block(high_dur, high_power))
            remaining -= high_dur
            if remaining > 0:
                low_dur = min(interval_duration, remaining)
                blocks.append(generate_steady_state_block(low_dur, low_power))
                remaining -= low_dur

    # =====================================================================
    # NORWEGIAN DOUBLE-THRESHOLD
    # =====================================================================
    elif "norwegian" in level_data:
        intervals_data = level_data.get("intervals", (4, 480))
        if isinstance(intervals_data, tuple):
            repeats, duration = intervals_data
        else:
            repeats = 4
            duration = 480

        on_power = level_data.get("on_power", 0.90)
        off_duration = level_data.get("off_duration", 120)
        off_power = level_data.get("off_power", 0.55)

        blocks.append(generate_warmup_block(1200))  # Longer warmup for Norwegian

        for rep in range(repeats):
            blocks.append(generate_steady_state_block(duration, on_power, cadence=88))
            if rep < repeats - 1:
                blocks.append(generate_steady_state_block(off_duration, off_power))

    # =====================================================================
    # ABOVE CP / CRITICAL POWER REPEATS
    # =====================================================================
    elif "above_cp" in level_data:
        intervals_data = level_data.get("intervals", (4, 120))
        if isinstance(intervals_data, tuple):
            repeats, duration = intervals_data
        else:
            repeats = 4
            duration = 120

        on_power = level_data.get("on_power", 1.10)
        off_duration = level_data.get("off_duration", 240)
        off_power = level_data.get("off_power", 0.55)

        blocks.append(generate_warmup_block())

        for rep in range(repeats):
            blocks.append(generate_steady_state_block(duration, on_power, cadence=95))
            if rep < repeats - 1:
                blocks.append(generate_steady_state_block(off_duration, off_power))

    # =====================================================================
    # W-PRIME DEPLETION
    # =====================================================================
    elif "w_prime" in level_data:
        sets = level_data.get("sets", 3)
        surge_duration = level_data.get("surge_duration", 180)
        surge_power = level_data.get("surge_power", 1.15)
        hold_duration = level_data.get("hold_duration", 120)
        hold_power = level_data.get("hold_power", 1.05)
        set_recovery = level_data.get("set_recovery", 300)

        blocks.append(generate_warmup_block())

        for set_num in range(sets):
            blocks.append(generate_steady_state_block(surge_duration, surge_power))
            blocks.append(generate_steady_state_block(hold_duration, hold_power))
            if set_num < sets - 1:
                blocks.append(generate_steady_state_block(set_recovery, 0.55))

    # =====================================================================
    # RECOVERY WORKOUTS
    # =====================================================================
    elif "recovery" in level_data:
        duration = level_data.get("duration", 2700)
        power = level_data.get("power", 0.52)

        blocks.append(generate_warmup_block(300))  # Short warmup
        blocks.append(generate_steady_state_block(duration - 600, power, cadence=90))
        blocks.append(generate_cooldown_block(300))
        return "".join(blocks)

    # =====================================================================
    # REST DAY (No blocks - just placeholder)
    # =====================================================================
    elif "rest_day" in level_data:
        # Rest day generates minimal file - just a marker
        blocks.append('    <FreeRide Duration="0" FlatRoad="1"/>\n')
        return "".join(blocks)

    # =====================================================================
    # TESTING PROTOCOLS
    # =====================================================================
    elif "testing" in level_data:
        test_type = level_data.get("test_type", "ramp")
        warmup_duration = level_data.get("warmup_duration", 600)
        warmup_power = level_data.get("warmup_power", 0.50)

        if test_type == "ramp":
            # Ramp test: warmup then progressive ramp to failure
            blocks.append(generate_steady_state_block(warmup_duration, warmup_power))
            # Ramp from ~50% to max (simulated as 18 steps of 1min each)
            for i in range(18):
                power = 0.50 + (i * 0.03)  # Increment ~3% each minute
                blocks.append(generate_steady_state_block(60, min(power, 1.50)))
            blocks.append(generate_cooldown_block(300))
            return "".join(blocks)

        elif test_type == "20min_ftp":
            # 20min FTP test with blowout warmup
            blowout_intervals = level_data.get("blowout_intervals", (3, 60))
            blowout_power = level_data.get("blowout_power", 1.20)
            test_duration = level_data.get("test_duration", 1200)

            blocks.append(generate_warmup_block(warmup_duration))
            # Blowout efforts
            for i in range(blowout_intervals[0]):
                blocks.append(generate_steady_state_block(blowout_intervals[1], blowout_power))
                blocks.append(generate_steady_state_block(120, 0.50))
            # 5min recovery before test
            blocks.append(generate_steady_state_block(300, 0.55))
            # 20min all-out (represented as FreeRide for max effort)
            blocks.append(f'    <FreeRide Duration="{test_duration}" FlatRoad="1"/>\n')
            blocks.append(generate_cooldown_block(600))
            return "".join(blocks)

        elif test_type in ("cp_3min", "cp_12min"):
            # CP test: warmup then all-out effort
            test_duration = level_data.get("test_duration", 180)
            blocks.append(generate_warmup_block(warmup_duration))
            blocks.append(generate_steady_state_block(300, 0.55))  # Pre-test settle
            blocks.append(f'    <FreeRide Duration="{test_duration}" FlatRoad="1"/>\n')
            blocks.append(generate_cooldown_block(600))
            return "".join(blocks)

    # =====================================================================
    # INSCYD / METABOLIC WORKOUTS
    # =====================================================================
    elif "inscyd" in level_data or "vlamax_reduction" in level_data or "fatmax" in level_data:
        duration = level_data.get("duration", 5400)
        power = level_data.get("power", 0.70)
        sprint_intervals = level_data.get("sprint_intervals", (0, 0))
        sprint_power = level_data.get("sprint_power", 2.0)

        blocks.append(generate_warmup_block(900))

        if sprint_intervals[0] > 0:
            # VLamax reduction: Long Z2 with distributed sprints
            main_duration = duration - 1500
            sprint_spacing = main_duration // (sprint_intervals[0] + 1)

            for i in range(sprint_intervals[0]):
                blocks.append(generate_steady_state_block(sprint_spacing, power))
                blocks.append(generate_steady_state_block(sprint_intervals[1], sprint_power))
            # Final Z2 segment
            blocks.append(generate_steady_state_block(sprint_spacing, power))
        else:
            # FatMax: Pure steady-state Z2
            blocks.append(generate_steady_state_block(duration - 1500, power))

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
    workout_name: Optional[str] = None
) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """
    Generate a complete Nate workout.

    This function selects an appropriate archetype based on workout type and
    methodology, then generates the workout name, description, and ZWO blocks.

    Args:
        workout_type: Type of workout. Valid types include:
            - 'vo2max', 'vo2': VO2max intervals
            - 'threshold', 'tt', 'ftp': Threshold/FTP work
            - 'sprint', 'neuromuscular': Sprint efforts
            - 'anaerobic': Anaerobic capacity
            - 'g_spot', 'tempo': G-Spot intervals (87-92% FTP)
            - 'recovery', 'easy': Recovery rides
            - 'test', 'ramp_test': Testing protocols
            - And many more (see select_archetype_for_workout)
        level: Progression level from 1 (easiest) to 6 (hardest).
            Defaults to 3 (moderate).
        methodology: Training methodology. Valid options:
            - 'POLARIZED': 80/20 hard/easy split
            - 'PYRAMIDAL': Traditional volume-first
            - 'G_SPOT': Threshold-focused
            - 'HIT': High-intensity focused
            - And more (see TRAINING_METHODOLOGIES)
        variation: Which archetype variation to use within the category (0-indexed).
            Defaults to 0 (primary archetype).
        workout_name: Optional custom name for the workout. If None, generates
            a name from the archetype name and level.

    Returns:
        Tuple of (name, description, blocks) where:
        - name: Workout name string
        - description: Full workout description with warmup, main set, cooldown
        - blocks: ZWO XML block content (not complete file)

        Returns (None, None, None) if:
        - workout_type is not recognized
        - methodology avoids this workout category
        - archetype has no data for the requested level

    Examples:
        >>> name, desc, blocks = generate_nate_workout('vo2max', 4, 'POLARIZED')
        >>> name
        'VO2max 5x3 Classic L4'

        >>> # G-Spot avoided by Polarized methodology
        >>> name, desc, blocks = generate_nate_workout('g_spot', 4, 'POLARIZED')
        >>> name is None
        True
    """
    # Validate level
    if not 1 <= level <= 6:
        logger.warning(f"Level {level} out of range [1-6], clamping to valid range")
        level = max(1, min(6, level))

    # Select archetype
    archetype = select_archetype_for_workout(workout_type, methodology, variation)

    if archetype is None:
        logger.info(
            f"No archetype found for workout_type='{workout_type}', "
            f"methodology='{methodology}', variation={variation}. "
            f"This may be intentional (e.g., Polarized avoids G-Spot)."
        )
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
    workout_name: Optional[str] = None
) -> Optional[str]:
    """
    Generate a complete ZWO file from a Nate archetype.

    This function generates a complete, valid ZWO XML file that can be
    imported directly into Zwift.

    Args:
        workout_type: Type of workout (see generate_nate_workout for valid types).
        level: Progression level from 1 (easiest) to 6 (hardest). Defaults to 3.
        methodology: Training methodology (see TRAINING_METHODOLOGIES).
            Defaults to 'POLARIZED'.
        variation: Which archetype variation to use (0-indexed). Defaults to 0.
        workout_name: Optional custom name for the workout.

    Returns:
        Complete ZWO XML content as a string, ready to save to a .zwo file.
        Returns None if workout generation fails (e.g., invalid workout type,
        methodology avoids the workout category).

    Examples:
        >>> zwo = generate_nate_zwo('vo2max', 4, 'POLARIZED')
        >>> zwo.startswith('<?xml')
        True

        >>> # Save to file
        >>> with open('workout.zwo', 'w') as f:
        ...     f.write(generate_nate_zwo('threshold', 3, 'PYRAMIDAL'))
    """
    name, description, blocks = generate_nate_workout(
        workout_type, level, methodology, variation, workout_name
    )

    if name is None or blocks is None:
        logger.debug(
            f"ZWO generation failed: workout_type='{workout_type}', "
            f"methodology='{methodology}'"
        )
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
