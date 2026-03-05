from io import BytesIO
import os

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image as RLImage,
)


def build_pdf(payload, meta=None):
    """
    Gera um PDF em memoria com duas paginas:
    1) Resumo do dashboard
    2) Detalhamento tecnico
    """
    meta = meta or {}
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "title_center",
        parent=styles["Title"],
        alignment=1,
    )
    h2_style = ParagraphStyle(
        "h2_center",
        parent=styles["Heading2"],
        alignment=1,
    )
    h3_style = ParagraphStyle(
        "h3_center",
        parent=styles["Heading3"],
        alignment=1,
    )
    small_style = ParagraphStyle(
        "small",
        parent=styles["BodyText"],
        fontSize=9,
        leading=11,
    )

    story = []

    banner = _load_banner("assets/logo_banner.png", max_width=16 * cm)
    if banner:
        story.append(banner)
        story.append(Spacer(1, 10))

    story.append(Paragraph("Relatorio Executivo - EWS-PME", title_style))
    story.append(Spacer(1, 8))

    # Identificacao
    id_rows = []
    if meta.get("empresa"):
        id_rows.append(["Empresa", str(meta["empresa"])])
    if meta.get("responsavel"):
        id_rows.append(["Responsavel", str(meta["responsavel"])])
    if meta.get("email"):
        id_rows.append(["Email", str(meta["email"])])

    if id_rows:
        story.append(Paragraph("Identificacao", h2_style))
        story.append(_make_table(id_rows))
        story.append(Spacer(1, 10))

    resumo = payload.get("resumo_executivo", {})
    indicadores = payload.get("indicadores", {})
    alertas = payload.get("alertas", {})
    confianca = payload.get("confianca_detalhe", {})

    # Resumo executivo
    resumo_rows = [
        ["Classificacao", _v(resumo.get("classificacao"))],
        ["Score Tecnico", _v(resumo.get("score_tecnico"))],
        ["Confianca", _v(resumo.get("confianca"))],
        ["Autoridade Estrutural", _v(resumo.get("autoridade_estrutural"))],
        ["Override Liquidez", _v(resumo.get("override_liquidez"))],
    ]
    story.append(Paragraph("Resumo Executivo", h2_style))
    story.append(_make_table(resumo_rows))
    story.append(Spacer(1, 8))

    # Indicadores
    ind_rows = [
        ["IPR", _v(indicadores.get("IPR"))],
        ["IPM", _v(indicadores.get("IPM"))],
        ["IFC", _v(indicadores.get("IFC"))],
        ["IBE", _v(indicadores.get("IBE"))],
    ]
    story.append(Paragraph("Indicadores Estruturais", h2_style))
    story.append(_make_table(ind_rows))
    story.append(Spacer(1, 8))

    # Alertas
    alert_rows = [
        ["Prejuizo Recente", _v(alertas.get("prejuizo_recente"))],
        ["Liquidez Critica", _v(alertas.get("liquidez_critica"))],
    ]
    story.append(Paragraph("Alertas", h2_style))
    story.append(_make_table(alert_rows))
    story.append(Spacer(1, 8))

    # Qualidade do historico
    conf_rows = [
        ["Status", _v(confianca.get("status"))],
        ["Meses Validos", _v(confianca.get("meses_validos"))],
        ["Maior Sequencia Continua", _v(confianca.get("maior_sequencia_continua"))],
    ]
    story.append(Paragraph("Qualidade do Historico", h2_style))
    story.append(_make_table(conf_rows))

    # Detalhamento tecnico (segue o fluxo, sem quebra forçada)
    story.append(Spacer(1, 18))
    story.append(_section_banner("Detalhamento Tecnico"))
    story.append(Spacer(1, 6))

    baselines = payload.get("baselines")
    if baselines:
        story.append(Paragraph("Baselines", h3_style))
        story.append(_make_table(_dict_rows(baselines)))
        story.append(Spacer(1, 8))

    tecnico = payload.get("tecnico", {})
    if not tecnico:
        story.append(Paragraph("Sem dados tecnicos disponiveis.", small_style))
    else:
        for key in ["IPR", "IPM", "IFC", "IBE", "ISG"]:
            data = tecnico.get(key)
            if not data:
                continue
            story.append(Paragraph(f"Detalhes {key}", h3_style))
            story.append(_make_table(_dict_rows(data)))
            story.append(Spacer(1, 8))

    doc.build(story)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf


def _make_table(rows):
    table = Table([["Campo", "Valor"]] + rows, colWidths=[7 * cm, 9 * cm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8EDF7")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#1C1E21")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 10),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D7DCE5")),
                ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 1), (-1, -1), 9),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    return table


def _dict_rows(data, prefix=""):
    rows = []
    for key, value in data.items():
        label = _normalize_label(f"{prefix}{key}")
        if isinstance(value, dict):
            rows.extend(_dict_rows(value, prefix=f"{label}."))
        else:
            rows.append([label, _v(value)])
    return rows


def _v(value):
    if value is None:
        return "-"
    if isinstance(value, bool):
        return "Sim" if value else "Nao"
    return str(value)


def _load_banner(path, max_width):
    if not os.path.exists(path):
        return None
    try:
        img = ImageReader(path)
        width_px, height_px = img.getSize()
        if width_px <= 0 or height_px <= 0:
            return None
        scale = min(1.0, max_width / float(width_px))
        img_flow = RLImage(path, width=width_px * scale, height=height_px * scale)
        img_flow.hAlign = "CENTER"
        return img_flow
    except Exception:
        return None


def _section_banner(text):
    table = Table([[text]], colWidths=[16 * cm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#1C1E21")),
                ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 12),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return table


def _normalize_label(label):
    if label.startswith("componentes."):
        label = label[len("componentes."):]
    label = label.replace(".componentes.", ".")
    return label
