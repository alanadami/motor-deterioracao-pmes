from core.utils import format_for_display


def generate_dashboard_payload(
    ipr_result,
    ipm_result,
    ifc_result,
    ibe_result,
    isg_result,
    confianca_result
):
    """
    Consolida todos os resultados em payload único para UI.
    """

    payload = {
        "resumo_executivo": {
            "classificacao": isg_result["classificacao"],
            "score_tecnico": isg_result["score_tecnico"],
            "confianca": isg_result["confianca"],
            "autoridade_estrutural": isg_result["autoridade_estrutural"],
            "override_liquidez": isg_result["override_ativo"],
        },

        "indicadores": {
            "IPR": ipr_result["score"],
            "IPM": ipm_result["score"],
            "IFC": ifc_result["score"],
            "IBE": ibe_result["score"],
        },

        # 🔥 CORREÇÃO AQUI
        "alertas": isg_result["alertas"],

        "confianca_detalhe": {
            "status": confianca_result["status"],
            "meses_validos": confianca_result["meses_validos"],
            "maior_sequencia_continua": confianca_result["maior_sequencia_continua"],
        }
    }

    return format_for_display(payload)