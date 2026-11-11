# Come generare la voce di Nico (da NON dimenticare)
Aggiornato 11 nov 2026. Il vecchio modello (Gemini 3.1 Flash TTS) è stato sostituito da **Gemini 3.8 Flash TTS**; la voce "Nico Springfieldpedia 3 1" non esiste più.
1. AI Studio → https://aistudio.google.com/generate-speech
2. Se in alto c'è "No API key selected": clic sul pulsante chiave → "Seleziona chiave" (chiave "Gemini API Key", progetto CustomVolley, fatturazione già autorizzata dall'utente). Non si digita nessuna chiave.
3. La voce si chiama **Nico SimpsonsPedia 1 (Custom)**. Se manca: "Create new voice" → Voice Design → nome "Nico SimpsonsPedia", testo = doc/prompt_voce_nico.txt (prima riga) → Generate voice → scegliere il take 1 → Continue → Use voice.
4. Incollare un blocco di 120-200 parole (un blocco = una generazione), Run (Ctrl+Invio), attendere, icona download accanto al player. Il WAV finisce in Downloads come "Generated Audio <data> - <ora>.wav".
5. Mappare i file con lista esplicita dei nomi (mai per mtime). Convertire con ffmpeg -ar 24000 -ac 1.
6. Layout 1536x639: area testo (728,190), Run (1172,611), Download (962,603). Se il layout cambia, usare find/ref invece delle coordinate.
7. Non scrivere "Springfieldpedia": ora il canale è SimpsonsPedia; non indicare nel parlato giorni/numero di uscite.
Se un passo è bloccato: provare a trovare la soluzione qui prima di chiedere all'utente.
