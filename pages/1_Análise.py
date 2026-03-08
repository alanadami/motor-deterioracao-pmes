import io
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

st.markdown("### Usar exemplo")

exemplo_csv = """data,receita,custos,caixa
2023-01,95000,78000,40000
2023-02,97000,79000,43000
2023-03,98000,80000,46000
2023-04,99000,81000,49000
2023-05,100000,82000,52000
2023-06,101000,83000,55000
2023-07,85000,90000,50000
2023-08,83000,91000,44000
2023-09,87000,89000,42000
2023-10,95000,82000,46000
2023-11,98000,83000,50000
2023-12,100000,84000,54000
2024-01,102000,85000,58000
2024-02,103000,86000,62000
2024-03,105000,87000,66000
2024-04,106000,88000,70000
2024-05,108000,89000,74000
2024-06,110000,90000,78000
"""

if "use_example" not in st.session_state:
    st.session_state.use_example = False

col_a, col_b = st.columns(2)
with col_a:
    if st.button("Usar exemplo"):
        st.session_state.use_example = True
with col_b:
    if st.button("Limpar exemplo"):
        st.session_state.use_example = False

uploaded_file = st.file_uploader("Envie o CSV da empresa", type="csv")

if uploaded_file:
    st.session_state.use_example = False
    df = pd.read_csv(uploaded_file)
elif st.session_state.use_example:
    df = pd.read_csv(io.StringIO(exemplo_csv))
else:
    df = None

if df is not None:

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
    st.session_state.df = df.copy()

    st.success("Análise concluída.")

    st.json(payload)
