"""
CONFIGURAZIONE
===============
Questo bot NON esegue mai ordini reali da solo. Raccoglie dati di prezzo +
notizie reali, chiede un parere motivato a Claude (Anthropic), e ti avvisa.
Il "portafoglio" che traccia è virtuale (soldi finti), utile per valutare
nelle prossime settimane se le sue segnalazioni si sarebbero rivelate
sensate, PRIMA di collegare qualsiasi conto vero (Directa o altro).
"""

# ---------------------------------------------------------------------------
# 1) ASSET DA MONITORARE (ticker Yahoo Finance)
# ---------------------------------------------------------------------------
ASSETS = [
    {"ticker": "BTC-USD", "nome": "Bitcoin"},
    {"ticker": "SPY", "nome": "S&P 500 (ETF)"},
]

# ---------------------------------------------------------------------------
# 2) INDICATORI TECNICI (dati giornalieri)
# ---------------------------------------------------------------------------
SMA_FAST = 20
SMA_SLOW = 50
RSI_PERIOD = 14

# ---------------------------------------------------------------------------
# 3) FONTI DI NOTIZIE (feed RSS pubblici, nessuna chiave richiesta)
# ---------------------------------------------------------------------------
FONTI_NOTIZIE = [
    "https://www.investing.com/rss/news_25.rss",       # Investing.com - Economia
    "https://feeds.reuters.com/reuters/businessNews",   # Reuters Business
]
NUMERO_NOTIZIE_PER_FONTE = 8

# ---------------------------------------------------------------------------
# 4) IL "CERVELLO" CHE RAGIONA SU DATI + NOTIZIE
# ---------------------------------------------------------------------------
import os

# Scegli il fornitore: "gemini" (GRATUITO, consigliato per iniziare) oppure
# "anthropic" (Claude, a pagamento ma economico - pochi centesimi al mese
# per questo uso). Entrambi funzionano con la stessa logica del bot.
PROVIDER = os.environ.get("PROVIDER", "gemini")

# --- Google Gemini (gratuito) ---
# Crea una chiave gratuita su https://aistudio.google.com/apikey
# (accedi con un account Google, nessuna carta di credito richiesta).
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
# Controlla i modelli disponibili nel piano gratuito su https://ai.google.dev/gemini-api/docs/rate-limits
# (i nomi dei modelli gratuiti cambiano nel tempo - verifica quello aggiornato)
MODELLO_GEMINI = os.environ.get("MODELLO_GEMINI", "gemini-2.0-flash-lite")

# --- Anthropic Claude (a pagamento) ---
# Crea una chiave su https://console.anthropic.com
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
# Controlla il modello più recente su https://docs.claude.com
MODELLO_ANTHROPIC = "claude-sonnet-5"

# MODALITA' TEST: se True, il bot NON chiama davvero nessuna API (quindi
# nessun costo, nessuna chiave necessaria) e usa invece una risposta finta
# di esempio. Utile per verificare che tutto il resto dell'infrastruttura
# (dati, notizie, portafoglio virtuale, GitHub Actions, Telegram) funzioni
# correttamente, prima di collegare qualsiasi chiave vera.
MODALITA_TEST = os.environ.get("MODALITA_TEST", "true").lower() == "true"

# ---------------------------------------------------------------------------
# 5) PORTAFOGLIO VIRTUALE ("SOLDI DEL MONOPOLI")
# ---------------------------------------------------------------------------
CAPITALE_VIRTUALE_INIZIALE = 100.0
MAX_POSITION_PCT = 0.30       # % massima di capitale virtuale per asset

# ---------------------------------------------------------------------------
# 6) FREQUENZA DI CONTROLLO
# ---------------------------------------------------------------------------
CHECK_INTERVAL_SECONDS = 60 * 60 * 24   # una volta al giorno

# ---------------------------------------------------------------------------
# 7) NOTIFICHE TELEGRAM (opzionale)
# ---------------------------------------------------------------------------
# Anche questi letti da variabili d'ambiente, stesso motivo delle chiavi sopra.
TELEGRAM_ENABLED = os.environ.get("TELEGRAM_BOT_TOKEN", "") != ""
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "")

STATO_FILE = "portafoglio_virtuale.json"
