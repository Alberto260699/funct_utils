# ============================================================
# 1. ASCOLTO
# ============================================================

import speech_recognition as sr

recognizer = sr.Recognizer()

with sr.Microphone() as mic:
	print("Parla...")
	audio = recognizer.listen(mic)

comando = recognizer.recognize_google(audio, language="it-IT")

print("Hai detto:", comando)

# ============================================================
# 2. PARLATO
# ============================================================

import pyttsx3

#inizializza il motore di sintesi
engine = pyttsx3.init()

#stringa
testo = 'ciao, come va?'

engine.say(testo)

engine.runAndWait()

# ============================================================
# 2.1 SET DELLA VOCE
# ============================================================

import pyttsx3

def list_voices(engine):
	"""Stampa tutte le voci disponibili con ID e lingua."""
	voices = engine.getProperty('voices')
	for idx, voice in enumerate(voices):
		print(f"{idx}: {voice.name} | ID: {voice.id} | Lingua: {voice.languages}")

def set_voice(engine, voice_index):
	"""Imposta la voce usando l'indice della lista."""
	voices = engine.getProperty('voices')
	if 0 <= voice_index < len(voices):
		engine.setProperty('voice', voices[voice_index].id)
	else:
		raise ValueError("Indice voce non valido.")

def main():
	try:
		engine = pyttsx3.init()

		# Elenco voci disponibili
		print("Voci disponibili:")
		list_voices(engine)

		# Scegli la voce (esempio: indice 1)
		scelta = int(input("Inserisci l'indice della voce desiderata: "))
		set_voice(engine, scelta)

		# Imposta velocità e volume
		engine.setProperty('rate', 150)   # parole al minuto
		engine.setProperty('volume', 1.0) # da 0.0 a 1.0

		# Test
		engine.say("Ciao! Questa è la voce selezionata.")
		engine.runAndWait()

	except ValueError as ve:
		print(f"Errore: {ve}")
	except Exception as e:
		print(f"Si è verificato un errore: {e}")

if __name__ == "__main__":
	main()
