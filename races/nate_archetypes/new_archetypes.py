#!/usr/bin/env python3
"""
New archetype additions for the Gravel God training system.
Aligned with polarized (80/20) training philosophy.
No Sweet Spot - uses G-Spot (87-92% FTP) sparingly for durability work only.
"""

# =============================================================================
# VO2MAX ADDITIONS
# =============================================================================

VO2MAX_NEW = [
    {
        'name': '5x3 VO2 Classic',
        'levels': {
            '1': {
                'structure': '15min warmup Z2, 4x3min @ 108-112% FTP, 3min recovery between',
                'execution': 'Learning the format - shorter intervals, more repeats. Control the power',
                'cadence_prescription': '90-100rpm (high turnover)',
                'position_prescription': 'Seated, on the hoods',
                'timing_prescription': 'Fresh',
                'fueling': '60-70g CHO/hr',
                'intervals': (4, 180),
                'on_power': 1.10,
                'off_power': 0.55,
                'duration': 180
            },
            '2': {
                'structure': '15min warmup Z2, 5x3min @ 110-115% FTP, 3min recovery between',
                'execution': 'Building volume - control the power, don\'t go too deep early',
                'intervals': (5, 180),
                'on_power': 1.12,
                'off_power': 0.55,
                'duration': 180
            },
            '3': {
                'structure': '15min warmup Z2, 6x3min @ 112-117% FTP, 3min recovery between',
                'execution': 'Full recovery between efforts. Build power through each interval',
                'intervals': (6, 180),
                'on_power': 1.15,
                'off_power': 0.55,
                'duration': 180
            },
            '4': {
                'structure': '15min warmup Z2, 6x3min @ 115-120% FTP, 2.5min recovery between',
                'execution': 'Reduced recovery - building tolerance. Control early, push late',
                'intervals': (6, 180),
                'on_power': 1.17,
                'off_power': 0.55,
                'duration': 180
            },
            '5': {
                'structure': '15min warmup Z2, 7x3min @ 118-123% FTP, 2.5min recovery between',
                'execution': 'Extended volume - maximum sustainable power',
                'intervals': (7, 180),
                'on_power': 1.20,
                'off_power': 0.55,
                'duration': 180
            },
            '6': {
                'structure': '15min warmup Z2, 8x3min @ 120-125% FTP, 2min recovery between',
                'execution': 'Maximum development - empty the tank on final intervals',
                'intervals': (8, 180),
                'on_power': 1.22,
                'off_power': 0.55,
                'duration': 180
            }
        }
    },
    {
        'name': 'Descending VO2 Pyramid',
        'levels': {
            '1': {
                'structure': '15min warmup Z2, 1 set: 4min @ 108% + 3min @ 110% + 2min @ 115% + 1min @ 120% FTP, 3min recovery between efforts',
                'execution': 'Learning the format - descending duration, ascending intensity',
                'cadence_prescription': '90-100rpm (high turnover)',
                'position_prescription': 'Seated, on the hoods',
                'timing_prescription': 'Fresh',
                'fueling': '60-70g CHO/hr',
                'pyramid': True,
                'efforts': [
                    {'duration': 240, 'power': 1.08},
                    {'duration': 180, 'power': 1.10},
                    {'duration': 120, 'power': 1.15},
                    {'duration': 60, 'power': 1.20}
                ],
                'recovery_duration': 180
            },
            '2': {
                'structure': '15min warmup Z2, 1.5 sets: 4min @ 110% + 3min @ 112% + 2min @ 117% + 1min @ 122% FTP, 5min between sets',
                'execution': 'Building volume - maintain form through intensity increase',
                'pyramid': True,
                'sets': 1.5,
                'efforts': [
                    {'duration': 240, 'power': 1.10},
                    {'duration': 180, 'power': 1.12},
                    {'duration': 120, 'power': 1.17},
                    {'duration': 60, 'power': 1.22}
                ],
                'recovery_duration': 180,
                'set_recovery': 300
            },
            '3': {
                'structure': '15min warmup Z2, 2 sets: 4min @ 112% + 3min @ 115% + 2min @ 118% + 1min @ 125% FTP, 5min between sets',
                'execution': 'Full pyramid sets - mental game of knowing it gets shorter',
                'pyramid': True,
                'sets': 2,
                'efforts': [
                    {'duration': 240, 'power': 1.12},
                    {'duration': 180, 'power': 1.15},
                    {'duration': 120, 'power': 1.18},
                    {'duration': 60, 'power': 1.25}
                ],
                'recovery_duration': 180,
                'set_recovery': 300
            },
            '4': {
                'structure': '15min warmup Z2, 2 sets: 4min @ 115% + 3min @ 117% + 2min @ 120% + 1min @ 128% FTP, 5min between sets',
                'execution': 'Increased intensity - push hard on short efforts',
                'pyramid': True,
                'sets': 2,
                'efforts': [
                    {'duration': 240, 'power': 1.15},
                    {'duration': 180, 'power': 1.17},
                    {'duration': 120, 'power': 1.20},
                    {'duration': 60, 'power': 1.28}
                ],
                'recovery_duration': 180,
                'set_recovery': 300
            },
            '5': {
                'structure': '15min warmup Z2, 2.5 sets: 4min @ 117% + 3min @ 120% + 2min @ 123% + 1min @ 130% FTP, 5min between sets',
                'execution': 'Extended volume - race-realistic intensity changes',
                'pyramid': True,
                'sets': 2.5,
                'efforts': [
                    {'duration': 240, 'power': 1.17},
                    {'duration': 180, 'power': 1.20},
                    {'duration': 120, 'power': 1.23},
                    {'duration': 60, 'power': 1.30}
                ],
                'recovery_duration': 180,
                'set_recovery': 300
            },
            '6': {
                'structure': '15min warmup Z2, 3 sets: 4min @ 118% + 3min @ 122% + 2min @ 125% + 1min @ 135% FTP, 4min between sets',
                'execution': 'Maximum development - reduced recovery between sets, all-out final efforts',
                'pyramid': True,
                'sets': 3,
                'efforts': [
                    {'duration': 240, 'power': 1.18},
                    {'duration': 180, 'power': 1.22},
                    {'duration': 120, 'power': 1.25},
                    {'duration': 60, 'power': 1.35}
                ],
                'recovery_duration': 180,
                'set_recovery': 240
            }
        }
    },
    {
        'name': 'Norwegian 4x8',
        'levels': {
            '1': {
                'structure': '15min warmup Z2, 3x8min @ 88-90% HRmax (~105-108% FTP), 4min recovery between',
                'execution': 'Learning the Seiler format - controlled intensity, full recovery',
                'cadence_prescription': '85-95rpm (race cadence)',
                'position_prescription': 'Seated, on the hoods',
                'timing_prescription': 'Fresh',
                'fueling': '60-70g CHO/hr',
                'intervals': (3, 480),
                'on_power': 1.06,
                'off_power': 0.55,
                'duration': 480
            },
            '2': {
                'structure': '15min warmup Z2, 4x8min @ 88-90% HRmax (~107-110% FTP), 4min recovery between',
                'execution': 'Classic Seiler format - research-backed optimal duration for masters',
                'intervals': (4, 480),
                'on_power': 1.08,
                'off_power': 0.55,
                'duration': 480
            },
            '3': {
                'structure': '15min warmup Z2, 4x8min @ 90% HRmax (~108-112% FTP), 3.5min recovery between',
                'execution': 'Reduced recovery - building tolerance while maintaining duration',
                'intervals': (4, 480),
                'on_power': 1.10,
                'off_power': 0.55,
                'duration': 480
            },
            '4': {
                'structure': '15min warmup Z2, 5x8min @ 90% HRmax (~110-113% FTP), 3.5min recovery between',
                'execution': 'Extended volume - accumulating time at VO2max workload',
                'intervals': (5, 480),
                'on_power': 1.11,
                'off_power': 0.55,
                'duration': 480
            },
            '5': {
                'structure': '15min warmup Z2, 5x8min @ 90-92% HRmax (~112-115% FTP), 3min recovery between',
                'execution': 'Increased intensity with reduced recovery - near race simulation',
                'intervals': (5, 480),
                'on_power': 1.13,
                'off_power': 0.55,
                'duration': 480
            },
            '6': {
                'structure': '15min warmup Z2, 6x8min @ 92% HRmax (~113-118% FTP), 3min recovery between',
                'execution': 'Maximum sustainable volume at VO2max - 48min total work',
                'intervals': (6, 480),
                'on_power': 1.15,
                'off_power': 0.55,
                'duration': 480
            }
        }
    },
    {
        'name': 'VO2max with Loaded Recovery',
        'levels': {
            '1': {
                'structure': '15min warmup Z2, 3x (3min @ 115% FTP + 2min @ 85% FTP), 3min Z1 between sets',
                'execution': 'Learning the format - VO2 effort followed by tempo recovery, not Z1',
                'cadence_prescription': '90-100rpm on, 85-90rpm recovery',
                'position_prescription': 'Seated throughout',
                'timing_prescription': 'Fresh',
                'fueling': '60-70g CHO/hr',
                'loaded_recovery': True,
                'intervals': (3, 300),
                'on_power': 1.15,
                'loaded_power': 0.85,
                'loaded_duration': 120,
                'off_power': 0.50,
                'off_duration': 180
            },
            '2': {
                'structure': '15min warmup Z2, 4x (3min @ 117% FTP + 2min @ 85% FTP), 3min Z1 between sets',
                'execution': 'Building volume - tempo recovery keeps HR elevated',
                'loaded_recovery': True,
                'intervals': (4, 300),
                'on_power': 1.17,
                'loaded_power': 0.85,
                'loaded_duration': 120,
                'off_power': 0.50,
                'off_duration': 180
            },
            '3': {
                'structure': '15min warmup Z2, 4x (3min @ 118% FTP + 2.5min @ 87% FTP), 2.5min Z1 between sets',
                'execution': 'Extended tempo recovery - more time above threshold',
                'loaded_recovery': True,
                'intervals': (4, 330),
                'on_power': 1.18,
                'loaded_power': 0.87,
                'loaded_duration': 150,
                'off_power': 0.50,
                'off_duration': 150
            },
            '4': {
                'structure': '15min warmup Z2, 5x (3min @ 120% FTP + 2.5min @ 88% FTP), 2.5min Z1 between sets',
                'execution': 'Increased volume and intensity - race simulation',
                'loaded_recovery': True,
                'intervals': (5, 330),
                'on_power': 1.20,
                'loaded_power': 0.88,
                'loaded_duration': 150,
                'off_power': 0.50,
                'off_duration': 150
            },
            '5': {
                'structure': '15min warmup Z2, 5x (3.5min @ 120% FTP + 2.5min @ 88% FTP), 2min Z1 between sets',
                'execution': 'Extended VO2 efforts - reduced full recovery',
                'loaded_recovery': True,
                'intervals': (5, 360),
                'on_power': 1.20,
                'loaded_power': 0.88,
                'loaded_duration': 150,
                'off_power': 0.50,
                'off_duration': 120
            },
            '6': {
                'structure': '15min warmup Z2, 6x (3.5min @ 122% FTP + 2.5min @ 90% FTP), 2min Z1 between sets',
                'execution': 'Maximum development - G-Spot recovery keeps legs burning',
                'loaded_recovery': True,
                'intervals': (6, 360),
                'on_power': 1.22,
                'loaded_power': 0.90,
                'loaded_duration': 150,
                'off_power': 0.50,
                'off_duration': 120
            }
        }
    }
]


