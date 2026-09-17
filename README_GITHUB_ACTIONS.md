# Bot con ragionamento su notizie reali — versione GitHub Actions

Questa versione è pensata per girare **gratis, in cloud, senza nessun
computer o server da tenere acceso**, tramite GitHub Actions: uno
strumento di GitHub che esegue automaticamente il tuo codice secondo una
pianificazione che scegli tu (di default: una volta al giorno).

**Nessuna operazione reale viene mai eseguita da questo bot.**

## 1. Crea un repository GitHub (privato)

1. Vai su https://github.com e crea un account gratuito se non l'hai già
2. Clicca "New repository"
3. Dagli un nome (es. `il-mio-bot-trading`)
4. **Impostalo come Private** (importante: il codice contiene la logica
   del tuo bot, meglio non renderlo pubblico)
5. Crea il repository

## 2. Carica tutti i file di questo progetto

Puoi farlo dal sito di GitHub stesso (bottone "Add file" -> "Upload
files") caricando tutti i file, **inclusa la cartella `.github`** con il
suo contenuto (`.github/workflows/bot.yml`) — è il file che dice a
GitHub quando e come eseguire il bot.

Se hai familiarità con git da terminale, in alternativa:
```
git clone <url-del-tuo-repository>
cd <nome-repository>
# copia qui tutti i file del progetto
git add .
git commit -m "Primo caricamento del bot"
git push
```

## 3. Configura i "secrets" (le tue chiavi segrete)

Le chiavi NON vanno scritte nei file di codice quando usi GitHub - vanno
salvate come "secrets", visibili solo a GitHub Actions, mai nel codice
visibile.

1. Nel tuo repository, vai su **Settings -> Secrets and variables ->
   Actions**
2. Clicca **New repository secret** e crea questi (uno per uno):
   - `ANTHROPIC_API_KEY` -> la tua chiave da console.anthropic.com
   - `TELEGRAM_BOT_TOKEN` -> (opzionale) il token del tuo bot Telegram
   - `TELEGRAM_CHAT_ID` -> (opzionale) il tuo chat ID Telegram

## 4. Attiva GitHub Actions

Di solito è già attivo di default sui repository nuovi. Verifica andando
sul tab **Actions** del tuo repository: dovresti vedere il workflow "Bot
di trading (controllo giornaliero)".

## 5. Testa manualmente (prima di aspettare la pianificazione automatica)

1. Vai sul tab **Actions**
2. Clicca sul workflow "Bot di trading (controllo giornaliero)"
3. Clicca **Run workflow** (esecuzione manuale, per testare subito senza
   aspettare l'orario programmato)
4. Guarda i log dell'esecuzione direttamente nella pagina - se c'è un
   errore (es. chiave sbagliata), lo vedrai scritto lì

## 6. Cosa succede da qui in poi

- Ogni giorno, all'orario impostato nel file `bot.yml` (di default le
  7:00 UTC, cioè 8-9 del mattino in Italia), GitHub esegue automaticamente
  il bot
- Il bot scarica prezzi reali e notizie reali **in quel momento**, chiede
  il parere a Claude, e (se hai configurato Telegram) ti manda l'avviso
  sul telefono
- Il portafoglio virtuale (`portafoglio_virtuale.json`) e il log
  (`log.txt`) vengono salvati automaticamente nel repository stesso ad
  ogni esecuzione, così i dati non si perdono tra un giorno e l'altro

## Per cambiare l'orario del controllo giornaliero

Apri `.github/workflows/bot.yml` e modifica questa riga:
```yaml
- cron: "0 7 * * *"
```
Il formato è `minuto ora * * *` in orario UTC (non italiano!). Ad esempio,
per farlo girare alle 8:30 del mattino italiano (inverno, UTC+1):
```yaml
- cron: "30 7 * * *"
```
Attenzione: l'Italia cambia ora legale/solare, GitHub Actions no - quindi
l'orario locale reale si sposterà di un'ora due volte l'anno.

## Limiti onesti da conoscere (oltre a quelli già scritti nel README originale)

- Il piano gratuito di GitHub Actions ha un limite mensile di minuti di
  esecuzione (abbondante per un controllo al giorno di pochi minuti, ma
  esiste)
- GitHub potrebbe ritardare l'esecuzione pianificata di qualche minuto
  nei momenti di alto traffico sulla piattaforma - normale, non un bug
- Se il repository resta inattivo per molto tempo (mesi), GitHub può
  disabilitare automaticamente i workflow pianificati: basta riattivarli
  manualmente dal tab Actions se succede
