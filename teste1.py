import yfinance as yf
import pandas as pd

# Ler CSV
df_all = pd.read_csv("sp500_historical_list.csv")

# Lista de tickers
tickers = df_all["Ticker"].tolist()

# Função para testar se o ticker é válido
def check_ticker(ticker):
    try:
        data = yf.Ticker(ticker).history(period="1d")
        return not data.empty
    except Exception:
        return False

# Verificar todos os tickers
validity = {ticker: check_ticker(ticker) for ticker in tickers}

# Criar DataFrame com resultados
df_validity = pd.DataFrame(list(validity.items()), columns=["Ticker", "Valid"])
print(df_validity.head())

# Filtrar apenas tickers válidos
valid_tickers = df_validity[df_validity["Valid"]]["Ticker"].tolist()

df_validity.to_csv("tickers_validity.csv", index=False)
pd.DataFrame(valid_tickers, columns=["Ticker"]).to_csv("valid_tickers.csv", index=False)

print(f"Número de tickers válidos: {len(valid_tickers)}")