import cv2
from pathlib import Path


# ============================================================
# 1. CHIEDI IL NOME DELLA PERSONA
# ============================================================

nome = input("Inserisci il nome della persona: ").strip()
 
if not nome:
	print("Nome non valido.")
	exit()


# ============================================================
# 2. CREA LA CARTELLA
# ============================================================

cartella = Path("faces") / nome
cartella.mkdir(parents=True, exist_ok=True)

print(f"\nLe immagini verranno salvate in: {cartella}")


# ============================================================
# 3. CARICA IL RILEVATORE DI VOLTI
# ============================================================

face_cascade = cv2.CascadeClassifier(
	cv2.data.haarcascades +
	"haarcascade_frontalface_default.xml"
)


# ============================================================
# 4. APRI LA WEBCAM
# ============================================================

video = cv2.VideoCapture(0)

if not video.isOpened():
	print("Errore: impossibile aprire la webcam.")
	exit()


# Numero progressivo delle immagini
numero_foto = 1

print("\nCOMANDI:")
print("SPAZIO = salva una foto")
print("ESC	= termina")
print()


# ============================================================
# 5. CICLO PRINCIPALE
# ============================================================

while True:

	# Acquisisce un frame dalla webcam
	ret, frame = video.read()

	if not ret:
		print("Errore nella lettura della webcam.")
		break

	# Converte l'immagine in scala di grigi
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# Cerca i volti
	faces = face_cascade.detectMultiScale(
		gray,
		scaleFactor=1.1,
		minNeighbors=5
	)


	# ========================================================
	# 6. DISEGNA IL RETTANGOLO SUI VOLTI
	# ========================================================

	for x, y, w, h in faces:

		cv2.rectangle(
			frame,
			(x, y),
			(x + w, y + h),
			(255, 0, 0),
			2
		)


	# ========================================================
	# 7. MOSTRA INFORMAZIONI SULLO SCHERMO
	# ========================================================

	testo = f"{nome} - Foto: {numero_foto}"

	cv2.putText(
		frame,
		testo,
		(10, 30),
		cv2.FONT_HERSHEY_SIMPLEX,
		0.8,
		(255, 255, 255),
		2
	)

	cv2.putText(
		frame,
		"SPAZIO = salva | ESC = esci",
		(10, frame.shape[0] - 20),
		cv2.FONT_HERSHEY_SIMPLEX,
		0.6,
		(255, 255, 255),
		2
	)


	# ========================================================
	# 8. MOSTRA LA WEBCAM
	# ========================================================

	cv2.imshow("Registrazione volto", frame)


	# ========================================================
	# 9. CONTROLLA LA TASTIERA
	# ========================================================

	tasto = cv2.waitKey(1) & 0xFF


	# ESC
	if tasto == 27:
		break


	# SPAZIO
	if tasto == 32:

		# Salva solamente se è stato trovato almeno un volto
		if len(faces) > 0:

			# Prendiamo il primo volto trovato
			x, y, w, h = faces[0]

			# Ritaglia il volto
			face = frame[y:y+h, x:x+w]

			# Nome del file
			nome_file = cartella / f"{numero_foto:03d}.jpg"

			# Salva il volto
			cv2.imwrite(str(nome_file), face)

			print(f"Salvata: {nome_file}")

			numero_foto += 1

		else:
			print("Nessun volto rilevato. Foto non salvata.")


# ============================================================
# 10. CHIUDI TUTTO
# ============================================================

cv2.destroyAllWindows()
video.release()

print(f"\nRegistrazione terminata.")
print(f"Immagini salvate: {numero_foto - 1}")