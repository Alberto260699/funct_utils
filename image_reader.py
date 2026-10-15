#python ocr.py immagine.png
 
import cv2
import pytesseract
import argparse 

# Se sei su Windows e Tesseract non è nel PATH, decommenta:
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe" 

def estrai_testo(percorso_immagine):
    # Legge l'immagine
    img = cv2.imread(percorso_immagine)
 
    # Converte in scala di grigi
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
 
    # Migliora il contrasto
    gray = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]
 
    # OCR
    testo = pytesseract.image_to_string(gray, lang="ita+eng")
 
    return testo
 
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Estrae il testo da un'immagine")
    parser.add_argument("immagine", help="Percorso dell'immagine")
 
    args = parser.parse_args()
 
    testo = estrai_testo(args.immagine)
 
    print("\n=== TESTO ESTRATTO ===\n")
    print(testo)
 
 
 
#se vuoi solo i numeri
import cv2
import pytesseract
 
# Solo Windows:
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
 
img = cv2.imread("immagine.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)[1]
 
config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789'
 
testo = pytesseract.image_to_string(
    gray,
    config=config
)
 
numeri = [riga.strip() for riga in testo.splitlines() if riga.strip()]
 
print(numeri)