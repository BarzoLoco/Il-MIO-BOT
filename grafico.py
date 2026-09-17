"""
GRAFICO
========
Genera un'immagine (PNG) con l'andamento del portafoglio virtuale nel
tempo. Viene incorporata dentro STORICO.md, così è visibile direttamente
aprendo quel file su GitHub (anche dall'app mobile), senza bisogno di
nessun hosting esterno - il repository può restare privato.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import config

FILE_GRAFICO = "dashboard.png"


def genera_grafico(portafoglio: dict):
    storico = portafoglio["storico_valore"]
    if len(storico) < 2:
        return False  # troppo pochi punti per un grafico leggibile, saltiamo

    date = [p["data"] for p in storico]
    valori = [p["valore"] for p in storico]
    capitale_iniziale = config.CAPITALE_VIRTUALE_INIZIALE

    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(date, valori, marker="o", color="#27ae60", linewidth=2)
    ax.axhline(capitale_iniziale, color="#888", linestyle="--", linewidth=1,
               label=f"Capitale iniziale (€{capitale_iniziale:.0f})")

    ax.set_title("Andamento del portafoglio virtuale")
    ax.set_ylabel("Valore (€)")
    ax.legend(loc="best", fontsize=9)
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    fig.savefig(FILE_GRAFICO, dpi=130)
    plt.close(fig)
    return True
