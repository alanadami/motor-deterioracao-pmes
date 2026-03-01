import pandas as pd
from config import PERSIST_WINDOW
from core.utils import (
    proportion_below,
    max_consecutive_below,
    normalize_sequence,
    clamp,
)
from core.baseline import calculate_recent_mean
from core.utils import to_native


def calculate_ibe(df: pd.DataFrame, baseline_caixa: float):
    """
    Calcula IBE - Indicador de Erosão de Buffers.
    
    Mede redução relativa do caixa recente em relação ao histórico
    + persistência abaixo da mediana.
    
    Não possui override.
    """

    # ==========================
    # 1️⃣ Redução Relativa (RR)
    # ==========================

    media_recente = calculate_recent_mean(df["caixa"])

    if baseline_caixa <= 0:
        rr_norm = 0.0
    else:
        rr = (baseline_caixa - media_recente) / baseline_caixa
        rr_norm = clamp(rr)

    # ==========================
    # 2️⃣ Persistência abaixo da mediana
    # ==========================

    recent = df["caixa"].tail(PERSIST_WINDOW)

    dn = proportion_below(recent, baseline_caixa)
    seq = max_consecutive_below(recent, baseline_caixa)
    sc_norm = normalize_sequence(seq, PERSIST_WINDOW)

    pr = (dn + sc_norm) / 2

    # ==========================
    # 3️⃣ Score final
    # ==========================

    score = clamp((rr_norm + pr) / 2)

    return to_native ({
        "score": float(score),
        "componentes": {
            "RR_norm": float(rr_norm),
            "PR": float(pr),
            "DN": float(dn),
            "sequencia": int(seq),
            "media_recente": float(media_recente),
        },
        "alertas": {},
        "override": False,
    })