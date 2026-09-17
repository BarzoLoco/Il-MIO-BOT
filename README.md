# Bot con ragionamento su notizie reali (Claude + portafoglio virtuale)

Ogni giorno il bot: scarica prezzi e indicatori tecnici, raccoglie notizie
finanziarie reali via RSS, chiede a Claude un parere motivato per ogni
asset, ti avvisa, e aggiorna un portafoglio **virtuale** (soldi finti) per
farti vedere cosa sarebbe successo se avessi seguito ogni suggerimento.

**Nessuna operazione reale viene mai eseguita da questo bot.**

## 1. Installazione

```
pip install -r requirements.txt
```

## 2. Crea una chiave API Anthropic

1. Vai su https://console.anthropic.com e crea un account
2. Genera una API key (sezione "API Keys")
3. Ricarica un piccolo credito (l'uso di questo bot - una manciata di
   richieste brevi al giorno - costa tipicamente centesimi al mese, non
   euro; controlla i prezzi aggiornati su https://docs.claude.com)
4. Incolla la chiave in `config.py`:
   ```python
   ANTHROPIC_API_KEY = "sk-ant-..."
   ```

## 3. (Opzionale) Notifiche Telegram

Stessa procedura delle versioni precedenti: `@BotFather` per il token,
`@userinfobot` per il tuo chat_id, poi in `config.py`:
```python
TELEGRAM_ENABLED = True
TELEGRAM_BOT_TOKEN = "..."
TELEGRAM_CHAT_ID = "..."
```

## 4. Avvia

```
python bot.py
```

Ogni giorno vedrai (e riceverai su Telegram, se attivo) qualcosa come:
```
[Bitcoin] Suggerimento: ATTENDI (confidenza: media)
Prezzo attuale: 112543.20
Motivazione: Il prezzo è sopra la media mobile lenta ma l'RSI a 74 indica
ipercomprato. Le notizie di oggi menzionano tensioni geopolitiche che
potrebbero aumentare la volatilità a breve termine, non specifiche per BTC.
(Promemoria: nessuna operazione reale è stata eseguita)

Portafoglio VIRTUALE oggi: €103.40 (partito da €100.00)
```

## 5. Segui il portafoglio virtuale per 2+ settimane

Il file `portafoglio_virtuale.json` si aggiorna automaticamente e ti dice
cosa sarebbe successo seguendo ogni suggerimento alla lettera, con prezzi
reali. Guardalo con occhio critico:
- Le motivazioni ti sembrano sensate, o generiche/scontate?
- Il portafoglio virtuale cresce, resta stabile, o perde valore?
- Ti fideresti di queste stesse motivazioni con soldi veri?

## 6. Il passo verso Directa (quando/se sarai pronto)

Questo è deliberatamente **un passo separato**, non automatico:
1. Attiva l'API sul tuo conto Directa (dalla tua area personale:
   Info -> Additional Activations -> API)
2. Installa e apri la piattaforma Darwin di Directa
3. Userai una libreria come `directa-api-wrapper` (cerca su PyPI) per
   collegare Python a Darwin - è un progetto separato da integrare, non
   una semplice riga di config qui
4. Anche allora, ti consiglio di iniziare in modalità simulazione
   (offerta dalla libreria stessa) prima di passare a ordini reali

## Limiti onesti da conoscere

- **Le notizie raccolte sono generiche** (RSS di economia/finanza in
  generale), non filtrate per essere specifiche sugli asset che segui.
  Claude userà il suo giudizio per capire cosa è rilevante, ma non
  aspettarti che trovi sempre una notizia "perfetta" per BTC o SPY ogni
  giorno - spesso dirà onestamente che le notizie non sono rilevanti.
- **Claude non ha accesso a dati in tempo reale oltre a quello che gli
  passiamo noi nel prompt** - ragiona solo sui numeri e i titoli che il
  bot gli fornisce in quel momento, non su una conoscenza di mercato
  aggiornata al secondo.
- **Un parere motivato non è una previsione garantita.** Anche un'ottima
  motivazione può risultare sbagliata: i mercati sono difficili da
  prevedere per chiunque, umano o IA.
- **Il portafoglio virtuale è un benchmark**, non un consiglio a seguirlo
  ciecamente quando/se passerai al conto vero.
