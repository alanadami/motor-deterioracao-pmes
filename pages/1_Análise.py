import streamlit as st
import pandas as pd

from core.report import generate_dashboard_payload
from core.confianca import calculate_confianca
from core.ipr import calculate_ipr
from core.ipm import calculate_ipm
from core.ifc import calculate_ifc
from core.ibe import calculate_ibe
from core.isg import calculate_isg
from core.baseline import validate_minimum_history, calculate_historical_median

st.title("Análise Financeira")

if not st.session_state.get("authorized", False):
    st.warning("É necessário realizar a identificação na página inicial.")
    st.stop()

st.markdown("### Modelo de CSV")

modelo_csv = """data,receita,custos,caixa
2023-01,100000,80000,150000
2023-02,110000,85000,140000
"""

st.download_button(
    "Baixar modelo CSV",
    data=modelo_csv,
    file_name="modelo_ews_pme.csv",
    mime="text/csv"
)

uploaded_file = st.file_uploader("Envie o CSV da empresa", type="csv")

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    df["data"] = pd.to_datetime(df["data"])
    df = df.sort_values("data")

    validate_minimum_history(df)

    df["margem"] = df["receita"] - df["custos"]

    # Baselines
    baseline_receita = calculate_historical_median(df["receita"])
    baseline_margem = calculate_historical_median(df["margem"])
    baseline_caixa = calculate_historical_median(df["caixa"])

    # Indicadores
    ipr_result = calculate_ipr(df, baseline_receita)
    ipm_result = calculate_ipm(df, baseline_margem)
    ifc_result = calculate_ifc(df, baseline_caixa)
    ibe_result = calculate_ibe(df, baseline_caixa)

    confianca_result = calculate_confianca(df)

    isg_result = calculate_isg(
        ipr_result,
        ipm_result,
        ifc_result,
        ibe_result,
        confianca_result
    )

    payload = generate_dashboard_payload(
        ipr_result,
        ipm_result,
        ifc_result,
        ibe_result,
        isg_result,
        confianca_result,
        baselines={
            "baseline_receita": baseline_receita,
            "baseline_margem": baseline_margem,
            "baseline_caixa": baseline_caixa,
        }
    )

    st.session_state.payload = payload

    st.success("Análise concluída.")

    st.json(payload)
