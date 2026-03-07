import re
import streamlit as st

from config import COVERAGE_OVERRIDE, RECENT_WINDOW, PERSIST_WINDOW
from charts.ipr import plot_ipr
from charts.ipm import plot_ipm
from charts.ifc import plot_ifc
from charts.ibe import plot_ibe
from charts.margem_receita import plot_margem_receita
from charts.caixa_custos import plot_caixa_custos

st.set_page_config(page_title="Indicadores - EWS-PME", layout="centered")

if not st.session_state.get("authorized", False):
    st.warning("É necessário realizar a identificação na página inicial.")
    st.stop()

if "df" not in st.session_state:
    st.warning("Nenhuma análise disponível. Gere a análise antes de abrir esta página.")
    st.stop()

df = st.session_state.df.copy()
payload = st.session_state.get("payload", {})
baselines = payload.get("baselines", {})

baseline_receita = baselines.get("baseline_receita", df["receita"].median())
baseline_margem = baselines.get("baseline_margem", (df["receita"] - df["custos"]).median())
baseline_caixa = baselines.get("baseline_caixa", df["caixa"].median())

def _to_float(value):
    if isinstance(value, (int, float)):
        return float(value)
    if value is None:
        return 0.0
    text = str(value)
    text = text.replace("R$", "").replace(" ", "")
    text = re.sub(r"[^\d,\.-]", "", text)
    if "," in text and "." in text:
        text = text.replace(",", "")
    elif "," in text and "." not in text:
        text = text.replace(",", ".")
    try:
        return float(text)
    except ValueError:
        return 0.0

baseline_receita = _to_float(baseline_receita)
baseline_margem = _to_float(baseline_margem)
baseline_caixa = _to_float(baseline_caixa)

def _format_currency(value):
    sign = "-" if value < 0 else ""
    value = abs(value)
    text = f"{value:,.0f}"
    text = text.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{sign}R$ {text}"

df = df.sort_values("data")
df["margem"] = df["receita"] - df["custos"]

st.title("Gráficos dos Indicadores")
st.caption("Visualize os indicadores em série temporal e seus baselines.")

st.subheader("IPR — Receita vs Baseline")
st.plotly_chart(
    plot_ipr(
        df,
        baseline_receita,
        baseline_label=f"Baseline: {_format_currency(baseline_receita)}",
        last_n=PERSIST_WINDOW,
    ),
    use_container_width=True,
)

st.subheader("IPM — Margem vs Baseline")
st.plotly_chart(
    plot_ipm(
        df,
        baseline_margem,
        baseline_label=f"Baseline: {_format_currency(baseline_margem)}",
        last_n=PERSIST_WINDOW,
    ),
    use_container_width=True,
)

st.subheader("IFC — Cobertura de Caixa (meses)")
st.plotly_chart(
    plot_ifc(
        df,
        COVERAGE_OVERRIDE,
        RECENT_WINDOW,
        baseline_label=f"Mín. estrutural: {COVERAGE_OVERRIDE:.1f}m",
        last_n=PERSIST_WINDOW,
    ),
    use_container_width=True,
)

st.subheader("IBE — Caixa vs Baseline")
st.plotly_chart(
    plot_ibe(
        df,
        baseline_caixa,
        baseline_label=f"Baseline: {_format_currency(baseline_caixa)}",
        last_n=PERSIST_WINDOW,
    ),
    use_container_width=True,
)

st.subheader("Margem vs Receita")
st.plotly_chart(
    plot_margem_receita(
        df,
        last_n=PERSIST_WINDOW,
    ),
    use_container_width=True,
)

st.subheader("Caixa vs Custos Médios")
st.plotly_chart(
    plot_caixa_custos(
        df,
        RECENT_WINDOW,
        last_n=PERSIST_WINDOW,
    ),
    use_container_width=True,
)
