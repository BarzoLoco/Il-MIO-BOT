"""
IL "CERVELLO"
==============
Manda, per ogni asset, i dati tecnici (numeri puri) + le notizie del
giorno (testo puro) a un modello linguistico (Gemini o Claude, a seconda
di config.PROVIDER), chiedendo un suggerimento con motivazione.

IMPORTANTE: il modello NON prende decisioni finanziarie vincolanti - genera
un'opinione testuale motivata, come lo farebbe un analista che legge le
stesse notizie che leggi tu. Il bot non esegue nulla sulla base di questa
risposta: la mostra a te, e basta.
"""

import json
import requests
import config


PROMPT_TEMPLATE = """Sei un assistente che aiuta un investitore individuale (capitale molto piccolo,
circa 100 euro virtuali, orizzonte di alcuni mesi) a interpretare la situazione di un asset.

NON stai eseguendo nessuna operazione. Stai solo dando un'opinione motivata che l'investitore
valuterà insieme ad altre informazioni prima di decidere lui stesso.

Asset: {nome} ({ticker})

Dati tecnici attuali (numeri, non interpretazione):
{dati_tecnici}

Titoli di notizie finanziarie/economiche generali delle ultime ore (potrebbero non riguardare
direttamente questo asset - usa il tuo giudizio su quali sono rilevanti):
{notizie}

Rispondi SOLO in JSON valido, senza testo prima o dopo, in questo formato esatto:
{{
  "suggerimento": "compra" | "vendi" | "attendi",
  "confidenza": "bassa" | "media" | "alta",
  "motivazione": "spiegazione in italiano, massimo 3 frasi, che cita sia i dati tecnici sia
     eventuali notizie rilevanti se ce ne sono; se le notizie non sono rilevanti per questo
     asset, dillo esplicitamente e basati solo sui dati tecnici"
}}
"""


def _pulisci_e_valida_json(testo: str) -> dict:
    pulito = testo.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    parere = json.loads(pulito)
    assert parere["suggerimento"] in ("compra", "vendi", "attendi")
    return parere


def _chiedi_a_gemini(prompt: str) -> dict:
    url = (
        f"https://generativelanguage.googleapis.com/v1beta/models/"
        f"{config.MODELLO_GEMINI}:generateContent?key={config.GEMINI_API_KEY}"
    )
    risposta = requests.post(
        url,
        json={"contents": [{"parts": [{"text": prompt}]}]},
        timeout=30,
    )
    risposta.raise_for_status()
    testo = risposta.json()["candidates"][0]["content"]["parts"][0]["text"]
    return _pulisci_e_valida_json(testo)


def _chiedi_a_claude(prompt: str) -> dict:
    risposta = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers={
            "x-api-key": config.ANTHROPIC_API_KEY,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        json={
            "model": config.MODELLO_ANTHROPIC,
            "max_tokens": 400,
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=30,
    )
    risposta.raise_for_status()
    testo = risposta.json()["content"][0]["text"]
    return _pulisci_e_valida_json(testo)


def chiedi_parere(nome: str, ticker: str, dati_tecnici: dict, notizie: list[str]) -> dict:
    if config.MODALITA_TEST:
        return {
            "suggerimento": "attendi",
            "confidenza": "bassa",
            "motivazione": (
                f"[MODALITA TEST - nessuna vera analisi] Questo è un parere finto "
                f"generato senza chiamare nessuna API, per verificare che "
                f"l'infrastruttura funzioni. Prezzo rilevato: {dati_tecnici.get('prezzo_attuale')}. "
                f"Notizie raccolte: {len(notizie)}."
            ),
        }

    prompt = PROMPT_TEMPLATE.format(
        nome=nome,
        ticker=ticker,
        dati_tecnici=json.dumps(dati_tecnici, indent=2, ensure_ascii=False),
        notizie="\n".join(f"- {n}" for n in notizie) if notizie else "(nessuna notizia disponibile oggi)",
    )

    if config.PROVIDER == "gemini":
        return _chiedi_a_gemini(prompt)
    elif config.PROVIDER == "anthropic":
        return _chiedi_a_claude(prompt)
    else:
        raise ValueError(f"PROVIDER non riconosciuto: {config.PROVIDER!r} (usa 'gemini' o 'anthropic')")
