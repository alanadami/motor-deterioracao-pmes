import pandas as pd
from config import PERSIST_WINDOW
from core.utils import (
    proportion_below,
    max_consecutive_below,
    normalize_sequence,
    clamp,
    to_native,
)
from core.baseline import calculate_recent_mean


def calculate_ipm(df: pd.DataFrame, baseline_margem: float):
    """
    IPM — Indicador de Persistência da Margem

    Mede:
    1) Persistência negativa da margem em relação ao baseline
    2) Intensidade estrutural via sequência
    3) Penalização proporcional caso margem média recente seja negativa

    Escala final: 0 (saudável) → 1 (deterioração máxima)
    """

    # ==========================
    # 1️⃣ Janela recente
    # ==========================

    recent = df["margem"].tail(PERSIST_WINDOW)

    # ==========================
    # 2️⃣ Componentes estruturais
    # ==========================

    dn = proportion_below(recent, baseline_margem)
    seq = max_consecutive_below(recent, baseline_margem)
    sc_norm = normalize_sequence(seq, PERSIST_WINDOW)

    ipm_base = (dn + sc_norm) / 2

    # ==========================
    # 3️⃣ Intensidade recente
    # ==========================

    media_recente = calculate_recent_mean(df["margem"])
    penalizacao = 0.0
    alerta_prejuizo = False

    if media_recente < 0:
        alerta_prejuizo = True

        # penalização só se baseline for positivo
        if baseline_margem > 0:
            penalizacao = min(1.0, abs(media_recente) / baseline_margem)
        else:
            penalizacao = 1.0  # já está estruturalmente negativa

    print("Média recente margem:", media_recente)
    print("Baseline margem:", baseline_margem)

    # ==========================
    # 4️⃣ Score Final
    # ==========================

    # Soma estrutural + intensidade
    score = clamp(ipm_base + penalizacao)

    # ==========================
    # 5️⃣ Retorno
    # ==========================

    return to_native({
        "score": float(score),
        "componentes": {
            "DN": float(dn),
            "sequencia": int(seq),
            "SC_norm": float(sc_norm),
            "ipm_base": float(ipm_base),
            "margem_media_recente": float(media_recente),
            "penalizacao": float(penalizacao),
        },
        "alertas": {
            "prejuizo_recente": alerta_prejuizo
        },
        "override": False,
    })

    
