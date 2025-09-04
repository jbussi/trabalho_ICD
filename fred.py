import pandas as pd
from fredapi import Fred

fred = Fred(api_key='8f01c5703f25d5ea61bb466337b2a5c7')

series = {
    # Macroeconômicos
    "taxa_juros": "FEDFUNDS",
    "inflacao_cpi": "CPIAUCSL",
    "pib_real": "GDPC1",  # trimestral
    "massa_monetaria": "M2SL",
    "desemprego": "UNRATE",
    "dolar_index": "DTWEXBGS",
    "juros_t10y": "GS10",
    "ouro": "PCU2122212122210",

    # Índices de mercado
    "sp500": "SP500",
    "dow_jones": "DJIA",
    "nasdaq": "NASDAQCOM",

    # Crédito
    "corporate_baa": "BAA",
    "credito_cartao": "TERMCBCCALLNS",
    "mortgage_30y": "MORTGAGE30US"
}

df = pd.DataFrame()

for nome, codigo in series.items():
    try:
        serie = fred.get_series(codigo)
        df[nome] = serie
    except Exception as e:
        print(f"Erro ao baixar {nome}: {e}")

# Ajustar frequência mensal (algumas séries podem ser trimestrais ou diárias)
df = df.resample("M").last()  # pega o último valor de cada mês

# Preencher PIB trimestral com forward-fill
df["pib_real"] = df["pib_real"].ffill()

# Salvar CSV
df.to_csv("dados_macro_fred.csv")
print("✅ CSV gerado com sucesso!")