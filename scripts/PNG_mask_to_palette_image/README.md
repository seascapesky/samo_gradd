Questo script carica una maschera **mono-canale** con indici di classe (`ID_mask.png`), applica una **palette di colori** (0=nero/background, 1=verde/guardrail_ok, 2=rosso/guardrail_damaged) e la converte in **RGB** per una rapida visualizzazione.



**Requisiti**

pacchetti `Pillow numpy`

**Personalizzazione palette**

Modifica la lista palette aggiungendo terne (R, G, B) per ogni classe:

0: 0, 0, 0 – background

1: 0, 255, 0 – guardrail_ok

2: 255, 0, 0 – guardrail_damaged

Il codice completa automaticamente la palette fino a 256 colori (768 valori).
