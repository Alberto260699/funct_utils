import cv2
from pathlib import Path
import json


cartella_faces = Path("faces")

if not cartella_faces.exists():
    print("La cartella faces non esiste.")
    exit()


recognizer = cv2.face.LBPHFaceRecognizer_create() #Local Binary Patterns Histograms: riconoscitore 
#LBPH lavora con immagini monocromatiche.

faces = []
labels = []

nomi = {}

id_persona = 0


for cartella_persona in cartella_faces.iterdir():

    if not cartella_persona.is_dir():
        continue

    nome = cartella_persona.name

    nomi[id_persona] = nome

    for file_immagine in cartella_persona.glob("*.jpg"):

        immagine = cv2.imread(
            str(file_immagine),
            cv2.IMREAD_GRAYSCALE
        )

        if immagine is None:
            continue

        faces.append(immagine)
        labels.append(id_persona)

    id_persona += 1


if len(faces) == 0:
    print("Nessuna immagine trovata.")
    exit()


print(f"Immagini trovate: {len(faces)}")
print(f"Persone trovate: {len(nomi)}")

print("Addestramento in corso...")

recognizer.train(faces, labels)

recognizer.save("modello.yml")


with open("nomi.json", "w", encoding="utf-8") as file:
    json.dump(
        nomi,
        file,
        ensure_ascii=False,
        indent=4
    )


print("Addestramento completato.")
print("Modello salvato in: modello.yml")
print("Nomi salvati in: nomi.json")