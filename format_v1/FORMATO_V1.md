# Formato Springfieldpedia v1 (classifica) — salvato 5 nov 2026

Struttura video (8–9 min):
1. HOOK (blocco B01, ~32 s): Nico parla, ogni ~4 s taglio su una scena di un episodio diverso (2,6 s).
2. SIGLA (5,5 s): logo + tagline + stacco musicale (sigla.py).
3. Per ogni posizione N°10 → N°1:
   - Blocco voce di Nico (~33 s) con cartello "N°x" in alto a sinistra e titolo episodio in basso (mai sopra Nico).
   - 3 scene "intermezzo" dell'episodio da 5 s a 6 s, 14,5 s, 23 s (broll.py), la voce continua.
   - Clip originale ~10 s a tutto schermo con audio originale + sottotitoli italiani (cut.py).
4. CONCLUSIONE (B12) con ISCRIVITI + "Martedì + Venerdì ore 17:00".

Per cambiare un video NON si rifà la voce: si cambiano solo gli elenchi BR (broll.py) e C (cut.py).
Pipeline: nb.py (Nico + bocca sincronizzata, pose Definitivo V2) → broll.py (scene) → sigla.py → final.sh (concat + musica con ducking).
Shorts: shorts.py (9:16: finestra con scene sopra, Nico sotto, poi clip originale).
Pose Nico: solo 08_Definitivo_v2.

## Regole aggiunte dopo il feedback (5 nov, v3) — valide per TUTTI i video
- Le scene intermezzo devono essere SINCRONIZZATE con ciò che dice Nico: si calcolano i tempi delle frasi (sent.py) e si assegna a ogni frase una scena dell'episodio che la illustra (broll.py, dizionario BR).
- A metà di ogni blocco c'è una clip ICONICA completa (7–12 s) con voci originali e sottotitoli italiani (cut2.py, lista M; punto di inserimento in SPLIT).
- A fine blocco resta la clip finale con audio originale.
- Scritte mai sopra Nico: numero in alto a sinistra, titolo episodio in basso al centro.
- Hook con scene intercalate in sync, poi sigla (sigla.py).
- Per un nuovo video: copione + voce → sent.py (tempi frasi) → compilare BR, M, SPLIT → build2.sh.

## Formato Short "Lo sapevi?" (scelto il 5 nov) — short2.py
- Voce breve di Nico (15–22 s, ~55 parole), prima frase "Lo sapevi?" con Nico a schermo, ultime frasi con Nico.
- Il resto: scene dell'episodio sincronizzate frase per frase (SC), su sfondo sfocato, sottotitoli grandi parola per parola (giallo sulla parola corrente), chip LO SAPEVI? + episodio in alto, firma in basso, musica bassa.
- Solo fatti verificabili (cast, battute presenti nei sottotitoli).