# =============================================================================
# THRESHOLD/TT ADDITIONS
# =============================================================================

THRESHOLD_NEW = [
    {
        'name': 'Single Sustained Threshold',
        'levels': {
            '1': {
                'structure': '20min warmup Z2 with 2x1min openers, 1x20min @ 95-98% FTP, 10min cooldown',
                'execution': 'Mental toughness builder - one long effort, no breaks. Start conservative',
                'cadence_prescription': '85-95rpm (race cadence)',
                'position_prescription': 'Seated, aero if comfortable',
                'timing_prescription': 'Fresh',
                'fueling': '60-70g CHO/hr',
                'single_effort': True,
                'duration': 1200,
                'power': 0.96
            },
            '2': {
                'structure': '20min warmup Z2 with 2x1min openers, 1x25min @ 96-99% FTP, 10min cooldown',
                'execution': 'Building duration - find your rhythm and lock in',
                'single_effort': True,
                'duration': 1500,
                'power': 0.97
            },
            '3': {
                'structure': '20min warmup Z2 with 2x1min openers, 1x30min @ 97-100% FTP, 10min cooldown',
                'execution': 'Classic TT duration - steady, controlled power throughout',
                'single_effort': True,
                'duration': 1800,
                'power': 0.98
            },
            '4': {
                'structure': '20min warmup Z2 with 2x1min openers, 1x35min @ 98-101% FTP, 10min cooldown',
                'execution': 'Extended threshold - break it into mental thirds',
                'single_effort': True,
                'duration': 2100,
                'power': 0.99
            },
            '5': {
                'structure': '20min warmup Z2 with 2x1min openers, 1x40min @ 98-101% FTP, 10min cooldown',
                'execution': 'Race-realistic duration - this is your FTP test effort',
                'single_effort': True,
                'duration': 2400,
                'power': 1.00
            },
            '6': {
                'structure': '20min warmup Z2 with 2x1min openers, 1x45min @ 98-102% FTP, 10min cooldown',
                'execution': 'Maximum threshold duration - mental fortress training',
                'single_effort': True,
                'duration': 2700,
                'power': 1.00
            }
        }
    },
    {
        'name': 'Threshold Ramps',
        'levels': {
            '1': {
                'structure': '15min warmup Z2, 2x12min ramp: start @ 90% FTP, increase 2% every 3min to finish @ 98%, 5min recovery',
                'execution': 'Learning progressive building - smooth power increases',
                'cadence_prescription': '85-95rpm throughout',
                'position_prescription': 'Seated, on the hoods',
                'timing_prescription': 'Fresh',
                'fueling': '60-70g CHO/hr',
                'ramp': True,
                'intervals': (2, 720),
                'start_power': 0.90,
                'end_power': 0.98,
                'step_duration': 180,
                'off_power': 0.55,
                'off_duration': 300
            },
            '2': {
                'structure': '15min warmup Z2, 2x15min ramp: start @ 88% FTP, increase 2% every 3min to finish @ 100%, 5min recovery',
                'execution': 'Extended ramp - teaches negative splitting',
                'ramp': True,
                'intervals': (2, 900),
                'start_power': 0.88,
                'end_power': 1.00,
                'step_duration': 180,
                'off_power': 0.55,
                'off_duration': 300
            },
            '3': {
                'structure': '15min warmup Z2, 2x15min ramp: start @ 88% FTP, increase 2% every 3min to finish @ 102%, 5min recovery',
                'execution': 'Building to supra-threshold finish - race simulation',
                'ramp': True,
                'intervals': (2, 900),
                'start_power': 0.88,
                'end_power': 1.02,
                'step_duration': 180,
                'off_power': 0.55,
                'off_duration': 300
            },
            '4': {
                'structure': '15min warmup Z2, 3x12min ramp: start @ 88% FTP, increase 2.5% every 3min to finish @ 100%, 5min recovery',
                'execution': 'Increased volume - three ramps with steeper progression',
                'ramp': True,
                'intervals': (3, 720),
                'start_power': 0.88,
                'end_power': 1.00,
                'step_duration': 180,
                'off_power': 0.55,
                'off_duration': 300
            },
            '5': {
                'structure': '15min warmup Z2, 3x15min ramp: start @ 87% FTP, increase 2% every 3min to finish @ 101%, 4min recovery',
                'execution': 'Reduced recovery - building threshold capacity under fatigue',
                'ramp': True,
                'intervals': (3, 900),
                'start_power': 0.87,
                'end_power': 1.01,
                'step_duration': 180,
                'off_power': 0.55,
                'off_duration': 240
            },
            '6': {
                'structure': '15min warmup Z2, 3x18min ramp: start @ 85% FTP, increase 2% every 3min to finish @ 101%, 4min recovery',
                'execution': 'Maximum ramp duration - start easy, finish at threshold',
                'ramp': True,
                'intervals': (3, 1080),
                'start_power': 0.85,
                'end_power': 1.01,
                'step_duration': 180,
                'off_power': 0.55,
                'off_duration': 240
            }
        }
    },
    {
        'name': 'Descending Threshold',
        'levels': {
            '1': {
                'structure': '15min warmup Z2, 12min @ 96% + 10min @ 98% + 8min @ 100% FTP, 5min recovery between',
                'execution': 'Learning the format - getting shorter and harder as you tire',
                'cadence_prescription': '85-95rpm (race cadence)',
                'position_prescription': 'Seated, on the hoods',
                'timing_prescription': 'Fresh',
                'fueling': '60-70g CHO/hr',
                'descending': True,
                'efforts': [
                    {'duration': 720, 'power': 0.96},
                    {'duration': 600, 'power': 0.98},
                    {'duration': 480, 'power': 1.00}
                ],
                'recovery_duration': 300
            },
            '2': {
                'structure': '15min warmup Z2, 15min @ 96% + 12min @ 98% + 8min @ 100% FTP, 5min recovery between',
                'execution': 'Building duration - longer opener, same progression',
                'descending': True,
                'efforts': [
                    {'duration': 900, 'power': 0.96},
                    {'duration': 720, 'power': 0.98},
                    {'duration': 480, 'power': 1.00}
                ],
                'recovery_duration': 300
            },
            '3': {
                'structure': '15min warmup Z2, 15min @ 97% + 12min @ 99% + 10min @ 101% FTP, 5min recovery between',
                'execution': 'Increased intensity - finish above threshold',
                'descending': True,
                'efforts': [
                    {'duration': 900, 'power': 0.97},
                    {'duration': 720, 'power': 0.99},
                    {'duration': 600, 'power': 1.01}
                ],
                'recovery_duration': 300
            },
            '4': {
                'structure': '15min warmup Z2, 15min @ 97% + 12min @ 100% + 10min @ 102% + 5min @ 105% FTP, 4min recovery between',
                'execution': 'Added 4th effort - finish with VO2 kick',
                'descending': True,
                'efforts': [
                    {'duration': 900, 'power': 0.97},
                    {'duration': 720, 'power': 1.00},
                    {'duration': 600, 'power': 1.02},
                    {'duration': 300, 'power': 1.05}
                ],
                'recovery_duration': 240
            },
            '5': {
                'structure': '15min warmup Z2, 18min @ 97% + 14min @ 100% + 10min @ 103% + 5min @ 108% FTP, 4min recovery between',
                'execution': 'Extended opener - race simulation with strong finish',
                'descending': True,
                'efforts': [
                    {'duration': 1080, 'power': 0.97},
                    {'duration': 840, 'power': 1.00},
                    {'duration': 600, 'power': 1.03},
                    {'duration': 300, 'power': 1.08}
                ],
                'recovery_duration': 240
            },
            '6': {
                'structure': '15min warmup Z2, 20min @ 97% + 15min @ 100% + 10min @ 103% + 5min @ 110% FTP, 3min recovery between',
                'execution': 'Maximum development - reduced recovery, strong VO2 finish',
                'descending': True,
                'efforts': [
                    {'duration': 1200, 'power': 0.97},
                    {'duration': 900, 'power': 1.00},
                    {'duration': 600, 'power': 1.03},
                    {'duration': 300, 'power': 1.10}
                ],
                'recovery_duration': 180
            }
        }
    }
]


