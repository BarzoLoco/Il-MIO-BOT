"""
DATI DI MERCATO E INDICATORI
==============================
"""

import yfinance as yf
import pandas as pd
import config


def scarica_storico(ticker: str, periodo: str = "6mo") -> pd.DataFrame:
    df = yf.download(ticker, period=periodo, interval="1d", progress=False, auto_adjust=True)
    if df.empty:
        raise ValueError(f"Nessun dato per {ticker}")
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df = df.reset_index().rename(columns={"Close": "close", "Date": "data"})
    return df[["data", "close"]]


def calcola_indicatori(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["sma_fast"] = df["close"].rolling(config.SMA_FAST).mean()
    df["sma_slow"] = df["close"].rolling(config.SMA_SLOW).mean()
    delta = df["close"].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(config.RSI_PERIOD).mean()
    avg_loss = loss.rolling(config.RSI_PERIOD).mean()
    rs = avg_gain / avg_loss
    df["rsi"] = 100 - (100 / (1 + rs))
    return df


def riassunto_tecnico(df: pd.DataFrame) -> dict:
    """Numeri puri, senza interpretazione - la interpretazione la fa Claude dopo."""
    ultima = df.iloc[-1]
    trend = "sopra" if ultima["sma_fast"] > ultima["sma_slow"] else "sotto"
    return {
        "prezzo_attuale": round(float(ultima["close"]), 2),
        "sma_fast": round(float(ultima["sma_fast"]), 2),
        "sma_slow": round(float(ultima["sma_slow"]), 2),
        "posizione_media_veloce_vs_lenta": trend,
        "rsi": round(float(ultima["rsi"]), 1),
        "variazione_7gg_pct": round(float(df["close"].pct_change(7).iloc[-1] * 100), 2),
        "variazione_30gg_pct": round(float(df["close"].pct_change(30).iloc[-1] * 100), 2),
    }
