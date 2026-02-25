# ==========================
# BASELINES
# ==========================

HIST_WINDOW_MIN = 12
HIST_WINDOW_MAX = 24
PERSIST_WINDOW = 9
RECENT_WINDOW = 6

# ==========================
# IFC - LIQUIDEZ
# ==========================

COVERAGE_FULL_SCORE = 6      # cobertura confortável
COVERAGE_OVERRIDE = 3        # mínimo estrutural

# ==========================
# PESOS ISG
# ==========================

WEIGHTS = {
    "IFC": 0.35,
    "IPM": 0.30,
    "IPR": 0.20,
    "IBE": 0.15
}

# ==========================
# CLASSIFICAÇÃO QUALITATIVA
# ==========================

THRESHOLDS = {
    "SAUDAVEL": 0.30,
    "ATENCAO": 0.55,
    "ENFRAQUECIMENTO": 0.75
}