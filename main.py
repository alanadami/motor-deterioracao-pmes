import pandas as pd
from core.baseline import (
    validate_minimum_history,
    calculate_historical_median,
)
from core.ipr import calculate_ipr
from core.ipm import calculate_ipm
from core.ifc import calculate_ifc
from core.ibe import calculate_ibe
from core.isg import calculate_isg
from core.confianca import calculate_confianca
from core.utils import format_for_display




# ==============================
# 1️⃣ Carregar dados
# ==============================

df = pd.read_csv("data/empresa_teste.csv")


# ==============================
# 2️⃣ Garantir ordenação cronológica
# ==============================

df["data"] = pd.to_datetime(df["data"])
df = df.sort_values("data")


# ==============================
# 3️⃣ Validar histórico mínimo
# ==============================

validate_minimum_history(df)


# ==============================
# 4️⃣ Feature engineering básica
# ==============================

# Margem operacional absoluta
df["margem"] = df["receita"] - df["custos"]


# ==============================
# 5️⃣ Calcular baselines históricos
# ==============================

mediana_receita = calculate_historical_median(df["receita"])
mediana_margem = calculate_historical_median(df["margem"])
mediana_caixa = calculate_historical_median(df["caixa"])
baseline_margem = calculate_historical_median(df["margem"])

print("Mediana histórica da receita:", mediana_receita)
print("Mediana histórica da margem:", mediana_margem)
print("Mediana histórica do caixa:", mediana_caixa)


# ==============================
# 6️⃣ Calcular indicadores individuais
# ==============================

ipr_result = calculate_ipr(df, mediana_receita)
ipm_result = calculate_ipm(df, mediana_margem)
ifc_result = calculate_ifc(df, mediana_caixa)
ibe_result = calculate_ibe(df, mediana_caixa)
ipm_result = calculate_ipm(df, baseline_margem)
confianca_result = calculate_confianca(df)




# ==============================
# 7️⃣ Output técnico parcial
# ==============================

print("\nResultado IPR:")
print(format_for_display(ipr_result))

print("\nResultado IPM:")
print(format_for_display(ipm_result))

print("\nResultado IFC:")
print(format_for_display(ifc_result))

print("\nResultado IBE:")
print(format_for_display(ibe_result))

print("\nNível de confiança:")
print(format_for_display(confianca_result))


print("\nResultado ISG:")
isg_result = calculate_isg(
    ipr_result,
    ipm_result,
    ifc_result,
    ibe_result,
    confianca_result
)

print(format_for_display(isg_result))

from core.report import generate_dashboard_payload

dashboard_payload = generate_dashboard_payload(
    ipr_result,
    ipm_result,
    ifc_result,
    ibe_result,
    isg_result,
    confianca_result
)

print(dashboard_payload)