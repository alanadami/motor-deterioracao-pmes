import streamlit as st
from PIL import Image


st.set_page_config(
    page_title="EWS-PME",
    page_icon="📊",
    layout="centered"
)

if "authorized" not in st.session_state:
    st.session_state.authorized = False


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

st.markdown("### Identificação para geração do relatório")

empresa = st.text_input("Nome da empresa")
responsavel = st.text_input("Responsável")
email = st.text_input("Email para contato")

autorizacao = st.checkbox(
    "Declaro que compreendo o funcionamento da ferramenta e autorizo contato posterior."
)

if st.button("Prosseguir para Análise"):
    if empresa and responsavel and email and autorizacao:
        st.session_state.authorized = True
        st.session_state.empresa = empresa
        st.session_state.responsavel = responsavel
        st.session_state.email = email
        st.success("Identificação confirmada. Acesse a página 'Análise' no menu lateral.")
    else:
        st.error("Preencha todos os campos e confirme autorização.")