# =============================================================================
# SPRINT/NEUROMUSCULAR ADDITIONS
# =============================================================================

SPRINT_NEW = [
    {
        'name': 'Attack Repeats',
        'levels': {
            '1': {
                'structure': '15min warmup Z2, 4x30sec @ 150% FTP all-out, 3min recovery between',
                'execution': 'Race-breaking efforts - simulate attacking off the front',
                'cadence_prescription': '100-120rpm (high power, high turnover)',
                'position_prescription': 'Out of saddle for first 10sec, then seated',
                'timing_prescription': 'Fresh',
                'fueling': '60-70g CHO/hr',
                'intervals': (4, 30),
                'on_power': 1.50,
                'off_power': 0.50,
                'duration': 30,
                'off_duration': 180
            },
            '2': {
                'structure': '15min warmup Z2, 5x30sec @ 150% FTP all-out, 2.5min recovery between',
                'execution': 'Building volume - reduced recovery simulates race fatigue',
                'intervals': (5, 30),
                'on_power': 1.50,
                'off_power': 0.50,
                'duration': 30,
                'off_duration': 150
            },
            '3': {
                'structure': '15min warmup Z2, 6x30sec @ 150% FTP all-out, 2.5min recovery between',
                'execution': 'Increased volume - maintain power across all repeats',
                'intervals': (6, 30),
                'on_power': 1.50,
                'off_power': 0.50,
                'duration': 30,
                'off_duration': 150
            },
            '4': {
                'structure': '15min warmup Z2, 6x30sec @ 155% FTP all-out, 2min recovery between',
                'execution': 'Increased intensity, reduced recovery - attack training',
                'intervals': (6, 30),
                'on_power': 1.55,
                'off_power': 0.50,
                'duration': 30,
                'off_duration': 120
            },
            '5': {
                'structure': '15min warmup Z2, 7x30sec @ 155% FTP all-out, 2min recovery between',
                'execution': 'Extended volume - race-realistic attack frequency',
                'intervals': (7, 30),
                'on_power': 1.55,
                'off_power': 0.50,
                'duration': 30,
                'off_duration': 120
            },
            '6': {
                'structure': '15min warmup Z2, 8x30sec @ 160% FTP all-out, 1.5min recovery between',
                'execution': 'Maximum development - repeated attacks with minimal recovery',
                'intervals': (8, 30),
                'on_power': 1.60,
                'off_power': 0.50,
                'duration': 30,
                'off_duration': 90
            }
        }
    },
    {
        'name': 'Sprint Buildups',
        'levels': {
            '1': {
                'structure': '15min warmup Z2, 2 sets: 10sec + 15sec + 20sec + 30sec @ max, 2min between efforts, 5min between sets',
                'execution': 'Learning the format - progressive duration, all-out efforts',
                'cadence_prescription': 'Max sustainable for each duration',
                'position_prescription': 'Out of saddle',
                'timing_prescription': 'Fresh',
                'fueling': '60-70g CHO/hr',
                'buildup': True,
                'sets': 2,
                'efforts': [10, 15, 20, 30],
                'on_power': 1.80,  # Approximate max
                'effort_recovery': 120,
                'set_recovery': 300
            },
            '2': {
                'structure': '15min warmup Z2, 2 sets: 10sec + 15sec + 20sec + 30sec @ max, 1.5min between efforts, 5min between sets',
                'execution': 'Reduced recovery between efforts - building repeatability',
                'buildup': True,
                'sets': 2,
                'efforts': [10, 15, 20, 30],
                'on_power': 1.80,
                'effort_recovery': 90,
                'set_recovery': 300
            },
            '3': {
                'structure': '15min warmup Z2, 3 sets: 10sec + 15sec + 20sec + 30sec @ max, 1.5min between efforts, 5min between sets',
                'execution': 'Increased volume - three full sets',
                'buildup': True,
                'sets': 3,
                'efforts': [10, 15, 20, 30],
                'on_power': 1.80,
                'effort_recovery': 90,
                'set_recovery': 300
            },
            '4': {
                'structure': '15min warmup Z2, 3 sets: 10sec + 15sec + 20sec + 30sec + 45sec @ max, 1.5min between efforts, 4min between sets',
                'execution': 'Added 45sec effort - extended anaerobic duration',
                'buildup': True,
                'sets': 3,
                'efforts': [10, 15, 20, 30, 45],
                'on_power': 1.70,
                'effort_recovery': 90,
                'set_recovery': 240
            },
            '5': {
                'structure': '15min warmup Z2, 3 sets: 10sec + 15sec + 20sec + 30sec + 45sec @ max, 1min between efforts, 4min between sets',
                'execution': 'Reduced recovery - race simulation',
                'buildup': True,
                'sets': 3,
                'efforts': [10, 15, 20, 30, 45],
                'on_power': 1.70,
                'effort_recovery': 60,
                'set_recovery': 240
            },
            '6': {
                'structure': '15min warmup Z2, 4 sets: 10sec + 15sec + 20sec + 30sec + 45sec @ max, 1min between efforts, 3min between sets',
                'execution': 'Maximum development - four sets, minimal recovery',
                'buildup': True,
                'sets': 4,
                'efforts': [10, 15, 20, 30, 45],
                'on_power': 1.70,
                'effort_recovery': 60,
                'set_recovery': 180
            }
        }
    },
    {
        'name': 'Peak and Fade',
        'levels': {
            '1': {
                'structure': '15min warmup Z2, 4x (10sec MAX + 20sec @ 80% of sprint), 3min recovery between',
                'execution': 'Learning the format - explosive start, controlled fade',
                'cadence_prescription': 'Max then settle to 90-100rpm',
                'position_prescription': 'Standing start, sit after 10sec',
                'timing_prescription': 'Fresh',
                'fueling': '60-70g CHO/hr',
                'peak_fade': True,
                'intervals': (4, 30),
                'peak_duration': 10,
                'peak_power': 2.00,  # Max sprint
                'fade_duration': 20,
                'fade_power': 1.20,
                'off_power': 0.50,
                'off_duration': 180
            },
            '2': {
                'structure': '15min warmup Z2, 5x (10sec MAX + 20sec @ 80% of sprint), 2.5min recovery between',
                'execution': 'Building volume - maintain peak power across repeats',
                'peak_fade': True,
                'intervals': (5, 30),
                'peak_duration': 10,
                'peak_power': 2.00,
                'fade_duration': 20,
                'fade_power': 1.20,
                'off_power': 0.50,
                'off_duration': 150
            },
            '3': {
                'structure': '15min warmup Z2, 5x (12sec MAX + 25sec @ 80% of sprint), 2.5min recovery between',
                'execution': 'Extended efforts - longer peak, longer fade',
                'peak_fade': True,
                'intervals': (5, 37),
                'peak_duration': 12,
                'peak_power': 2.00,
                'fade_duration': 25,
                'fade_power': 1.20,
                'off_power': 0.50,
                'off_duration': 150
            },
            '4': {
                'structure': '15min warmup Z2, 6x (12sec MAX + 25sec @ 80% of sprint), 2min recovery between',
                'execution': 'Increased volume with reduced recovery',
                'peak_fade': True,
                'intervals': (6, 37),
                'peak_duration': 12,
                'peak_power': 2.00,
                'fade_duration': 25,
                'fade_power': 1.20,
                'off_power': 0.50,
                'off_duration': 120
            },
            '5': {
                'structure': '15min warmup Z2, 6x (15sec MAX + 25sec @ 80% of sprint), 2min recovery between',
                'execution': 'Extended peak duration - longer max effort',
                'peak_fade': True,
                'intervals': (6, 40),
                'peak_duration': 15,
                'peak_power': 2.00,
                'fade_duration': 25,
                'fade_power': 1.20,
                'off_power': 0.50,
                'off_duration': 120
            },
            '6': {
                'structure': '15min warmup Z2, 7x (15sec MAX + 30sec @ 80% of sprint), 1.5min recovery between',
                'execution': 'Maximum development - sprint contest simulation',
                'peak_fade': True,
                'intervals': (7, 45),
                'peak_duration': 15,
                'peak_power': 2.00,
                'fade_duration': 30,
                'fade_power': 1.20,
                'off_power': 0.50,
                'off_duration': 90
            }
        }
    },
    {
        'name': 'ILT Single Leg Training',
        'levels': {
            '1': {
                'structure': '15min warmup Z2, 4x1min single leg (alternating), 1min both legs between, Z2 power',
                'execution': 'Learning the format - focus on smooth pedal stroke, eliminate dead spots',
                'cadence_prescription': '70-80rpm (lower than normal for control)',
                'position_prescription': 'Seated, hands relaxed',
                'timing_prescription': 'Fresh or recovery day',
                'fueling': 'Normal hydration',
                'ilt': True,
                'intervals': (4, 60),
                'power': 0.70,  # Z2 power
                'cadence': 75,
                'off_duration': 60
            },
            '2': {
                'structure': '15min warmup Z2, 5x1min single leg (alternating), 1min both legs between, Z2 power',
                'execution': 'Building volume - maintain smooth stroke throughout',
                'ilt': True,
                'intervals': (5, 60),
                'power': 0.70,
                'cadence': 75,
                'off_duration': 60
            },
            '3': {
                'structure': '15min warmup Z2, 6x1min single leg (alternating), 45sec both legs between, Z2 power',
                'execution': 'Reduced recovery - building endurance in the pattern',
                'ilt': True,
                'intervals': (6, 60),
                'power': 0.70,
                'cadence': 80,
                'off_duration': 45
            },
            '4': {
                'structure': '15min warmup Z2, 6x90sec single leg (alternating), 45sec both legs between, Z2 power',
                'execution': 'Extended duration - longer single leg efforts',
                'ilt': True,
                'intervals': (6, 90),
                'power': 0.70,
                'cadence': 80,
                'off_duration': 45
            },
            '5': {
                'structure': '15min warmup Z2, 8x90sec single leg (alternating), 30sec both legs between, Z2 power',
                'execution': 'Increased volume - minimal recovery between legs',
                'ilt': True,
                'intervals': (8, 90),
                'power': 0.70,
                'cadence': 85,
                'off_duration': 30
            },
            '6': {
                'structure': '15min warmup Z2, 8x2min single leg (alternating), 30sec both legs between, Z2 power',
                'execution': 'Maximum duration - 2min single leg efforts for pedaling efficiency',
                'ilt': True,
                'intervals': (8, 120),
                'power': 0.70,
                'cadence': 85,
                'off_duration': 30
            }
        }
    }
]


