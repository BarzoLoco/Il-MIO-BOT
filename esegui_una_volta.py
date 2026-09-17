"""
ESECUZIONE SINGOLA (per GitHub Actions)
==========================================
A differenza di bot.py (che gira in loop continuo su un PC/server sempre
acceso), questo script fa UN SOLO ciclo e termina. È pensato per essere
lanciato da un sistema esterno che decide *quando* farlo partire (nel
nostro caso: GitHub Actions, una volta al giorno secondo lo schedule
definito in .github/workflows/bot.yml).
"""

import bot
import notifiche
import config

if __name__ == "__main__":
    notifiche.log("=== Esecuzione singola (GitHub Actions) ===")
    if config.MODALITA_TEST:
        notifiche.log("MODALITA TEST attiva: nessuna chiamata reale a Claude, nessun costo.")
    elif not config.ANTHROPIC_API_KEY:
        notifiche.log("ERRORE: variabile d'ambiente ANTHROPIC_API_KEY non impostata.")
        raise SystemExit(1)
    bot.esegui_ciclo()
    notifiche.log("=== Ciclo completato, lo script termina qui (nessun loop) ===")
