from core.utils import format_for_display


def generate_dashboard_payload(
    ipr_result,
    ipm_result,
    ifc_result,
    ibe_result,
    isg_result,
    confianca_result,
    baselines=None
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
        },

        "tecnico": {
            "IPR": {
                "score": ipr_result["score"],
                "componentes": ipr_result.get("componentes", {}),
                "alertas": ipr_result.get("alertas", {}),
                "override": ipr_result.get("override", False),
            },
            "IPM": {
                "score": ipm_result["score"],
                "componentes": ipm_result.get("componentes", {}),
                "alertas": ipm_result.get("alertas", {}),
                "override": ipm_result.get("override", False),
            },
            "IFC": {
                "score": ifc_result["score"],
                "componentes": ifc_result.get("componentes", {}),
                "alertas": ifc_result.get("alertas", {}),
                "override": ifc_result.get("override", False),
            },
            "IBE": {
                "score": ibe_result["score"],
                "componentes": ibe_result.get("componentes", {}),
                "alertas": ibe_result.get("alertas", {}),
                "override": ibe_result.get("override", False),
            },
            "ISG": {
                "componentes": isg_result.get("componentes", {}),
                "autoridade_estrutural": isg_result.get("autoridade_estrutural"),
                "override_ativo": isg_result.get("override_ativo"),
            },
        },
    }

    if baselines:
        payload["baselines"] = baselines

    return format_for_display(payload)