# =============================================================================
# ANAEROBIC CAPACITY (NEW CATEGORY)
# =============================================================================

ANAEROBIC_CAPACITY = [
    {
        'name': '2min Killers',
        'levels': {
            '1': {
                'structure': '15min warmup Z2, 3x2min @ 115% FTP, 4min recovery between',
                'execution': 'Learning lactate tolerance - these hurt. Pace evenly, don\'t blow up',
                'cadence_prescription': '90-100rpm (high turnover reduces muscle tension)',
                'position_prescription': 'Seated, on the hoods',
                'timing_prescription': 'Fresh',
                'fueling': '60-70g CHO/hr',
                'intervals': (3, 120),
                'on_power': 1.15,
                'off_power': 0.50,
                'duration': 120,
                'off_duration': 240
            },
            '2': {
                'structure': '15min warmup Z2, 4x2min @ 115% FTP, 4min recovery between',
                'execution': 'Building volume - maintain power across all repeats',
                'intervals': (4, 120),
                'on_power': 1.15,
                'off_power': 0.50,
                'duration': 120,
                'off_duration': 240
            },
            '3': {
                'structure': '15min warmup Z2, 4x2min @ 118% FTP, 3.5min recovery between',
                'execution': 'Increased intensity, reduced recovery - building tolerance',
                'intervals': (4, 120),
                'on_power': 1.18,
                'off_power': 0.50,
                'duration': 120,
                'off_duration': 210
            },
            '4': {
                'structure': '15min warmup Z2, 5x2min @ 118% FTP, 3min recovery between',
                'execution': 'Extended volume - race-breaking power',
                'intervals': (5, 120),
                'on_power': 1.18,
                'off_power': 0.50,
                'duration': 120,
                'off_duration': 180
            },
            '5': {
                'structure': '15min warmup Z2, 5x2min @ 120% FTP, 2.5min recovery between',
                'execution': 'Reduced recovery - simulates repeated attacks',
                'intervals': (5, 120),
                'on_power': 1.20,
                'off_power': 0.50,
                'duration': 120,
                'off_duration': 150
            },
            '6': {
                'structure': '15min warmup Z2, 6x2min @ 120% FTP, 2min recovery between',
                'execution': 'Maximum development - 12min total at race-breaking power',
                'intervals': (6, 120),
                'on_power': 1.20,
                'off_power': 0.50,
                'duration': 120,
                'off_duration': 120
            }
        }
    },
    {
        'name': '90sec Repeats',
        'levels': {
            '1': {
                'structure': '15min warmup Z2, 4x90sec @ 120% FTP, 3min recovery between',
                'execution': 'Short, sharp efforts - race-breaking intensity',
                'cadence_prescription': '95-105rpm (high turnover)',
                'position_prescription': 'Seated or standing as needed',
                'timing_prescription': 'Fresh',
                'fueling': '60-70g CHO/hr',
                'intervals': (4, 90),
                'on_power': 1.20,
                'off_power': 0.50,
                'duration': 90,
                'off_duration': 180
            },
            '2': {
                'structure': '15min warmup Z2, 5x90sec @ 120% FTP, 3min recovery between',
                'execution': 'Building volume - maintain power consistency',
                'intervals': (5, 90),
                'on_power': 1.20,
                'off_power': 0.50,
                'duration': 90,
                'off_duration': 180
            },
            '3': {
                'structure': '15min warmup Z2, 5x90sec @ 122% FTP, 2.5min recovery between',
                'execution': 'Increased intensity with reduced recovery',
                'intervals': (5, 90),
                'on_power': 1.22,
                'off_power': 0.50,
                'duration': 90,
                'off_duration': 150
            },
            '4': {
                'structure': '15min warmup Z2, 6x90sec @ 122% FTP, 2.5min recovery between',
                'execution': 'Extended volume - attack repeatability',
                'intervals': (6, 90),
                'on_power': 1.22,
                'off_power': 0.50,
                'duration': 90,
                'off_duration': 150
            },
            '5': {
                'structure': '15min warmup Z2, 6x90sec @ 125% FTP, 2min recovery between',
                'execution': 'Reduced recovery at high intensity - race simulation',
                'intervals': (6, 90),
                'on_power': 1.25,
                'off_power': 0.50,
                'duration': 90,
                'off_duration': 120
            },
            '6': {
                'structure': '15min warmup Z2, 8x90sec @ 125% FTP, 1.5min recovery between',
                'execution': 'Maximum development - repeated race-breaking efforts',
                'intervals': (8, 90),
                'on_power': 1.25,
                'off_power': 0.50,
                'duration': 90,
                'off_duration': 90
            }
        }
    },
    {
        'name': '1min All-Out Repeats',
        'levels': {
            '1': {
                'structure': '15min warmup Z2, 4x1min @ 130% FTP, 3min recovery between',
                'execution': 'Maximum 1min power - neuromuscular + anaerobic',
                'cadence_prescription': '100-110rpm (high turnover)',
                'position_prescription': 'Standing start, sit as needed',
                'timing_prescription': 'Fresh',
                'fueling': '60-70g CHO/hr',
                'intervals': (4, 60),
                'on_power': 1.30,
                'off_power': 0.50,
                'duration': 60,
                'off_duration': 180
            },
            '2': {
                'structure': '15min warmup Z2, 5x1min @ 130% FTP, 2.5min recovery between',
                'execution': 'Building volume with reduced recovery',
                'intervals': (5, 60),
                'on_power': 1.30,
                'off_power': 0.50,
                'duration': 60,
                'off_duration': 150
            },
            '3': {
                'structure': '15min warmup Z2, 5x1min @ 135% FTP, 2.5min recovery between',
                'execution': 'Increased intensity - approaching sprint territory',
                'intervals': (5, 60),
                'on_power': 1.35,
                'off_power': 0.50,
                'duration': 60,
                'off_duration': 150
            },
            '4': {
                'structure': '15min warmup Z2, 6x1min @ 135% FTP, 2min recovery between',
                'execution': 'Extended volume - repeatability under fatigue',
                'intervals': (6, 60),
                'on_power': 1.35,
                'off_power': 0.50,
                'duration': 60,
                'off_duration': 120
            },
            '5': {
                'structure': '15min warmup Z2, 7x1min @ 135% FTP, 1.5min recovery between',
                'execution': 'Minimal recovery - race simulation',
                'intervals': (7, 60),
                'on_power': 1.35,
                'off_power': 0.50,
                'duration': 60,
                'off_duration': 90
            },
            '6': {
                'structure': '15min warmup Z2, 8x1min @ 140% FTP, 1.5min recovery between',
                'execution': 'Maximum development - 8min total at near-max power',
                'intervals': (8, 60),
                'on_power': 1.40,
                'off_power': 0.50,
                'duration': 60,
                'off_duration': 90
            }
        }
    }
]


