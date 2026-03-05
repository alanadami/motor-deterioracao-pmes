import streamlit as st
from PIL import Image

from core.pdf_report import build_pdf

st.set_page_config(page_title="Relatório EWS-PME", layout="centered")

if "payload" not in st.session_state:
    st.warning("Nenhuma análise disponível.")
    st.stop()

payload = st.session_state.payload
resumo = payload["resumo_executivo"]
indicadores = payload["indicadores"]
alertas = payload["alertas"]
confianca = payload["confianca_detalhe"]

meta = {
    "empresa": st.session_state.get("empresa"),
    "responsavel": st.session_state.get("responsavel"),
    "email": st.session_state.get("email"),
}
pdf_bytes = build_pdf(payload, meta=meta)
st.download_button(
    "Baixar PDF",
    data=pdf_bytes,
    file_name="relatorio_ews_pme.pdf",
    mime="application/pdf",
)

# =========================
# HELPERS DE COR
# =========================

def interpolate_color(value):
    """
    Interpola entre azul (#1877F2) e vermelho (#e63946) com base no valor (0–1).
    0 = azul puro, 1 = vermelho puro.
    Retorna (hex_color, top_gradient, text_color_class).
    """
    v = max(0.0, min(1.0, float(value)))
    # RGB azul
    r1, g1, b1 = 24, 119, 242
    # RGB vermelho
    r2, g2, b2 = 230, 57, 70
    r = int(r1 + (r2 - r1) * v)
    g = int(g1 + (g2 - g1) * v)
    b = int(b1 + (b2 - b1) * v)
    hex_color = f"#{r:02x}{g:02x}{b:02x}"
    # gradiente da barra superior
    r_lt = min(255, r + 40)
    g_lt = min(255, g + 40)
    b_lt = min(255, b + 40)
    hex_lt = f"#{r_lt:02x}{g_lt:02x}{b_lt:02x}"
    gradient = f"linear-gradient(90deg, {hex_color}, {hex_lt})"
    return hex_color, gradient

def score_ring_color(value):
    """Cor do anel do score: 0=azul, 1=vermelho."""
    return interpolate_color(value)[0]

def is_saudavel_classificacao(value):
    text = str(value).strip().lower()
    normalized = (
        text.replace("á", "a")
            .replace("à", "a")
            .replace("â", "a")
            .replace("ã", "a")
            .replace("ç", "c")
            .replace("é", "e")
            .replace("ê", "e")
            .replace("í", "i")
            .replace("ó", "o")
            .replace("ô", "o")
            .replace("õ", "o")
            .replace("ú", "u")
    )
    return "saudavel" in normalized

def score_to_level(value):
    v = max(0.0, min(1.0, float(value)))
    if v >= 0.75:
        return "Nível crítico"
    if v >= 0.56:
        return "Enfraquecimento"
    if v >= 0.31:
        return "Atenção"
    return "Estável"

# =========================
# ESTILOS
# =========================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: #1C1E21;
}

.main > div {
    max-width: 900px;
    margin: auto;
    padding: 32px 16px;
    background: #F5F7FA;
}

