# Nate Workout Generator

A complete ZWO workout generator based on the Nate archetype system.

## Features

- **41 archetypes** across 15 categories
- **6 progression levels** per archetype (246 total variations)
- **14 training methodologies** (Polarized, Pyramidal, G-Spot, HIT, etc.)
- **8 progression styles** for periodization
- **Methodology-aware selection** (e.g., Polarized avoids G-Spot workouts)
- **Recovery week handling** (3:1 and 4:1 patterns)
- **Coaching text events** in generated workouts
- **Full XML validation** of output

## Quick Start

```python
from nate_workout_generator import generate_nate_zwo

# Generate a VO2max workout
zwo = generate_nate_zwo(
    workout_type='vo2max',
    level=4,
    methodology='POLARIZED'
)

# Save to file
with open('workout.zwo', 'w') as f:
    f.write(zwo)
```

## Workout Types

| Type | Category | Description |
|------|----------|-------------|
| `vo2max`, `vo2` | VO2max | High-intensity intervals above threshold |
| `threshold`, `tt`, `ftp` | TT_Threshold | Sustained threshold work |
| `sprint`, `neuromuscular` | Sprint | Short explosive efforts |
| `anaerobic` | Anaerobic_Capacity | 1-3 minute max efforts |
| `g_spot`, `tempo` | G_Spot | Sub-threshold intervals (87-92% FTP) |
| `durability`, `tired` | Durability | Quality work when fatigued |
| `endurance`, `openers` | Endurance | Easy rides and pre-race openers |
| `race_sim`, `breakaway` | Race_Simulation | Race-specific patterns |
| `lt1`, `maf` | LT1_MAF | Low-intensity aerobic work |
| `cp`, `critical_power` | Critical_Power | W' and CP development |
| `norwegian` | Norwegian_Double | 4x8 threshold sessions |
| `hvli`, `lsd` | HVLI_Extended | Long slow distance |
| `test`, `ramp_test` | Testing | FTP and ramp tests |
| `recovery`, `easy` | Recovery | Active recovery rides |
| `inscyd`, `vlamax` | INSCYD | Metabolic profiling workouts |

## Methodologies

| Methodology | Description | Progression Style |
|-------------|-------------|-------------------|
| `POLARIZED` | 80/20 hard/easy split | intensity_stable |
| `PYRAMIDAL` | Traditional volume-first | volume_first |
| `G_SPOT` | Threshold-focused | density_increase |
| `HIT` | High-intensity focused | intensity_increase |
| `BLOCK` | Block periodization | block_staircase |
| `REVERSE` | Intensity early, volume late | intensity_first |
| `NORWEGIAN` | Double-threshold sessions | lactate_threshold_drift |
| `MAF_LT1` | Low-HR aerobic building | duration_increase |
| `CRITICAL_POWER` | CP/W' model training | cp_w_prime_balance |
| `INSCYD` | Metabolic profiling | metabolic_marker |
| `HVLI` | High-volume low-intensity | volume_accumulation |
| `HRV_AUTO` | Readiness-based | readiness_guided |
| `GOAT` | Adaptive composite | adaptive_composite |
| `TIME_CRUNCHED` | Minimal time, max adaptation | intensity_increase |

## Progression Levels

| Level | Description | Use Case |
|-------|-------------|----------|
| 1 | Introductory | First week, recovery |
| 2 | Base building | Early season |
| 3 | Moderate development | Standard training |
| 4 | Standard load | Default, taper weeks |
| 5 | High load | Peak training |
| 6 | Race preparation | Final build weeks |

## API Reference

### `generate_nate_zwo()`

Generate a complete ZWO file.

```python
def generate_nate_zwo(
    workout_type: str,           # Required: workout type (see table above)
    level: int = 3,              # Progression level 1-6
    methodology: str = "POLARIZED",  # Training methodology
    variation: int = 0,          # Archetype variation within category
    workout_name: str = None     # Custom workout name
) -> Optional[str]:
    """Returns complete ZWO XML string, or None if generation fails."""
```

### `generate_nate_workout()`

Generate workout components separately.

```python
def generate_nate_workout(
    workout_type: str,
    level: int = 3,
    methodology: str = "POLARIZED",
    variation: int = 0,
    workout_name: str = None
) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    """Returns (name, description, blocks) tuple."""
```

### `calculate_level_from_week()`

Calculate appropriate level for a given week.

```python
def calculate_level_from_week(
    week_num: int,               # Current week (1-indexed)
    total_weeks: int,            # Total plan weeks
    taper_weeks: int = 2,        # Weeks of taper at end
    methodology: str = "POLARIZED",
    recovery_pattern: str = "3:1"  # Recovery week pattern
) -> int:
    """Returns level 1-6 based on progression and recovery patterns."""
```

### `is_recovery_week()`

Check if a week is a recovery/deload week.

```python
def is_recovery_week(
    week_num: int,               # Current week (1-indexed)
    recovery_pattern: str = "3:1"  # Pattern like "3:1" or "4:1"
) -> bool:
    """Returns True if week is a recovery week."""
```

## Constants

All magic numbers are defined in `constants.py`:

- `PowerZones`: FTP fractions for each zone
- `Durations`: Standard segment durations in seconds
- `Cadence`: Standard cadence values
- `Levels`: Level boundaries and thresholds
- `ValidationLimits`: Sanity check limits
- `ZWODefaults`: Default values for ZWO generation

## Testing

Run all tests:
```bash
cd races/tests
python -m unittest discover -v
```

Run specific test module:
```bash
python -m unittest test_nate_generator_integration -v
python -m unittest test_zwo_validation -v
python -m unittest test_edge_cases -v
```

## File Structure

```
races/
├── generation_modules/
│   ├── nate_workout_generator.py  # Main generator
│   ├── constants.py               # All constants
│   └── README.md                  # This file
├── nate_archetypes/
│   └── new_archetypes.py          # Archetype definitions
└── tests/
    ├── __init__.py
    ├── test_nate_generator_integration.py
    ├── test_zwo_validation.py
    └── test_edge_cases.py
```

## Notes

- **G-Spot replaces Sweet Spot** throughout this generator (87-92% FTP)
- **CP to FTP conversion**: CP ≈ 96% FTP, so 110% CP ≈ 106% FTP
- **Recovery weeks** reduce level by 2 (minimum level 1)
- **Taper weeks** always return level 4