# =============================================================================
# DURABILITY ADDITIONS
# =============================================================================

DURABILITY_NEW = [
    {
        'name': 'Tired VO2max',
        'levels': {
            '1': {
                'structure': '2hr Z2 endurance, then 2x4min @ 110% FTP with 4min recovery',
                'execution': 'VO2max when exhausted - these will feel harder than fresh. Good.',
                'cadence_prescription': '90-100rpm (maintain turnover)',
                'position_prescription': 'Seated, on the hoods',
                'timing_prescription': 'Late-ride (after 2hr)',
                'fueling': '60-80g CHO/hr throughout - critical for late quality',
                'tired_vo2': True,
                'base_duration': 7200,
                'base_power': 0.70,
                'intervals': (2, 240),
                'on_power': 1.10,
                'off_power': 0.55,
                'off_duration': 240
            },
            '2': {
                'structure': '2.5hr Z2 endurance, then 3x4min @ 112% FTP with 4min recovery',
                'execution': 'Building volume - VO2max efforts after extended base',
                'tired_vo2': True,
                'base_duration': 9000,
                'base_power': 0.70,
                'intervals': (3, 240),
                'on_power': 1.12,
                'off_power': 0.55,
                'off_duration': 240
            },
            '3': {
                'structure': '2.5hr Z2 endurance, then 3x4min @ 115% FTP with 3.5min recovery',
                'execution': 'Increased intensity with reduced recovery',
                'tired_vo2': True,
                'base_duration': 9000,
                'base_power': 0.70,
                'intervals': (3, 240),
                'on_power': 1.15,
                'off_power': 0.55,
                'off_duration': 210
            },
            '4': {
                'structure': '3hr Z2 endurance, then 4x4min @ 115% FTP with 3min recovery',
                'execution': 'Extended base duration - race-realistic fatigue',
                'tired_vo2': True,
                'base_duration': 10800,
                'base_power': 0.70,
                'intervals': (4, 240),
                'on_power': 1.15,
                'off_power': 0.55,
                'off_duration': 180
            },
            '5': {
                'structure': '3.5hr Z2 endurance, then 4x4min @ 117% FTP with 3min recovery',
                'execution': 'Extended pre-load - this is Unbound simulation',
                'tired_vo2': True,
                'base_duration': 12600,
                'base_power': 0.70,
                'intervals': (4, 240),
                'on_power': 1.17,
                'off_power': 0.55,
                'off_duration': 180
            },
            '6': {
                'structure': '4hr Z2 endurance, then 5x4min @ 118% FTP with 2.5min recovery',
                'execution': 'Maximum development - 4hr pre-load, 5 VO2 efforts',
                'tired_vo2': True,
                'base_duration': 14400,
                'base_power': 0.70,
                'intervals': (5, 240),
                'on_power': 1.18,
                'off_power': 0.55,
                'off_duration': 150
            }
        }
    },
    {
        'name': 'Double Day Simulation',
        'levels': {
            '1': {
                'structure': 'AM: 1.5hr Z2 easy. PM (4-6hr later): 3x8min @ 100% FTP with 5min recovery',
                'execution': 'Simulates stage race or back-to-back training - quality on tired legs',
                'cadence_prescription': '85-95rpm PM session',
                'position_prescription': 'Seated, on the hoods',
                'timing_prescription': 'Split session - 4-6hr between',
                'fueling': 'Refuel between sessions: 1.2g CHO/kg/hr + protein',
                'double_day': True,
                'am_duration': 5400,
                'am_power': 0.70,
                'pm_intervals': (3, 480),
                'pm_on_power': 1.00,
                'pm_off_power': 0.55,
                'pm_off_duration': 300
            },
            '2': {
                'structure': 'AM: 2hr Z2 easy. PM (4-6hr later): 3x10min @ 100% FTP with 5min recovery',
                'execution': 'Extended AM ride - building durability',
                'double_day': True,
                'am_duration': 7200,
                'am_power': 0.70,
                'pm_intervals': (3, 600),
                'pm_on_power': 1.00,
                'pm_off_power': 0.55,
                'pm_off_duration': 300
            },
            '3': {
                'structure': 'AM: 2hr Z2 easy. PM (4-6hr later): 3x12min @ 100% FTP with 4min recovery',
                'execution': 'Extended PM efforts - threshold durability',
                'double_day': True,
                'am_duration': 7200,
                'am_power': 0.70,
                'pm_intervals': (3, 720),
                'pm_on_power': 1.00,
                'pm_off_power': 0.55,
                'pm_off_duration': 240
            },
            '4': {
                'structure': 'AM: 2.5hr Z2 easy. PM (4-6hr later): 3x12min @ 100% FTP with 4min recovery',
                'execution': 'Extended AM - more pre-fatigue before quality',
                'double_day': True,
                'am_duration': 9000,
                'am_power': 0.70,
                'pm_intervals': (3, 720),
                'pm_on_power': 1.00,
                'pm_off_power': 0.55,
                'pm_off_duration': 240
            },
            '5': {
                'structure': 'AM: 2.5hr Z2 easy. PM (4-6hr later): 4x10min @ 100% FTP with 4min recovery',
                'execution': 'More PM volume - race simulation',
                'double_day': True,
                'am_duration': 9000,
                'am_power': 0.70,
                'pm_intervals': (4, 600),
                'pm_on_power': 1.00,
                'pm_off_power': 0.55,
                'pm_off_duration': 240
            },
            '6': {
                'structure': 'AM: 3hr Z2 easy. PM (4-6hr later): 4x12min @ 100% FTP with 3min recovery',
                'execution': 'Maximum development - 3hr AM, 48min threshold PM',
                'double_day': True,
                'am_duration': 10800,
                'am_power': 0.70,
                'pm_intervals': (4, 720),
                'pm_on_power': 1.00,
                'pm_off_power': 0.55,
                'pm_off_duration': 180
            }
        }
    },
    {
        'name': 'Progressive Fatigue Threshold',
        'levels': {
            '1': {
                'structure': '15min warmup Z2, 3x10min @ 98% FTP with 5min, 4min, 3min recovery (decreasing)',
                'execution': 'Learning the format - same effort, less recovery each time',
                'cadence_prescription': '85-95rpm (race cadence)',
                'position_prescription': 'Seated, on the hoods',
                'timing_prescription': 'Fresh',
                'fueling': '60-70g CHO/hr',
                'progressive_fatigue': True,
                'intervals': 3,
                'effort_duration': 600,
                'on_power': 0.98,
                'recovery_sequence': [300, 240, 180]
            },
            '2': {
                'structure': '15min warmup Z2, 3x12min @ 98% FTP with 5min, 4min, 3min recovery (decreasing)',
                'execution': 'Extended efforts - building threshold under progressive fatigue',
                'progressive_fatigue': True,
                'intervals': 3,
                'effort_duration': 720,
                'on_power': 0.98,
                'recovery_sequence': [300, 240, 180]
            },
            '3': {
                'structure': '15min warmup Z2, 4x10min @ 99% FTP with 5min, 4min, 3min, 2min recovery (decreasing)',
                'execution': 'Added 4th effort - final recovery only 2min',
                'progressive_fatigue': True,
                'intervals': 4,
                'effort_duration': 600,
                'on_power': 0.99,
                'recovery_sequence': [300, 240, 180, 120]
            },
            '4': {
                'structure': '15min warmup Z2, 4x12min @ 99% FTP with 5min, 4min, 3min, 2min recovery (decreasing)',
                'execution': 'Extended efforts with progressive fatigue',
                'progressive_fatigue': True,
                'intervals': 4,
                'effort_duration': 720,
                'on_power': 0.99,
                'recovery_sequence': [300, 240, 180, 120]
            },
            '5': {
                'structure': '15min warmup Z2, 4x12min @ 100% FTP with 4min, 3min, 2min, 1.5min recovery (decreasing)',
                'execution': 'Increased intensity with aggressive recovery reduction',
                'progressive_fatigue': True,
                'intervals': 4,
                'effort_duration': 720,
                'on_power': 1.00,
                'recovery_sequence': [240, 180, 120, 90]
            },
            '6': {
                'structure': '15min warmup Z2, 5x10min @ 100% FTP with 4min, 3min, 2.5min, 2min, 1.5min recovery (decreasing)',
                'execution': 'Maximum development - 5 efforts, final recovery 90sec',
                'progressive_fatigue': True,
                'intervals': 5,
                'effort_duration': 600,
                'on_power': 1.00,
                'recovery_sequence': [240, 180, 150, 120, 90]
            }
        }
    }
]


