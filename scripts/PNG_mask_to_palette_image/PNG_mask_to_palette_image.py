# Importa il modulo Image dalla libreria Pillow per gestire le immagini
import PIL.Image  

# Importa NumPy, una libreria per la gestione di array e operazioni matematiche
import numpy as np
# Carica la maschera salvata
mask = np.array(PIL.Image.open("ID_mask.png"))  #apre il file PNG della maschera come un oggetto immagine e la converte in un array NumPy, facilitando eventuali manipolazioni numeriche
mask_img = PIL.Image.fromarray(mask).convert("P")            #crea un oggetto immagine Pillow a partire dall'array "mask", converte l'immagine in modalità "P" (palettizzata), in cui ogni pixel contiene un indice che fa riferimento a una palette di colori

# Definisce una palette: ogni gruppo di tre valori rappresenta un colore (R, G, B)
palette = [
    0, 0, 0,      # Classe 0: nero (Background)
    0, 255, 0,    # Classe 1: verde (Guardrail_ok)
    255, 0, 0,    # Classe 2: rosso (Guardrail_Damaged)
    # Si possono aggiungere altri colori se ci sono più classi
    
]

#   La lista "palette" contiene i colori che saranno associati agli indici dell'immagine.
#   Ogni tre valori consecutivi rappresentano il canale Rosso, Verde e Blu di un colore.
#   Qui sono definiti tre colori: nero per lo sfondo, verde per la prima classe, e rosso per la seconda classe.

# Completare la palette fino a 256 colori (256*3 = 768 valori)
#  Le immagini palettizzate in modalità "P" richiedono una palette composta da 768 valori (256 colori x 3 canali).
#  Se la lista "palette" attuale contiene meno di 768 valori, questo comando aggiunge zeri (cioè il colore nero) fino a raggiungere i 768 valori totali.

palette += [0] * (768 - len(palette))

# Il metodo putpalette() applica la palette definita all'immagine "mask_img".
# Adesso, ogni indice presente nell'immagine verrà mappato al colore corrispondente nella palette.

mask_img.putpalette(palette)

# Converte l'immagine dalla modalità "P" (indicizzata) a "RGB" (true color).
# Questa conversione applica la palette e restituisce un'immagine in cui ogni pixel ha i valori diretti dei canali R, G, B, rendendo l'immagine facilmente visualizzabile a colori.

mask_img = mask_img.convert("RGB")

# Mostra l'immagine risultante in una finestra di visualizzazione.

mask_img.show()
