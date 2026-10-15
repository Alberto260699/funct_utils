```python
import cv2
import json


# ==========================
# 1. CARICAMENTO DEL MODELLO
# ==========================

recognizer = cv2.face.LBPHFaceRecognizer_create()

recognizer.read("modello.yml")


# ==========================
# 2. CARICAMENTO DEI NOMI
# ==========================

with open("nomi.json", "r", encoding="utf-8") as file:
    nomi = json.load(file)


# ==========================
# 3. RILEVATORE DEI VOLTI
# ==========================

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)


# ==========================
# 4. APERTURA WEBCAM
# ==========================

video = cv2.VideoCapture(0)

if not video.isOpened():
    print("Errore: impossibile aprire la webcam.")
    exit()


# ==========================
# 5. SOGLIA DI RICONOSCIMENTO
# ==========================

soglia = 70


# ==========================
# 6. CICLO PRINCIPALE
# ==========================

while True:

    ret, frame = video.read()

    if not ret:
        print("Errore nella lettura della webcam.")
        break


    # Conversione in scala di grigi
    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )


    # Rilevamento dei volti
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5
    )


    # Analizziamo ogni volto
    for x, y, w, h in faces:

        # Ritagliamo il volto
        face = gray[y:y+h, x:x+w]


        # Riconoscimento
        id_persona, confidence = recognizer.predict(face)


        # Controlliamo la soglia
        if confidence < soglia:

            nome = nomi[str(id_persona)]

        else:

            nome = "Sconosciuto"


        # Disegniamo il rettangolo
        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (255, 0, 0),
            2
        )


        # Scriviamo il nome
        cv2.putText(
            frame,
            f"{nome} ({confidence:.1f})",
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )


    # Mostriamo il risultato
    cv2.imshow(
        "Riconoscimento facciale",
        frame
    )


    # ESC per uscire
    if cv2.waitKey(1) & 0xFF == 27:
        break


# ==========================
# 7. CHIUSURA
# ==========================

video.release()
cv2.destroyAllWindows()
```
