import re
import streamlit as st
from PIL import Image


st.set_page_config(
    page_title="EWS-PME",
    page_icon="📊",
    layout="centered"
)

if "authorized" not in st.session_state:
    st.session_state.authorized = True


logo = Image.open("assets/logo.png")
st.image(logo, width=300)

st.title("📊 Motor de Monitoramento de Deterioração de Negócios (EWS-PME)")

st.markdown("""
Ferramenta online para identificação de sinais estruturais de deterioração financeira em pequenas e médias empresas.

### O que o sistema faz
- Analisa receita, custos e caixa.
- Mede persistência de deterioração.
- Prioriza liquidez e sustentabilidade estrutural.
- Gera diagnóstico executivo estruturado.

### O que o sistema não faz
- Não prevê falência.
- Não realiza valuation.
- Não substitui consultoria contábil.
- Não armazena dados financeiros enviados.

### Requisitos mínimos
- Pelo menos 12 meses de dados mensais.
- Arquivo CSV com colunas obrigatórias:
    - data (YYYY-MM)
    - receita
    - custos
    - caixa
""")

st.markdown("### Envie sua opinião")
st.markdown(
    "Quer aprofundar nos relatórios ou deixar feedback? "
    "Envie um email para **galves.alan@gmail.com**."
)
st.info("Acesse a página 'Análise' no menu lateral para iniciar.")
