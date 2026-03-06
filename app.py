import re
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
telefone = st.text_input("Telefone")

autorizacao = st.checkbox(
    "Declaro que compreendo o funcionamento da ferramenta e autorizo contato posterior."
)

if st.button("Prosseguir para Análise"):
    erros = []
    if not empresa:
        erros.append("Informe o nome da empresa.")
    if not responsavel:
        erros.append("Informe o responsável.")

    email_ok = bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email or ""))
    if not email_ok:
        erros.append("Informe um e-mail válido.")

    telefone_digitos = re.sub(r"\D", "", telefone or "")
    if len(telefone_digitos) not in (10, 11):
        erros.append("Informe um telefone válido (DDD + número).")

    if not autorizacao:
        erros.append("Confirme a autorização para contato.")

    if erros:
        st.error(" ".join(erros))
    else:
        st.session_state.authorized = True
        st.session_state.empresa = empresa
        st.session_state.responsavel = responsavel
        st.session_state.email = email
        st.session_state.telefone = telefone
        st.success("Identificação confirmada. Acesse a página 'Análise' no menu lateral.")
