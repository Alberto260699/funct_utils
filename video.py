import cv2
video=cv2.VideoCapture(0) #apre una connessione con la webcam principale
while True:
	retu, frame=video.read() #redu indica se la lettura è andata a buon fine, frame è l'immagine
	cv2.imshow('frame',frame) #mostra l'immagine
	if cv2.waitKey(1) & 0xFF == 27: #27 è il tasto ESC altrimenti puoi usare --> ord('a')
			break

cv2.destroyAllWindows()
video.release()

'''
tasto = cv2.waitKey(1)	   # Leggi la tastiera
codice_tasto = tasto & 0xFF  # Ottieni il codice del tasto

if codice_tasto == 97:		# 97 è 'a'
	break					 # Esci dal while
'''


# ----------------------------------------

import cv2

def click(event, x, y, flags, param):
	if event == cv2.EVENT_LBUTTONDOWN:
		print("Hai cliccato:", x, y)

cv2.namedWindow("Immagine")
cv2.setMouseCallback("Immagine", click)

immagine = cv2.imread("foto.jpg")

while True:
	cv2.imshow("Immagine", immagine)
	
	if cv2.waitKey(1) & 0xFF == 27:
		break

cv2.destroyAllWindows()


#--------------------------------------------
# riconoscimento facciale
#--------------------------------------------
import cv2

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
video = cv2.VideoCapture(0)

while True:
	ret, frame = video.read()
	
	if not ret:
		break
	
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	
	faces = face_cascade.detectMultiScale(
		gray,
		scaleFactor=1.1,
		minNeighbors=5
	)
	
	for x, y, w, h in faces:
		cv2.rectangle(
			frame,
			(x, y),
			(x + w, y + h),
			(255, 0, 0),
			2
		)
	
	cv2.imshow("Face detection", frame)
	
	if cv2.waitKey(1) & 0xFF == 27:
		break

cv2.destroyAllWindows()
video.release()