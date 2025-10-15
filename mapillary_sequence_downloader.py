# Script che scarica tutte le immagini di una sequenza Mapillary,
# inserisce nei file JPEG i metadati EXIF GPS (lat, lon) e salva.

import os
import requests
import json
from PIL import Image
import piexif
from io import BytesIO

def add_gps_info_to_image_data(latitude, longitude):
    def convert_to_degrees(value):
        d = int(value)
        m = int((value - d) * 60)
        s = (value - d - m/60) * 3600
        return d, m, s

    lat_deg = convert_to_degrees(latitude)
    lon_deg = convert_to_degrees(longitude)

    gps_ifd = {
        piexif.GPSIFD.GPSLatitudeRef: 'N' if latitude >= 0 else 'S',
        piexif.GPSIFD.GPSLatitude: [(lat_deg[0], 1), (lat_deg[1], 1), (int(lat_deg[2]*100), 100)],
        piexif.GPSIFD.GPSLongitudeRef: 'E' if longitude >= 0 else 'W',
        piexif.GPSIFD.GPSLongitude: [(lon_deg[0], 1), (lon_deg[1], 1), (int(lon_deg[2]*100), 100)],
    }

    exif_dict = {"GPS": gps_ifd}
    exif_bytes = piexif.dump(exif_dict)
    return exif_bytes

# Configura i parametri
access_token = 'MLY|XXXXXXXXXXXXXXXX|XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'      # Token Mapillary
sequence_id = 'XXXXXXXXXXXXXXXXXXXXX'                                       # ID della sequenza da scaricare
header = {'Authorization': f'OAuth {access_token}'}
base_url = f"https://graph.mapillary.com/image_ids?sequence_id={sequence_id}&limit=500"

# Crea la directory di download
output_dir = f"downloads/{sequence_id}"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Recupera tutte le immagini della sequenza con paginazione
url = base_url
all_images = []

while url:
    r = requests.get(url, headers=header)
    data = r.json()

    # Aggiunge i risultati alla lista
    if "data" in data:
        all_images.extend(data["data"])
    
    # Controlla se c'è una pagina successiva
    if "paging" in data and "next" in data["paging"]:
        url = data["paging"]["next"]
    else:
        url = None

print(f"Numero totale di immagini trovate: {len(all_images)}")

# Scarica ogni immagine
for img in all_images:
    img_id = img["id"]
    image_url = f"https://graph.mapillary.com/{img_id}?fields=thumb_original_url,geometry"
    img_r = requests.get(image_url, headers=header)
    img_data = img_r.json()

    if "thumb_original_url" not in img_data or "geometry" not in img_data:
        print(f"Errore con l'immagine {img_id}: URL o geometria mancante.")
        continue

    image_get_url = img_data['thumb_original_url']
    lon, lat = img_data['geometry']['coordinates']

    # Scarica e salva l'immagine
    try:
        image_data = requests.get(image_get_url, stream=True).content
        exif_bytes = add_gps_info_to_image_data(lat, lon)
        image = Image.open(BytesIO(image_data))
        output_path = os.path.join(output_dir, f"{img_id}.jpg")
        image.save(output_path, exif=exif_bytes)
        print(f"Immagine salvata: {output_path}")
    except Exception as e:
        print(f"Errore nel download o salvataggio dell'immagine {img_id}: {e}")
