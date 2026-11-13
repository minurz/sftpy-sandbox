# average active region flux density (G)
AR_BFIELD = 180.0

# anti-Hale fraction of active regions
BP_FRACTION_ANTI_HALE: float = 0.05 # 0.05

# asymmetry area ratio of leading to following pole spatial concentrations (r_lead / r_follow)^2; bracket 0.6–0.93
ASYM_RATIO: float = 0.8 # 0.8

# degree of randomness in asymmetry ratio, σ of ln(r_lead / r_follow), intrinsic (Yamamoto 2012)
ASYM_SCATTER: float = 0.12 # 0.12

# Flux scale at which asymmetry becomes significant (1e18 Mx per polarity or 2e20 Mx total unsigned)
ASYM_FLUX_FOLD: float = 100

# damping factor for anti-Hale flips, 0.0–1.0, where 1.0 is no damping and 0.0 is complete damping
AH_ASYM_DAMPING: float = 0.5

# power law index of source spectrum for active regions
BP_FLUX_POWER_ACT: float = 1.9

# power law index of source spectrum for ephemeral regions
BP_FLUX_POWER_EPH: float = 2.9

# minimum total flux of active region (10^18 Mx)
BP_FLUX_MIN: int = 12

# maximum total flux of active region (10^18 Mx)
BP_FLUX_MAX: int = 15000

# fraction of ephemeral regions that scale with source
BP_FRACTION_TURBULENT: float = 0.7

# spread in latitude distribution (deg)
BP_LAT_WIDTH: float = 25.0

# e-folding scale in flux for spread in latitude (10^18 Mx)
BP_LAT_FLUX_FOLD: float = 500.0

# Joy's Law Slope (deg)
BP_JOY_SLOPE: float = 0.24

# constant factor added to latitude spread (deg)
BP_LAT_CONST: float = 3.75

# mean equatorward tilt (deg)
# BP_TILT_MEAN: float = 4.2

# spread in equatorward tilt (deg)
BP_TILT_WIDTH: float = 90.0

# spread in anti-Hale tilt (deg)
BP_AH_TILT_WIDTH: float = 35.0

# e-folding scale in flux for spread in tilt (10^18 Mx)4
BP_TILT_FLUX_FOLD: float = 80.0

# constant factor added to joy tilt spread (deg)
BP_TILT_CONST: float = 18.0