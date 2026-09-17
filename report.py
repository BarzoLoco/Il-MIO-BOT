"""
REPORT LEGGIBILE (STORICO.md)
================================
Genera un file Markdown con l'andamento del portafoglio virtuale e la
lista delle operazioni fatte finora. GitHub mostra i file .md già
formattati con tabelle leggibili quando li apri sul sito - non serve
scaricare né installare nulla per leggerlo.
"""

import config

FILE_REPORT = "STORICO.md"


def genera_report(portafoglio: dict):
    storico_valore = portafoglio["storico_valore"]
    operazioni = portafoglio["storico_operazioni"]
    capitale_iniziale = config.CAPITALE_VIRTUALE_INIZIALE

    valore_attuale = storico_valore[-1]["valore"] if storico_valore else capitale_iniziale
    variazione_totale_pct = (valore_attuale / capitale_iniziale - 1) * 100
    giorni_attivi = len(storico_valore)

    righe = []
    righe.append("# Storico del portafoglio virtuale\n")
    righe.append(
        "> Aggiornato automaticamente dal bot ad ogni esecuzione. "
        "Soldi finti, prezzi reali. Nessuna operazione reale è mai stata eseguita.\n"
    )
    righe.append("![Andamento del portafoglio](dashboard.png)\n")

    righe.append("## Riepilogo\n")
    segno = "+" if variazione_totale_pct >= 0 else ""
    righe.append(f"- **Capitale iniziale**: €{capitale_iniziale:.2f}")
    righe.append(f"- **Valore attuale**: €{valore_attuale:.2f}")
    righe.append(f"- **Variazione totale**: {segno}{variazione_totale_pct:.2f}%")
    righe.append(f"- **Giorni di attività registrati**: {giorni_attivi}\n")

    righe.append("## Andamento giornaliero del valore\n")
    if storico_valore:
        righe.append("| Data | Valore (€) | Variazione da inizio |")
        righe.append("|---|---|---|")
        for punto in storico_valore:
            var_pct = (punto["valore"] / capitale_iniziale - 1) * 100
            segno_riga = "+" if var_pct >= 0 else ""
            righe.append(f"| {punto['data']} | {punto['valore']:.2f} | {segno_riga}{var_pct:.2f}% |")
    else:
        righe.append("_Nessun dato ancora registrato._")
    righe.append("")

    righe.append("## Operazioni eseguite (virtuali), con motivazione\n")
    if operazioni:
        for op in reversed(operazioni):  # più recenti prima
            var = op.get("variazione_pct")
            var_str = f" ({'+' if var and var >= 0 else ''}{var:.2f}%)" if var is not None else ""
            quantita = op.get("quantita")
            asset_base = op["ticker"].split("-")[0] if "ticker" in op else ""
            quantita_str = f" — {quantita:.8f}".rstrip("0").rstrip(".") + f" {asset_base}" if quantita else ""
            righe.append(f"**{op['data']} — {op['nome']} — {op['azione']}** a €{op['prezzo']:.2f}{var_str}{quantita_str}")
            righe.append(f"> {op.get('motivazione', '(nessuna motivazione registrata)')}")
            righe.append("")
    else:
        righe.append("_Nessuna operazione eseguita finora._")
    righe.append("")

    with open(FILE_REPORT, "w", encoding="utf-8") as f:
        f.write("\n".join(righe))
