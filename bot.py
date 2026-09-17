"""
BOT PRINCIPALE
===============
Lancia con: python bot.py

Ogni ciclo (di default una volta al giorno):
 1. Scarica prezzi + calcola indicatori tecnici per ogni asset
 2. Raccoglie notizie finanziarie reali (RSS)
 3. Chiede a Claude un parere motivato per ogni asset (dati + notizie)
 4. Ti avvisa (log + Telegram) con il suggerimento e la motivazione
 5. Aggiorna il portafoglio VIRTUALE come se avessi seguito il suggerimento
    (solo per misurare "cosa sarebbe successo" - nessun soldo vero è toccato)

Questo bot non ha alcun accesso al tuo conto reale o a Directa. Quando
deciderai di collegare Directa, sarà un passo separato ed esplicito, non
un'estensione automatica di questo script.
"""

import time
import datetime

import config
import dati
import notizie
import cervello
import portafoglio
import notifiche
import report
import grafico


def esegui_ciclo():
    port = portafoglio.carica_portafoglio()
    titoli_notizie = notizie.raccogli_notizie()
    notifiche.log(f"Notizie raccolte oggi: {len(titoli_notizie)}")

    prezzi_attuali = {}

    for asset in config.ASSETS:
        ticker, nome = asset["ticker"], asset["nome"]
        try:
            df = dati.scarica_storico(ticker)
            df = dati.calcola_indicatori(df)
            riassunto = dati.riassunto_tecnico(df)
        except Exception as e:
            notifiche.log(f"[{nome}] Errore nel recupero dati: {e}")
            continue

        prezzi_attuali[ticker] = riassunto["prezzo_attuale"]

        try:
            parere = cervello.chiedi_parere(nome, ticker, riassunto, titoli_notizie)
        except Exception as e:
            notifiche.log(f"[{nome}] Errore nel chiedere il parere a Claude: {e}")
            continue

        messaggio = (
            f"[{nome}] Suggerimento: {parere['suggerimento'].upper()} "
            f"(confidenza: {parere['confidenza']})\n"
            f"Prezzo attuale: {riassunto['prezzo_attuale']}\n"
            f"Motivazione: {parere['motivazione']}\n"
            f"(Promemoria: nessuna operazione reale è stata eseguita)"
        )
        notifiche.avvisa(messaggio)

        oggi = datetime.date.today().isoformat()
        portafoglio.applica_suggerimento(port, ticker, nome, parere["suggerimento"],
                                           riassunto["prezzo_attuale"], oggi,
                                           motivazione=parere["motivazione"])

    valore_virtuale = portafoglio.valore_totale(port, prezzi_attuali)
    notifiche.log(
        f"Portafoglio VIRTUALE oggi: €{valore_virtuale:.2f} "
        f"(partito da €{config.CAPITALE_VIRTUALE_INIZIALE:.2f})"
    )
    oggi = datetime.date.today().isoformat()
    portafoglio.registra_valore_giornaliero(port, oggi, valore_virtuale)
    portafoglio.salva_portafoglio(port)
    grafico.genera_grafico(port)
    report.genera_report(port)
    notifiche.log("Report STORICO.md e grafico dashboard.png aggiornati.")


def main():
    notifiche.log("=== Avvio bot (ragionamento su notizie reali, portafoglio virtuale) ===")
    if not config.MODALITA_TEST:
        if config.PROVIDER == "gemini" and not config.GEMINI_API_KEY:
            notifiche.log("ERRORE: GEMINI_API_KEY non impostata.")
            return
        if config.PROVIDER == "anthropic" and not config.ANTHROPIC_API_KEY:
            notifiche.log("ERRORE: ANTHROPIC_API_KEY non impostata.")
            return
    while True:
        try:
            esegui_ciclo()
        except Exception as e:
            notifiche.log(f"ERRORE nel ciclo: {e}")
        prossimo = datetime.datetime.now() + datetime.timedelta(seconds=config.CHECK_INTERVAL_SECONDS)
        notifiche.log(f"Prossimo controllo: {prossimo.strftime('%Y-%m-%d %H:%M')}")
        time.sleep(config.CHECK_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
