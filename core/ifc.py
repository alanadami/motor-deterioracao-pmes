import pandas as pd
from config import PERSIST_WINDOW, COVERAGE_FULL_SCORE, COVERAGE_OVERRIDE
from core.utils import (
    proportion_below,
    max_consecutive_below,
    normalize_sequence,
    clamp,
    to_native,
)
from core.baseline import calculate_recent_mean


def calculate_ifc(df: pd.DataFrame, baseline_caixa: float):
    """
    Calcula IFC - Indicador de Fragilidade de Caixa.

    Mede:
    1) Tendência negativa persistente do caixa
    2) Cobertura atual em meses
    3) Ativa override se liquidez crítica
    """

    # ==========================
    # 1️⃣ Tendência negativa do caixa
    # ==========================

    recent = df["caixa"].tail(PERSIST_WINDOW)

    dn = proportion_below(recent, baseline_caixa)
    seq = max_consecutive_below(recent, baseline_caixa)
    sc_norm = normalize_sequence(seq, PERSIST_WINDOW)

    tnc = (dn + sc_norm) / 2

    # ==========================
    # 2️⃣ Cobertura de liquidez
    # ==========================

    caixa_atual = df["caixa"].iloc[-1]
    custo_medio_recente = calculate_recent_mean(df["custos"])

    if custo_medio_recente <= 0:
        cobertura = 0.0
    else:
        cobertura = caixa_atual / custo_medio_recente

    # Score de cobertura:
    # 0 → cobertura >= COVERAGE_FULL_SCORE
    # 1 → cobertura muito baixa
    cs_score = max(0.0, 1 - (cobertura / COVERAGE_FULL_SCORE))

    # ==========================
    # 3️⃣ Score final IFC
    # ==========================

    score = clamp((tnc + cs_score) / 2)

    # ==========================
    # 4️⃣ Regra de override
    # ==========================

    liquidez_critica = cobertura < COVERAGE_OVERRIDE
    override = liquidez_critica

    # ==========================
    # 5️⃣ Retorno estruturado
    # ==========================

    return to_native({
        "score": float(score),
        "componentes": {
            "DN": float(dn),
            "sequencia": int(seq),
            "SC_norm": float(sc_norm),
            "TNC": float(tnc),
            "cobertura_meses": float(cobertura),
            "CS_score": float(cs_score),
        },
        "alertas": {
            "liquidez_critica": liquidez_critica
        },
        "override": override,
    })