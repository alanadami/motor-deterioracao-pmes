from config import WEIGHTS, THRESHOLDS
from core.utils import clamp, to_native


def calculate_isg(ipr_result, ipm_result, ifc_result, ibe_result, confianca_result):
    """
    ISG - Indicador de Saúde Geral

    Camadas:
    - Técnica: média ponderada
    - Executiva: classificação + precedência estrutural
    - Consolidação de alertas
    """

    # 1️⃣ Scores individuais
    ipr_score = ipr_result["score"]
    ipm_score = ipm_result["score"]
    ifc_score = ifc_result["score"]
    ibe_score = ibe_result["score"]

    # 2️⃣ Score técnico ponderado
    score_tecnico = clamp(
        WEIGHTS["IPR"] * ipr_score +
        WEIGHTS["IPM"] * ipm_score +
        WEIGHTS["IFC"] * ifc_score +
        WEIGHTS["IBE"] * ibe_score
    )

    # 3️⃣ Classificação por thresholds
    if score_tecnico <= THRESHOLDS["SAUDAVEL"]:
        classificacao = "Saudável"
    elif score_tecnico <= THRESHOLDS["ATENCAO"]:
        classificacao = "Atenção"
    elif score_tecnico <= THRESHOLDS["ENFRAQUECIMENTO"]:
        classificacao = "Enfraquecimento"
    else:
        classificacao = "Deterioração"

    # 4️⃣ Flags estruturais
    override_ativo = ifc_result["override"]
    autoridade_estrutural = confianca_result["autoridade_estrutural"]

    # 5️⃣ Precedência decisória
    if not autoridade_estrutural:
        classificacao = "Diagnóstico Preliminar"
    elif override_ativo:
        classificacao = "Deterioração"

    # 6️⃣ Consolidação de alertas
    alertas_consolidados = {
        "prejuizo_recente": ipm_result["alertas"].get("prejuizo_recente", False),
        "liquidez_critica": ifc_result["alertas"].get("liquidez_critica", False),
    }

    return to_native({
        "score_tecnico": float(score_tecnico),
        "classificacao": classificacao,
        "override_ativo": override_ativo,
        "autoridade_estrutural": autoridade_estrutural,
        "confianca": float(confianca_result["score"]),
        "componentes": {
            "IPR": float(ipr_score),
            "IPM": float(ipm_score),
            "IFC": float(ifc_score),
            "IBE": float(ibe_score),
        },
        "alertas": alertas_consolidados
    })