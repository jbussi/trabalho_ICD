import pandas as pd
import yfinance as yf

# Ler CSVs
df_all = pd.read_csv("sp500_historical_list.csv")
df_validity = pd.read_csv("tickers_validity.csv")

# Tickers válidos e inválidos
valid_tickers = df_validity[df_validity["Valid"] == True]["Ticker"].tolist()
invalid_tickers = df_validity[df_validity["Valid"] == False]["Ticker"].tolist()

print(f"Tickers válidos: {len(valid_tickers)}")
print(f"Tickers inválidos: {len(invalid_tickers)}")

# Função para tentar buscar informações de tickers inválidos
def get_info(ticker):
    try:
        t = yf.Ticker(ticker)
        info = t.info
        if info and "longName" in info:
            return {"Ticker": ticker, "Found": True, "Name": info.get("longName"), "Exchange": info.get("exchange")}
        else:
            return {"Ticker": ticker, "Found": False, "Name": None, "Exchange": None}
    except Exception:
        return {"Ticker": ticker, "Found": False, "Name": None, "Exchange": None}

# Rodar análise nos inválidos
results = [get_info(ticker) for ticker in invalid_tickers]

# Criar DataFrame com resultados
df_invalid_analysis = pd.DataFrame(results)
df_invalid_analysis.to_csv("tickers_invalid_analysis.csv", index=False)

print(df_invalid_analysis.head())