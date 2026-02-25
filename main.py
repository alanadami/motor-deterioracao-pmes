import pandas as pd
from core.baseline import (
    validate_minimum_history,
    calculate_historical_median,
)
from core.ipr import calculate_ipr
from core.ipm import calculate_ipm
from core.ifc import calculate_ifc
from core.ibe import calculate_ibe


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


# ==============================
# 7️⃣ Output técnico parcial
# ==============================

print("\nResultado IPR:")
print(ipr_result)

print("\nResultado IPM:")
print(ipm_result)

print("\nResultado IFC:")
print(ifc_result)

print("\nResultado IBE:")
print(ibe_result)