/* ── HEADER ── */
.header-wrapper {
    display: flex;
    align-items: stretch;
    gap: 16px;
    margin-bottom: 24px;
}
.header-logo-box {
    background: #FFFFFF;
    border: 1px solid #e4e6eb;
    border-radius: 16px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 16px;
    flex-shrink: 0;
}
.header-logo-box img {
    width: 120px;
    height: auto;
}
.header-title-box {
    background: #FFFFFF;
    border: 1px solid #e4e6eb;
    border-radius: 16px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    flex: 1;
    padding: 20px 24px;
}
.header-title { font-size: 22px; font-weight: 800; letter-spacing: -0.02em; color: #1C1E21; }
.header-ts    { font-family: 'DM Mono', monospace; font-size: 11px; color: #8a8d91; margin-top: 4px; }

/* fallback logo (sem imagem) */
.header-logo-fallback {
    width: 46px; height: 46px;
    background: linear-gradient(135deg, #1877F2, #0d5cc7);
    border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 17px; font-weight: 800; color: #fff;
    box-shadow: 0 4px 14px rgba(24,119,242,0.35);
}
.header-brand-name { font-size: 15px; font-weight: 700; color: #1C1E21; }
.header-brand-sub  { font-size: 11.5px; color: #65676b; }

/* ── SECTION LABEL ── */
.section-label {
    font-size: 10.5px; font-weight: 600;
    letter-spacing: 0.13em; text-transform: uppercase;
    color: #65676b; margin-bottom: 14px; margin-top: 20px;
    display: flex; align-items: center; gap: 8px;
    font-family: 'DM Mono', monospace;
}
.section-label::after { content:''; flex:1; height:1px; background:#e4e6eb; }

/* ── HERO CARDS (Classificação, Score, Confiança) ── */
.hero-card {
    background: #FFFFFF;
    border: 1px solid #e4e6eb;
    border-radius: 16px;
    padding: 24px 20px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    min-height: 190px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    transition: box-shadow 0.2s, transform 0.2s;
}
.hero-card:hover { box-shadow: 0 6px 20px rgba(0,0,0,0.09); transform: translateY(-2px); }

.card-label {
    font-size: 11px; font-weight: 600; text-transform: uppercase;
    letter-spacing: 0.1em; font-family: 'DM Mono', monospace;
    margin-bottom: 12px; width: 100%;
}

/* Classificação */
.card-class {
    background: linear-gradient(140deg, #ebf2ff, #dceafe) !important;
    border-color: rgba(24,119,242,0.18) !important;
}
.card-class .card-label { color: #5a8ad4; text-align: center; }
.status-pill {
    display: inline-flex; align-items: center; gap: 7px;
    border-radius: 100px;
    padding: 5px 12px; font-size: 12px; font-weight: 600; margin-bottom: 10px;
}
.status-pill.ok {
    background: rgba(45,166,95,0.12); border: 1px solid rgba(45,166,95,0.22);
    color: #1a7a4a;
}
.status-pill.danger {
    background: rgba(230,57,70,0.12); border: 1px solid rgba(230,57,70,0.22);
    color: #e63946;
}
.pulse {
    width: 7px; height: 7px; border-radius: 50%;
    display: inline-block;
    animation: pulse 1.6s ease-in-out infinite;
}
.pulse.ok { background: #1a7a4a; }
.pulse.danger { background: #e63946; }
@keyframes pulse {
    0%,100% { opacity:1; transform:scale(1); }
    50%      { opacity:.45; transform:scale(.8); }
}
.class-value { font-size: 28px; font-weight: 800; letter-spacing: -0.02em; }
.class-value.ok { color: #1a7a4a; }
.class-value.danger { color: #e63946; }

/* Score */
.card-score .card-label { color: #5a8ad4; text-align: center; }
.ring-container { position: relative; width: 96px; height: 96px; margin: 4px auto 10px; }
.ring-container svg { transform: rotate(-90deg); width: 96px; height: 96px; }
.ring-bg   { fill: none; stroke: #e4e6eb; stroke-width: 7; }
.ring-fill { fill: none; stroke-width: 7; stroke-linecap: round; stroke-dasharray: 251; }
.ring-val {
    position: absolute; top: 50%; left: 50%; transform: translate(-50%,-50%);
    font-size: 22px; font-weight: 800; letter-spacing: -0.03em;
}
.score-sub { font-size: 12px; color: #65676b; font-weight: 500; }

/* Confiança */
.card-conf {
    background: linear-gradient(140deg, #edfaf3, #d4f0e2) !important;
    border-color: rgba(45,166,95,0.2) !important;
}
.card-conf .card-label { color: #2d7a4f; text-align: center; }
.conf-val { font-size: 44px; font-weight: 800; color: #1a7a4a; letter-spacing: -0.04em; line-height: 1; }
.conf-bar { width: 100%; height: 5px; background: rgba(0,0,0,0.07); border-radius: 3px; margin-top: 14px; overflow: hidden; }
.conf-fill { height: 100%; background: linear-gradient(90deg, #2da65f, #56c98a); border-radius: 3px; }
.conf-tag {
    font-size: 11px; font-weight: 600; color: #1a7a4a;
    background: rgba(45,166,95,0.12); border: 1px solid rgba(45,166,95,0.2);
    border-radius: 100px; padding: 3px 10px; margin-top: 12px; display: inline-block;
}

/* ── INDICATOR CARDS ── */
.ind-card {
    background: #FFFFFF; border: 1px solid #e4e6eb;
    border-radius: 14px; padding: 18px 14px; text-align: center;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04); position: relative; overflow: hidden;
    transition: transform 0.2s, box-shadow 0.2s;
}
.ind-card:hover { transform: translateY(-3px); box-shadow: 0 8px 20px rgba(0,0,0,0.08); }
.ind-card::before { content:''; position:absolute; top:0;left:0;right:0; height:3px; border-radius:14px 14px 0 0; }
.ind-abbr { font-family:'DM Mono',monospace; font-size:10px; color:#8a8d91; letter-spacing:0.1em; margin-bottom:3px; }
.ind-name { font-size:11.5px; color:#65676b; margin-bottom:10px; font-weight:500; }
.ind-val  { font-size:28px; font-weight:800; letter-spacing:-0.03em; line-height:1; }
.ind-bar  { width:100%; height:3px; background:#e4e6eb; border-radius:2px; margin-top:10px; overflow:hidden; }
.ind-fill { height:100%; border-radius:2px; }

/* ── ALERT CARDS ── */
.alert-warn {
    background: #fff8e6; border: 1px solid rgba(230,119,0,0.2);
    border-radius: 14px; padding: 18px 20px;
    display: flex; align-items: flex-start; gap: 12px;
}
.alert-danger {
    background: #fff0f1; border: 1px solid rgba(230,57,70,0.2);
    border-radius: 14px; padding: 18px 20px;
    display: flex; align-items: flex-start; gap: 12px;
}
.alert-ok {
    background: #f0faf4; border: 1px solid rgba(45,166,95,0.2);
    border-radius: 14px; padding: 18px 20px;
    display: flex; align-items: center; gap: 12px;
}
.alert-icon {
    width: 34px; height: 34px; border-radius: 9px;
    display: flex; align-items: center; justify-content: center;
    font-size: 16px; flex-shrink: 0;
}
.alert-warn   .alert-icon { background: rgba(230,119,0,0.12); }
.alert-danger .alert-icon { background: rgba(230,57,70,0.10); }
.alert-ok     .alert-icon { background: rgba(45,166,95,0.12); }
.alert-type {
    font-size:10px; font-weight:700; letter-spacing:0.1em; text-transform:uppercase;
    font-family:'DM Mono',monospace; margin-bottom:3px;
}
.alert-warn   .alert-type { color: #e67700; }
.alert-danger .alert-type { color: #e63946; }
.alert-ok     .alert-type { color: #1a7a4a; }
.alert-text { font-size:13px; font-weight:500; line-height:1.4; color:#1C1E21; }

/* ── HISTORY CARDS ── */
.hist-card {
    background: #FFFFFF; border: 1px solid #e4e6eb;
    border-radius: 14px; padding: 22px 16px; text-align: center;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    height: 140px;
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    transition: transform 0.2s, box-shadow 0.2s;
    position: relative;
}
.hist-card:hover { transform: translateY(-2px); box-shadow: 0 6px 18px rgba(0,0,0,0.08); }
.hist-label { font-size:10.5px; font-weight:600; letter-spacing:0.1em; text-transform:uppercase; color:#65676b; font-family:'DM Mono',monospace; margin-bottom:10px; }
.hist-val   { font-size:32px; font-weight:800; color:#1C1E21; letter-spacing:-0.03em; }
.hist-val.green { color: #1a7a4a; }
.badge-alta {
    display: inline-flex; align-items: center; gap: 5px;
    background: #e6f4ed; border: 1px solid rgba(45,166,95,0.22);
    color: #1a7a4a; border-radius: 100px;
    padding: 4px 12px; font-size: 11px; font-weight: 600;
    position: absolute; bottom: 14px; left: 50%; transform: translateX(-50%);
    white-space: nowrap;
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================

try:
    logo = Image.open("assets/logo.png")
    import base64
    from io import BytesIO
    buf = BytesIO()
    logo.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode()
    logo_html = f"<img src='data:image/png;base64,{b64}' style='width:120px;height:auto;'/>"
except Exception:
    logo_html = """
    <div style='display:flex;flex-direction:column;align-items:center;gap:6px;'>
        <div class='header-logo-fallback'>AA</div>
        <div class='header-brand-name'>Alan Alves</div>
        <div class='header-brand-sub'>Análise e Ciência de Dados</div>
    </div>
    """

st.markdown(f"""
<div class='header-wrapper'>
    <div class='header-logo-box'>
        {logo_html}
    </div>
    <div class='header-title-box'>
        <div class='header-title'>Relatório Executivo</div>
        <div class='header-ts'>Gerado automaticamente · Motor EWS-PME</div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# KPIs — HERO ROW
# =========================

classificacao = resumo["classificacao"]
is_saudavel = is_saudavel_classificacao(classificacao)
status_class = "ok" if is_saudavel else "danger"
has_risco_estrutural = bool(resumo.get("override_liquidez")) or bool(alertas.get("liquidez_critica"))
show_status_pill = has_risco_estrutural and not is_saudavel
status_pill_html = ""
if show_status_pill:
    status_pill_html = f"<div class='status-pill {status_class}'><span class='pulse {status_class}'></span> Sinal Ativo</div>"

col1, col2, col3 = st.columns(3)

with col1:
    class_card_html = "\n".join([
        "<div class='hero-card card-class'>",
        "<div class='card-label'>Classificação</div>",
        status_pill_html,
        f"<div class='class-value {status_class}'>{classificacao}</div>",
        "</div>",
    ])
    st.markdown(class_card_html, unsafe_allow_html=True)

with col2:
    score = float(resumo['score_tecnico'])
    circumference = 251
    offset = circumference * (1 - score)
    ring_color = score_ring_color(score)
    ring_text_color = ring_color
    score_level = score_to_level(score)
    st.markdown(f"""
    <div class='hero-card card-score'>
        <div class='card-label'>Score Técnico</div>
        <div class='ring-container'>
            <svg viewBox='0 0 96 96'>
                <circle class='ring-bg'   cx='48' cy='48' r='40'/>
                <circle class='ring-fill' cx='48' cy='48' r='40'
                    style='stroke:{ring_color};stroke-dashoffset:{offset:.1f};filter:drop-shadow(0 0 5px {ring_color}80);'/>
            </svg>
            <div class='ring-val' style='color:{ring_text_color};'>{resumo['score_tecnico']}</div>
        </div>
        <div class='score-sub'>{score_level}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    conf_pct = int(float(resumo['confianca']) * 100)
    st.markdown(f"""
    <div class='hero-card card-conf'>
        <div class='card-label'>Confiança</div>
        <div class='conf-val'>{resumo['confianca']}</div>
        <div class='conf-bar'>
            <div class='conf-fill' style='width:{conf_pct}%;'></div>
        </div>
        <div class='conf-tag'>✓ Máxima confiança</div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# INDICADORES ESTRUTURAIS
# =========================

st.markdown("<div class='section-label'>Indicadores Estruturais</div>", unsafe_allow_html=True)

indicators = [
    ("IPR", "Receita",  indicadores["IPR"], "Persistência negativa da receita abaixo da mediana histórica."),
    ("IPM", "Margem",   indicadores["IPM"], "Persistência negativa da margem operacional."),
    ("IFC", "Liquidez", indicadores["IFC"], "Fragilidade estrutural do caixa e cobertura de custos."),
    ("IBE", "Buffers",  indicadores["IBE"], "Erosão gradual da proteção de caixa."),
]

cols = st.columns(4)
for i, (abbr, name, value, tooltip) in enumerate(indicators):
    hex_color, gradient = interpolate_color(value)
    bar_w = int(float(value) * 100)
    cols[i].markdown(f"""
    <div class='ind-card' title='{tooltip}'
         style='border-top: 3px solid {hex_color};'>
        <div class='ind-abbr'>{abbr}</div>
        <div class='ind-name'>{name}</div>
        <div class='ind-val' style='color:{hex_color};'>{value}</div>
        <div class='ind-bar'>
            <div class='ind-fill' style='width:{bar_w}%;background:{gradient};'></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# ALERTAS
# =========================

st.markdown("<div class='section-label'>Alertas</div>", unsafe_allow_html=True)

col_a, col_b = st.columns(2)

with col_a:
    if alertas["prejuizo_recente"]:
        st.markdown("""
        <div class='alert-warn'>
            <div class='alert-icon'>⚠️</div>
            <div>
                <div class='alert-type'>Aviso</div>
                <div class='alert-text'>Margem média recente negativa.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class='alert-ok'>
            <div class='alert-icon'>✅</div>
            <div>
                <div class='alert-type'>OK</div>
                <div class='alert-text'>Margem dentro do esperado.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

with col_b:
    if alertas["liquidez_critica"]:
        st.markdown("""
        <div class='alert-danger'>
            <div class='alert-icon'>🔴</div>
            <div>
                <div class='alert-type'>Crítico</div>
                <div class='alert-text'>Liquidez abaixo do nível estrutural mínimo.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class='alert-ok'>
            <div class='alert-icon'>✅</div>
            <div>
                <div class='alert-type'>OK</div>
                <div class='alert-text'>Liquidez dentro do nível estrutural.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def nivel_textual(score):
    if score <= 0.30:
        return "Estável"
    elif score <= 0.55:
        return "Atenção"
    elif score <= 0.75:
        return "Enfraquecimento"
    else:
        return "Nível crítico"

# =========================
# QUALIDADE DO HISTÓRICO
# =========================

st.markdown("<div class='section-label'>Qualidade do Histórico</div>", unsafe_allow_html=True)

colA, colB, colC = st.columns(3)

status_val = confianca['status']
is_alta = str(status_val).lower() == "alta"

colA.markdown(f"""
<div class='hist-card'>
    <div class='hist-label'>Status</div>
    <div class='hist-val {"green" if is_alta else ""}'>{status_val}</div>
    
</div>
""", unsafe_allow_html=True)

colB.markdown(f"""
<div class='hist-card'>
    <div class='hist-label'>Meses Válidos</div>
    <div class='hist-val'>{confianca['meses_validos']}</div>
</div>
""", unsafe_allow_html=True)

colC.markdown(f"""
<div class='hist-card'>
    <div class='hist-label'>Maior Sequência</div>
    <div class='hist-val'>{confianca['maior_sequencia_continua']}</div>
</div>
""", unsafe_allow_html=True)
