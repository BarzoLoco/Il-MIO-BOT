"""
PORTAFOGLIO VIRTUALE
=====================
Simula "cosa sarebbe successo se avessi seguito ogni suggerimento del
bot". Usa prezzi REALI (aggiornati ogni giorno) ma soldi FINTI. Utile per
valutare nelle prossime settimane se i suggerimenti sono stati sensati,
PRIMA di rischiare qualsiasi soldo vero.

Nota: questo è un benchmark ("se avessi sempre seguito il bot"), non
significa che tu debba seguirlo alla cieca - resta uno strumento di
valutazione, non un ordine.
"""

import json
import os
import config


def carica_portafoglio() -> dict:
    if not os.path.exists(config.STATO_FILE):
        return {
            "cash": config.CAPITALE_VIRTUALE_INIZIALE,
            "posizioni": {},   # {ticker: {"quantita": ..., "prezzo_medio": ...}}
            "storico_operazioni": [],
            "storico_valore": [],   # [{"data": ..., "valore": ...}, ...]
        }
    with open(config.STATO_FILE, "r", encoding="utf-8") as f:
        portafoglio = json.load(f)
        portafoglio.setdefault("storico_valore", [])  # compatibilità con salvataggi vecchi
        return portafoglio


def registra_valore_giornaliero(portafoglio: dict, data: str, valore: float):
    """Aggiunge (o aggiorna, se già presente per oggi) il valore totale del
    portafoglio nello storico giornaliero - usato per il grafico/report."""
    storico = portafoglio["storico_valore"]
    if storico and storico[-1]["data"] == data:
        storico[-1]["valore"] = valore
    else:
        storico.append({"data": data, "valore": round(valore, 4)})


def salva_portafoglio(portafoglio: dict):
    with open(config.STATO_FILE, "w", encoding="utf-8") as f:
        json.dump(portafoglio, f, indent=2, ensure_ascii=False)


def valore_totale(portafoglio: dict, prezzi_attuali: dict) -> float:
    valore = portafoglio["cash"]
    for ticker, pos in portafoglio["posizioni"].items():
        valore += pos["quantita"] * prezzi_attuali.get(ticker, pos["prezzo_medio"])
    return valore


def applica_suggerimento(portafoglio: dict, ticker: str, nome: str, suggerimento: str,
                          prezzo_attuale: float, data: str, motivazione: str = ""):
    posizione = portafoglio["posizioni"].get(ticker, {"quantita": 0.0, "prezzo_medio": 0.0})
    in_posizione = posizione["quantita"] > 0

    if suggerimento == "compra" and not in_posizione:
        importo = valore_totale(portafoglio, {ticker: prezzo_attuale}) * config.MAX_POSITION_PCT
        importo = min(importo, portafoglio["cash"])
        if importo <= 0:
            return
        quantita = importo / prezzo_attuale
        portafoglio["cash"] -= importo
        portafoglio["posizioni"][ticker] = {"quantita": quantita, "prezzo_medio": prezzo_attuale}
        portafoglio["storico_operazioni"].append(
            {"data": data, "ticker": ticker, "nome": nome, "azione": "COMPRA (virtuale)",
             "prezzo": prezzo_attuale, "quantita": quantita, "motivazione": motivazione}
        )

    elif suggerimento == "vendi" and in_posizione:
        ricavo = posizione["quantita"] * prezzo_attuale
        portafoglio["cash"] += ricavo
        variazione_pct = (prezzo_attuale / posizione["prezzo_medio"] - 1) * 100
        portafoglio["storico_operazioni"].append(
            {"data": data, "ticker": ticker, "nome": nome, "azione": "VENDI (virtuale)",
             "prezzo": prezzo_attuale, "quantita": posizione["quantita"],
             "variazione_pct": round(variazione_pct, 2), "motivazione": motivazione}
        )
        portafoglio["posizioni"][ticker] = {"quantita": 0.0, "prezzo_medio": 0.0}