# =============================================================================
# ENDURANCE ADDITIONS
# =============================================================================

ENDURANCE_NEW = [
    {
        'name': 'Pre-Race Openers',
        'levels': {
            '1': {
                'structure': '20min Z1-Z2 easy, 2x30sec @ 110% FTP with 2min easy, 5min Z1 cooldown',
                'execution': 'Day before race - wake up the legs without creating fatigue',
                'cadence_prescription': '90-100rpm on efforts',
                'position_prescription': 'Seated, relaxed',
                'timing_prescription': 'Day before race or event',
                'fueling': 'Normal hydration only',
                'openers': True,
                'warmup_duration': 1200,
                'warmup_power': 0.65,
                'efforts': (2, 30),
                'effort_power': 1.10,
                'effort_recovery': 120,
                'cooldown_duration': 300
            },
            '2': {
                'structure': '25min Z1-Z2 easy, 3x30sec @ 110% FTP with 2min easy, 5min Z1 cooldown',
                'execution': 'Standard openers - 3 short efforts to activate',
                'openers': True,
                'warmup_duration': 1500,
                'warmup_power': 0.65,
                'efforts': (3, 30),
                'effort_power': 1.10,
                'effort_recovery': 120,
                'cooldown_duration': 300
            },
            '3': {
                'structure': '30min Z1-Z2 easy, 3x45sec @ 110% FTP with 2min easy, 5min Z1 cooldown',
                'execution': 'Extended efforts - slightly longer activation',
                'openers': True,
                'warmup_duration': 1800,
                'warmup_power': 0.65,
                'efforts': (3, 45),
                'effort_power': 1.10,
                'effort_recovery': 120,
                'cooldown_duration': 300
            },
            '4': {
                'structure': '30min Z1-Z2 easy, 4x30sec @ 115% FTP with 2min easy, 5min Z1 cooldown',
                'execution': 'Increased intensity - sharper activation',
                'openers': True,
                'warmup_duration': 1800,
                'warmup_power': 0.65,
                'efforts': (4, 30),
                'effort_power': 1.15,
                'effort_recovery': 120,
                'cooldown_duration': 300
            },
            '5': {
                'structure': '35min Z1-Z2 easy, 4x45sec @ 115% FTP with 2min easy, 5min Z1 cooldown',
                'execution': 'Extended openers - longer base ride with sharper efforts',
                'openers': True,
                'warmup_duration': 2100,
                'warmup_power': 0.65,
                'efforts': (4, 45),
                'effort_power': 1.15,
                'effort_recovery': 120,
                'cooldown_duration': 300
            },
            '6': {
                'structure': '40min Z1-Z2 easy, 5x30sec @ 120% FTP with 2min easy, 5min Z1 cooldown',
                'execution': 'Full openers session - extended base with sharp activation',
                'openers': True,
                'warmup_duration': 2400,
                'warmup_power': 0.65,
                'efforts': (5, 30),
                'effort_power': 1.20,
                'effort_recovery': 120,
                'cooldown_duration': 300
            }
        }
    },
    {
        'name': 'Terrain Simulation Z2',
        'levels': {
            '1': {
                'structure': '1.5hr Z2 with variable power: alternate 5min @ 70% / 5min @ 75% FTP throughout',
                'execution': 'Simulates rolling terrain - variable power within Z2',
                'cadence_prescription': '80-90rpm on "climbs", 90-100rpm on "descents"',
                'position_prescription': 'Vary between hoods and drops',
                'timing_prescription': 'Endurance day',
                'fueling': '60g CHO/hr',
                'terrain_sim': True,
                'duration': 5400,
                'low_power': 0.70,
                'high_power': 0.75,
                'segment_duration': 300
            },
            '2': {
                'structure': '2hr Z2 with variable power: alternate 5min @ 68% / 5min @ 77% FTP throughout',
                'execution': 'Extended duration with more variability',
                'terrain_sim': True,
                'duration': 7200,
                'low_power': 0.68,
                'high_power': 0.77,
                'segment_duration': 300
            },
            '3': {
                'structure': '2.5hr Z2 with variable power: alternate 4min @ 67% / 6min @ 78% FTP throughout',
                'execution': 'Uneven segments - longer "climbs"',
                'terrain_sim': True,
                'duration': 9000,
                'low_power': 0.67,
                'high_power': 0.78,
                'segment_duration_low': 240,
                'segment_duration_high': 360
            },
            '4': {
                'structure': '3hr Z2 with variable power: random 3-7min segments @ 65-80% FTP',
                'execution': 'Random variability - gravel race simulation',
                'terrain_sim': True,
                'duration': 10800,
                'power_range': (0.65, 0.80),
                'segment_range': (180, 420)
            },
            '5': {
                'structure': '3.5hr Z2 with variable power: random 3-8min segments @ 63-82% FTP',
                'execution': 'Extended random variability - race-realistic',
                'terrain_sim': True,
                'duration': 12600,
                'power_range': (0.63, 0.82),
                'segment_range': (180, 480)
            },
            '6': {
                'structure': '4hr Z2 with variable power: random 3-10min segments @ 60-85% FTP',
                'execution': 'Maximum duration with full variability range',
                'terrain_sim': True,
                'duration': 14400,
                'power_range': (0.60, 0.85),
                'segment_range': (180, 600)
            }
        }
    }
]


