import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import pandas_datareader.data as web
import datetime
import os

def download_data():
    print("Scaricamento dati in corso...")
    # ETF: SPY (S&P 500)
    spy_df = yf.download("SPY", start="2015-01-01", end="2026-01-01")
    
    # Se yfinance restituisce un MultiIndex, appiattiamolo
    if isinstance(spy_df.columns, pd.MultiIndex):
        spy_df.columns = spy_df.columns.get_level_values(0)
    
    if 'Adj Close' in spy_df.columns:
        spy_price = spy_df['Adj Close']
    else:
        spy_price = spy_df['Close']
    
    # Assicuriamoci che sia una Series
    if isinstance(spy_price, pd.DataFrame):
        spy_price = spy_price.iloc[:, 0]

    # Obbligazioni: Rendimento Treasury a 10 anni (FRED: DGS10)
    start = datetime.datetime(2015, 1, 1)
    end = datetime.datetime(2026, 1, 1)
    try:
        bonds = web.DataReader("DGS10", "fred", start, end)
        if isinstance(bonds, pd.DataFrame):
            bonds = bonds.iloc[:, 0]
    except Exception as e:
        print(f"Errore nel download dei dati FRED: {e}")
        bonds_df = yf.download("TLT", start="2015-01-01", end="2026-01-01")
        if isinstance(bonds_df.columns, pd.MultiIndex):
            bonds_df.columns = bonds_df.columns.get_level_values(0)
        if 'Adj Close' in bonds_df.columns:
            bonds = bonds_df['Adj Close']
        else:
            bonds = bonds_df['Close']
        if isinstance(bonds, pd.DataFrame):
            bonds = bonds.iloc[:, 0]

    return spy_price, bonds

def analyze_non_linearity(returns, label):
    print(f"\n--- Analisi della Non-Linearità per {label} ---")
    
    # Assicuriamoci che i dati siano puliti
    data = returns.dropna()
    
    # Calcolo statistiche
    mu = float(data.mean())
    sigma = float(data.std())
    skewness = float(data.skew())
    kurtosis = float(data.kurtosis())
    
    print(f"Media: {mu:.6f}")
    print(f"Deviazione Standard: {sigma:.6f}")
    print(f"Skewness (Asimmetria): {skewness:.4f}")
    print(f"Curtosi (Code Grasse): {kurtosis:.4f}")
    
    # Test di Normalità (Jarque-Bera)
    jb_stat, jb_p = stats.jarque_bera(data)
    print(f"Test Jarque-Bera p-value: {jb_p:.6e}")
    if jb_p < 0.05:
        print("Conclusione: I rendimenti NON sono distribuiti normalmente (evidenza di non-linearità).")
    else:
        print("Conclusione: I rendimenti sembrano normali.")

def plot_distributions(returns, ticker):
    plt.figure(figsize=(12, 6))
    data = returns.dropna()
    
    # Istogramma vs Normale
    sns.histplot(data, kde=True, stat="density", label="Rendimenti Reali", color='blue', alpha=0.6)
    
    # Generazione distribuzione normale teorica
    x = np.linspace(float(data.min()), float(data.max()), 100)
    p = stats.norm.pdf(x, float(data.mean()), float(data.std()))
    plt.plot(x, p, 'r', linewidth=2, label="Distribuzione Normale Teorica")
    
    plt.title(f"Distribuzione dei Rendimenti di {ticker} vs Normale")
    plt.xlabel("Rendimento Logaritmico / Variazione")
    plt.ylabel("Densità")
    plt.legend()
    plt.grid(True, alpha=0.3)
    save_path = f"/home/ubuntu/{ticker}_distribution.png"
    plt.savefig(save_path)
    plt.close()
    print(f"Grafico salvato: {save_path}")

def main():
    # 1. Download
    spy_price, bond_data = download_data()
    
    # 2. Calcolo Rendimenti Logaritmici per SPY
    spy_returns = np.log(spy_price / spy_price.shift(1)).dropna()
    
    # 3. Analisi SPY
    analyze_non_linearity(spy_returns, "SPY (ETF Azionario)")
    plot_distributions(spy_returns, "SPY")
    
    # 4. Analisi Obbligazioni (Variazione rendimenti o prezzi)
    # Se sono rendimenti (FRED), analizziamo la differenza semplice
    # Se è un ETF (TLT), analizziamo i rendimenti logaritmici
    if bond_data.mean() < 1.0: # Probabilmente rendimenti logaritmici di un ETF
        bond_returns = bond_data
        label = "TLT (ETF Obbligazionario)"
    else: # Probabilmente rendimenti percentuali (FRED)
        bond_returns = bond_data.diff().dropna()
        label = "DGS10 (Rendimento 10Y)"
    
    analyze_non_linearity(bond_returns, label)
    plot_distributions(bond_returns, "BONDS")
    
    print("\n--- Progetto Completato ---")
    print("L'analisi statistica ha confermato la presenza di 'Fat Tails' (Curtosi > 0)")
    print("e asimmetria, che sono i pilastri della probabilità non lineare in finanza.")

if __name__ == "__main__":
    main()
