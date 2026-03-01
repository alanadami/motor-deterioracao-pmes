from config import HIST_WINDOW_MIN, HIST_WINDOW_MAX
from core.utils import clamp


def calculate_confianca(df):
    """
    Calcula a camada de confiança do modelo.

    Mede:
    - Continuidade informacional
    - Cobertura do histórico
    - Autoridade estrutural mínima
    """

    # 1️⃣ Identificar meses válidos (sem NaN nas 3 variáveis)
    valid_mask = (
        df["receita"].notna() &
        df["custos"].notna() &
        df["caixa"].notna()
    )

    meses_totais = len(df)
    meses_validos = valid_mask.sum()

    # 2️⃣ Calcular maior sequência contínua válida
    max_seq = 0
    current_seq = 0

    for is_valid in valid_mask:
        if is_valid:
            current_seq += 1
            max_seq = max(max_seq, current_seq)
        else:
            current_seq = 0

    # 3️⃣ Determinar autoridade estrutural
    autoridade_estrutural = meses_validos >= HIST_WINDOW_MIN

    # 4️⃣ Se não houver autoridade mínima
    if not autoridade_estrutural:
        return {
            "score": 0.0,
            "status": "Histórico Insuficiente",
            "autoridade_estrutural": False,
            "meses_validos": int(meses_validos),
            "maior_sequencia_continua": int(max_seq)
        }

    # 5️⃣ Índices
    ic = max_seq / HIST_WINDOW_MAX
    ico = meses_validos / HIST_WINDOW_MAX

    score = clamp((ic + ico) / 2)

    # 6️⃣ Classificação qualitativa
    if score >= 0.80:
        status = "Alta"
    elif score >= 0.60:
        status = "Moderada"
    else:
        status = "Baixa"

    return {
        "score": float(score),
        "status": status,
        "autoridade_estrutural": True,
        "meses_validos": int(meses_validos),
        "maior_sequencia_continua": int(max_seq)
    }