# =============================================================================
# RACE SIMULATION (NEW CATEGORY)
# =============================================================================

RACE_SIMULATION = [
    {
        'name': 'Breakaway Simulation',
        'levels': {
            '1': {
                'structure': '15min warmup Z2, 2x (5min @ 110% FTP attack + 10min @ 88% FTP tempo hold), 5min recovery between',
                'execution': 'Learning the format - attack then hold. This is breakaway work',
                'cadence_prescription': '95-105rpm attack, 85-95rpm hold',
                'position_prescription': 'Out of saddle for attack start, seated for hold',
                'timing_prescription': 'Fresh',
                'fueling': '60-70g CHO/hr',
                'breakaway': True,
                'intervals': 2,
                'attack_duration': 300,
                'attack_power': 1.10,
                'hold_duration': 600,
                'hold_power': 0.88,
                'recovery_duration': 300
            },
            '2': {
                'structure': '15min warmup Z2, 2x (5min @ 112% FTP attack + 12min @ 88% FTP tempo hold), 5min recovery between',
                'execution': 'Extended hold duration - sustaining the break',
                'breakaway': True,
                'intervals': 2,
                'attack_duration': 300,
                'attack_power': 1.12,
                'hold_duration': 720,
                'hold_power': 0.88,
                'recovery_duration': 300
            },
            '3': {
                'structure': '15min warmup Z2, 3x (5min @ 112% FTP attack + 10min @ 89% FTP tempo hold), 4min recovery between',
                'execution': 'Three breakaway attempts - race-realistic',
                'breakaway': True,
                'intervals': 3,
                'attack_duration': 300,
                'attack_power': 1.12,
                'hold_duration': 600,
                'hold_power': 0.89,
                'recovery_duration': 240
            },
            '4': {
                'structure': '15min warmup Z2, 3x (5min @ 115% FTP attack + 12min @ 90% FTP tempo hold), 4min recovery between',
                'execution': 'Increased intensity - harder attack, higher hold',
                'breakaway': True,
                'intervals': 3,
                'attack_duration': 300,
                'attack_power': 1.15,
                'hold_duration': 720,
                'hold_power': 0.90,
                'recovery_duration': 240
            },
            '5': {
                'structure': '15min warmup Z2, 3x (5min @ 115% FTP attack + 15min @ 90% FTP tempo hold), 3min recovery between',
                'execution': 'Extended hold with reduced recovery - race simulation',
                'breakaway': True,
                'intervals': 3,
                'attack_duration': 300,
                'attack_power': 1.15,
                'hold_duration': 900,
                'hold_power': 0.90,
                'recovery_duration': 180
            },
            '6': {
                'structure': '15min warmup Z2, 4x (5min @ 118% FTP attack + 12min @ 91% FTP tempo hold), 3min recovery between',
                'execution': 'Maximum development - 4 breakaway attempts, G-Spot holds',
                'breakaway': True,
                'intervals': 4,
                'attack_duration': 300,
                'attack_power': 1.18,
                'hold_duration': 720,
                'hold_power': 0.91,
                'recovery_duration': 180
            }
        }
    },
    {
        'name': 'Variable Pace Chaos',
        'levels': {
            '1': {
                'structure': '15min warmup Z2, 20min block: random 30sec-2min efforts @ 85-110% FTP, no pattern',
                'execution': 'Gravel race simulation - unpredictable power changes',
                'cadence_prescription': 'Variable - respond to terrain',
                'position_prescription': 'Change positions frequently',
                'timing_prescription': 'Fresh',
                'fueling': '60-70g CHO/hr',
                'chaos': True,
                'block_duration': 1200,
                'power_range': (0.85, 1.10),
                'effort_range': (30, 120)
            },
            '2': {
                'structure': '15min warmup Z2, 25min block: random 30sec-2min efforts @ 83-112% FTP, no pattern',
                'execution': 'Extended chaos block - wider power range',
                'chaos': True,
                'block_duration': 1500,
                'power_range': (0.83, 1.12),
                'effort_range': (30, 120)
            },
            '3': {
                'structure': '15min warmup Z2, 2x15min blocks: random 30sec-2min efforts @ 80-115% FTP, 5min Z2 between',
                'execution': 'Two chaos blocks - recovery between',
                'chaos': True,
                'blocks': 2,
                'block_duration': 900,
                'power_range': (0.80, 1.15),
                'effort_range': (30, 120),
                'block_recovery': 300
            },
            '4': {
                'structure': '15min warmup Z2, 2x20min blocks: random 30sec-3min efforts @ 78-118% FTP, 5min Z2 between',
                'execution': 'Extended blocks with wider effort range',
                'chaos': True,
                'blocks': 2,
                'block_duration': 1200,
                'power_range': (0.78, 1.18),
                'effort_range': (30, 180),
                'block_recovery': 300
            },
            '5': {
                'structure': '15min warmup Z2, 3x15min blocks: random 30sec-3min efforts @ 75-120% FTP, 4min Z2 between',
                'execution': 'Three chaos blocks - race simulation',
                'chaos': True,
                'blocks': 3,
                'block_duration': 900,
                'power_range': (0.75, 1.20),
                'effort_range': (30, 180),
                'block_recovery': 240
            },
            '6': {
                'structure': '15min warmup Z2, 45min continuous: random 30sec-4min efforts @ 70-125% FTP, no breaks',
                'execution': 'Maximum chaos - 45min of unpredictable power',
                'chaos': True,
                'block_duration': 2700,
                'power_range': (0.70, 1.25),
                'effort_range': (30, 240)
            }
        }
    },
    {
        'name': 'Sector Simulation',
        'levels': {
            '1': {
                'structure': '15min warmup Z2, 4x (90sec @ 130% FTP sector + 3min @ 75% FTP recovery), 5min Z2 between sets of 2',
                'execution': 'Simulates gravel sectors - hard start, recovery, repeat',
                'cadence_prescription': '100-110rpm sectors, 85-95rpm recovery',
                'position_prescription': 'Out of saddle sector start',
                'timing_prescription': 'Fresh',
                'fueling': '60-70g CHO/hr',
                'sector_sim': True,
                'sectors_per_set': 2,
                'sets': 2,
                'sector_duration': 90,
                'sector_power': 1.30,
                'sector_recovery': 180,
                'sector_recovery_power': 0.75,
                'set_recovery': 300
            },
            '2': {
                'structure': '15min warmup Z2, 6x (90sec @ 130% FTP sector + 3min @ 75% FTP recovery), 5min Z2 between sets of 3',
                'execution': 'More sectors per set - building repeatability',
                'sector_sim': True,
                'sectors_per_set': 3,
                'sets': 2,
                'sector_duration': 90,
                'sector_power': 1.30,
                'sector_recovery': 180,
                'sector_recovery_power': 0.75,
                'set_recovery': 300
            },
            '3': {
                'structure': '15min warmup Z2, 6x (2min @ 125% FTP sector + 3min @ 77% FTP recovery), 4min Z2 between sets of 3',
                'execution': 'Extended sectors - longer hard efforts',
                'sector_sim': True,
                'sectors_per_set': 3,
                'sets': 2,
                'sector_duration': 120,
                'sector_power': 1.25,
                'sector_recovery': 180,
                'sector_recovery_power': 0.77,
                'set_recovery': 240
            },
            '4': {
                'structure': '15min warmup Z2, 8x (2min @ 125% FTP sector + 2.5min @ 78% FTP recovery), 4min Z2 between sets of 4',
                'execution': 'Four sectors per set, reduced recovery',
                'sector_sim': True,
                'sectors_per_set': 4,
                'sets': 2,
                'sector_duration': 120,
                'sector_power': 1.25,
                'sector_recovery': 150,
                'sector_recovery_power': 0.78,
                'set_recovery': 240
            },
            '5': {
                'structure': '15min warmup Z2, 9x (2min @ 128% FTP sector + 2.5min @ 80% FTP recovery), 3min Z2 between sets of 3',
                'execution': 'Three sets of three - race simulation',
                'sector_sim': True,
                'sectors_per_set': 3,
                'sets': 3,
                'sector_duration': 120,
                'sector_power': 1.28,
                'sector_recovery': 150,
                'sector_recovery_power': 0.80,
                'set_recovery': 180
            },
            '6': {
                'structure': '15min warmup Z2, 12x (2min @ 130% FTP sector + 2min @ 80% FTP recovery), 3min Z2 between sets of 4',
                'execution': 'Maximum development - 12 sectors, minimal recovery',
                'sector_sim': True,
                'sectors_per_set': 4,
                'sets': 3,
                'sector_duration': 120,
                'sector_power': 1.30,
                'sector_recovery': 120,
                'sector_recovery_power': 0.80,
                'set_recovery': 180
            }
        }
    }
]


# =============================================================================
# COMBINED DICTIONARY FOR INTEGRATION
# =============================================================================

NEW_ARCHETYPES = {
    'VO2max': VO2MAX_NEW,
    'TT_Threshold': THRESHOLD_NEW,
    'Sprint_Neuromuscular': SPRINT_NEW,
    'Anaerobic_Capacity': ANAEROBIC_CAPACITY,  # NEW CATEGORY
    'Durability': DURABILITY_NEW,
    'Endurance': ENDURANCE_NEW,
    'Race_Simulation': RACE_SIMULATION  # NEW CATEGORY
}


if __name__ == '__main__':
    # Print summary of new archetypes
    print("NEW ARCHETYPES SUMMARY")
    print("=" * 60)

    total_archetypes = 0
    for category, archetypes in NEW_ARCHETYPES.items():
        print(f"\n{category}: {len(archetypes)} new archetypes")
        for arch in archetypes:
            print(f"  - {arch['name']} (6 levels)")
            total_archetypes += 1

    print(f"\n{'=' * 60}")
    print(f"TOTAL: {total_archetypes} new archetypes")
    print(f"TOTAL WORKOUT VARIATIONS: {total_archetypes * 6}")
