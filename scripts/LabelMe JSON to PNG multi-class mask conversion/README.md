Converte un **JSON di LabelMe** in una **maschera PNG mono-canale multi-classe**, gestendo anche i **fori**: qualsiasi shape con label `hole` viene **sottratta** dall’oggetto che la contiene.


**Requisiti**

pip install labelme numpy Pillow piexif

**Utilizzo**

python labelme_json_to_mask_multi_with_holes.py path/to/file.json
