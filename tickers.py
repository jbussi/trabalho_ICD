import pandas as pd
import requests

# URL da página da Wikipedia
url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)

# Ler tabelas
tables = pd.read_html(response.text, header=[0, 1])  # <- pega os dois níveis do cabeçalho

# Empresas atuais
df_current = tables[0][["Symbol", "Security"]].copy()
df_current.columns = ["Ticker", "Security"]
df_current["Status"] = "current"

# Histórico de mudanças (com MultiIndex)
df_changes = tables[1]

# Achatar os nomes de coluna (ex: ("Added","Ticker") -> "Added_Ticker")
df_changes.columns = ['_'.join(col).strip() for col in df_changes.columns.values]

# "Added" -> Ticker e Security
df_added = df_changes[["Added_Ticker", "Added_Security"]].copy()
df_added.columns = ["Ticker", "Security"]
df_added["Status"] = "added"

# "Removed" -> Ticker e Security
df_removed = df_changes[["Removed_Ticker", "Removed_Security"]].copy()
df_removed.columns = ["Ticker", "Security"]
df_removed["Status"] = "removed"

# Concatenar tudo
df_all = pd.concat([df_current, df_added, df_removed], ignore_index=True)

# Remover duplicados
df_all = df_all.dropna(subset=["Ticker"]).drop_duplicates()
df_all = df_all.dropna(subset=["Ticker"]).drop_duplicates(subset=["Ticker"], keep="first")
df_all.loc[df_all["Status"] != "current", "Status"] = "removed"
df_all = df_all.sort_values("Ticker").reset_index(drop=True)
df_all.to_csv("sp500_historical_list.csv", index=False)

print(df_all.head(20))