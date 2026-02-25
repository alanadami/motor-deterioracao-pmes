import pandas as pd
from config import PERSIST_WINDOW
from core.utils import (
    proportion_below,
    max_consecutive_below,
    normalize_sequence,
    clamp,
)
from core.baseline import calculate_recent_mean


def calculate_ipm(df: pd.DataFrame, baseline_margem: float):
    """
    Calcula IPM - Indicador de Persistência da Margem.
    
    Mede deterioração persistente da margem em relação ao baseline histórico.
    Aplica penalização proporcional caso a média recente esteja negativa.
    Não possui override.
    """

    # 1️⃣ Selecionar janela recente de persistência
    recent = df["margem"].tail(PERSIST_WINDOW)

    # 2️⃣ Calcular proporção abaixo da mediana histórica (DN)
    dn = proportion_below(recent, baseline_margem)

    # 3️⃣ Calcular maior sequência consecutiva abaixo da mediana
    seq = max_consecutive_below(recent, baseline_margem)

    # 4️⃣ Normalizar sequência
    sc_norm = normalize_sequence(seq, PERSIST_WINDOW)

    # 5️⃣ Score base (mesma lógica do IPR)
    ipm_base = (dn + sc_norm) / 2

    # 6️⃣ Calcular média recente da margem
    media_recente = calculate_recent_mean(df["margem"])

    penalizacao = 0.0
    alerta_prejuizo = False

    # 7️⃣ Aplicar penalização se média recente for negativa
    if baseline_margem > 0 and media_recente < 0:
        penalizacao = min(1.0, abs(media_recente) / baseline_margem)
        alerta_prejuizo = True

    # 8️⃣ Score final com modulação ponderada
    score = clamp(0.7 * ipm_base + 0.3 * penalizacao)
    return {
        "score": float(score),
        "componentes": {
            "DN": float(dn),
            "sequencia": int(seq),
            "SC_norm": float(sc_norm),
            "ipm_base": float(ipm_base),
            "media_recente": float(media_recente),
            "penalizacao": float(penalizacao),
        },
        "alertas": {
            "prejuizo_recorrente": alerta_prejuizo
        },
        "override": False,
    }