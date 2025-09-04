import yfinance as yf
import pandas as pd
import time
import os

token = '8f01c5703f25d5ea61bb466337b2a5c7'
# Lista de tickers (exemplo, você pode expandir com CSV de Nasdaq/NYSE)
data = pd.read_csv('nasdaq_screener_1756424326052.csv')
tickers = data['Symbol'].dropna().unique().tolist()

os.makedirs("dados_acoes", exist_ok=True)


# DataFrame para guardar dados fundamentais
def salvar_dados(ticker):
    try:
        t = yf.Ticker(ticker)

        # Preço histórico (máximo possível)
        hist = t.history(period="max")
        hist.to_csv(f"dados_acoes/{ticker}_historico.csv")

        # Info fundamental
        info = t.info
        pd.DataFrame([info]).to_csv(f"dados_acoes/{ticker}_fundamental.csv", index=False)

        # Balanço, DRE e Fluxo de Caixa
        t.balance_sheet.to_csv(f"dados_acoes/{ticker}_balanco.csv")
        t.financials.to_csv(f"dados_acoes/{ticker}_dre.csv")
        t.cashflow.to_csv(f"dados_acoes/{ticker}_fluxo.csv")

        print(f"✅ {ticker} salvo com sucesso")
    except Exception as e:
        print(f"❌ Erro com {ticker}: {e}")

# Loop em todos os tickers
for ticker in tickers:
    salvar_dados(ticker)
    time.sleep(2) 

print("✅ Download concluído!")