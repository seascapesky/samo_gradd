#!/usr/bin/env python3
"""
Script per convertire un file JSON di LabelMe in una maschera PNG multi-classe,
gestendo anche i fori ("holes").
- Ogni poligono con label diversa ottiene un indice (0 = sfondo, 1,2,3... = altre classi).
- I poligoni con label "hole" vengono sottratti dalla regione dell'oggetto.
Usage:
    python labelme_json_to_mask_multi_with_holes.py path/to/file.json [--invert-coords]
"""

import argparse
import json
import sys

try:
    import labelme
    import numpy as np
    import PIL.Image
except ImportError:
    print("Assicurati di aver installato labelme, numpy e pillow.")
    print("Ad esempio: pip install labelme numpy pillow")
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("json_file", help="Percorso del file .json di LabelMe")
    parser.add_argument("--invert-coords", action="store_true",
                        help="Inverti x e y (a volte necessario se la maschera risulta nera).")
    args = parser.parse_args()

    # Carica il file JSON
    with open(args.json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    height = data["imageHeight"]
    width = data["imageWidth"]

    # Inizializza la maschera finale a 0 (sfondo)
    final_mask = np.zeros((height, width), dtype=np.uint8)

    # Mappa label -> valore intero (0 riservato allo sfondo)
    label_name_to_value = {"_background_": 0}

    # Raggruppa le forme per group_id.
    # Se una forma non ha group_id, ne viene assegnato uno univoco basato sul suo indice.
    groups = {}
    for idx, shape in enumerate(data["shapes"]):
        group_id = shape.get("group_id")
        if group_id is None:
            group_id = f"shape_{idx}"
        groups.setdefault(group_id, []).append(shape)

    # Processa ogni gruppo di forme
    for group_shapes in groups.values():
        # Separa le forme "outer" da quelle con label "hole"
        outer_shapes = [s for s in group_shapes if s["label"].lower() != "hole"]
        hole_shapes = [s for s in group_shapes if s["label"].lower() == "hole"]

        # Se non ci sono forme outer, salta questo gruppo
        if not outer_shapes:
            continue

        # Determina il label per il gruppo: si assume che tutte le outer abbiano lo stesso label;
        # viene usato il label del primo poligono outer.
        group_label = outer_shapes[0]["label"]
        if group_label not in label_name_to_value:
            label_name_to_value[group_label] = len(label_name_to_value)
        class_value = label_name_to_value[group_label]

        # Crea la maschera per il gruppo, inizialmente vuota (tutti False)
        group_mask = np.zeros((height, width), dtype=bool)

        # Unisci tutte le forme outer nel gruppo
        for shape in outer_shapes:
            original_points = shape["points"]
            if args.invert_coords:
                points = [(pt[1], pt[0]) for pt in original_points]
            else:
                points = original_points
            mask_i = labelme.utils.shape_to_mask(
                img_shape=(height, width),
                points=points,
                shape_type=shape.get("shape_type", "polygon")
            )
            group_mask |= mask_i

        # Sottrai i fori: per ogni forma hole, rimuovi i pixel corrispondenti
        for shape in hole_shapes:
            original_points = shape["points"]
            if args.invert_coords:
                points = [(pt[1], pt[0]) for pt in original_points]
            else:
                points = original_points
            hole_mask = labelme.utils.shape_to_mask(
                img_shape=(height, width),
                points=points,
                shape_type=shape.get("shape_type", "polygon")
            )
            group_mask &= ~hole_mask

        # Assegna il valore della classe nella maschera finale
        final_mask[group_mask] = class_value

    # Salva la maschera come file PNG
    out_file = args.json_file.rsplit(".", 1)[0] + "_mask.png"
    PIL.Image.fromarray(final_mask).save(out_file)
    print(f"Salvato in: {out_file}")

    # Stampa la mappatura label -> valore
    print("Mappatura delle classi:")
    for k, v in label_name_to_value.items():
        print(f"  {v}: {k}")

if __name__ == "__main__":
    main()
