import pandas as pd
from config import PERSIST_WINDOW
from core.utils import (
    proportion_below,
    max_consecutive_below,
    normalize_sequence,
)


def calculate_ipr(df: pd.DataFrame, baseline_receita: float):
    """
    Calcula IPR - Indicador de Persistência da Receita.
    Mede deterioração persistente recente em relação ao baseline histórico.
    """

    # 1️⃣ Selecionar janela recente de persistência
    recent = df["receita"].tail(PERSIST_WINDOW)

    # 2️⃣ Calcular proporção abaixo da mediana (DN)
    dn = proportion_below(recent, baseline_receita)

    # 3️⃣ Calcular maior sequência consecutiva abaixo da mediana
    seq = max_consecutive_below(recent, baseline_receita)

    # 4️⃣ Normalizar sequência
    sc_norm = normalize_sequence(seq, PERSIST_WINDOW)

    # 5️⃣ Score final
    score = (dn + sc_norm) / 2

    return {
        "score": score,
        "componentes": {
            "DN": dn,
            "sequencia": seq,
            "SC_norm": sc_norm,
        },
        "alertas": {},
        "override": False,
    }