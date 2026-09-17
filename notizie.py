"""
NOTIZIE
========
Scarica i titoli delle notizie più recenti da fonti RSS pubbliche.
Nessuna chiave API richiesta. Se una fonte non risponde, viene saltata
senza far fallire il bot.
"""

import feedparser
import config
import notifiche


def raccogli_notizie() -> list[str]:
    titoli = []
    for url in config.FONTI_NOTIZIE:
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:config.NUMERO_NOTIZIE_PER_FONTE]:
                titolo = entry.get("title", "").strip()
                if titolo:
                    titoli.append(titolo)
        except Exception as e:
            notifiche.log(f"ATTENZIONE: impossibile leggere il feed {url}: {e}", stampa_a_schermo=False)
    return titoli
