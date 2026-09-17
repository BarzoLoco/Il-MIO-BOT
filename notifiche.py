import datetime
import config

try:
    import requests
except ImportError:
    requests = None

LOG_FILE = "log.txt"


def log(messaggio: str, stampa_a_schermo: bool = True):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    riga = f"[{timestamp}] {messaggio}"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(riga + "\n")
    if stampa_a_schermo:
        print(riga)


def avvisa(messaggio: str):
    log(messaggio)
    if config.TELEGRAM_ENABLED:
        _invia_telegram(messaggio)


def _invia_telegram(testo: str):
    if requests is None or not config.TELEGRAM_BOT_TOKEN or not config.TELEGRAM_CHAT_ID:
        return
    url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": config.TELEGRAM_CHAT_ID, "text": testo}, timeout=10)
    except Exception as e:
        log(f"ATTENZIONE: invio Telegram fallito: {e}", stampa_a_schermo=False)
