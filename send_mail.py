'''
SENZA ALLEGATO
'''
import smtplib
from email.message import EmailMessage

# CREA MESSAGGIO
msg = EmailMessage()
msg["From"] = tuamail@gmail.com
msg["To"] = destinatario@gmail.com
msg["Subject"] = "Test email da Python"
msg.set_content("Ciao!\nQuesta email è stata inviata con Python.")
 
# CONNESSIONE SMTP
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
	server.login(tuamail@gmail.com, "PASSWORD_APP")
	server.send_message(msg)

print("Email inviata!")

'''
CON ALLEGATO
'''
from email.message import EmailMessage
import smtplib

msg = EmailMessage()
msg["From"] = tuamail@gmail.com
msg["To"] = destinatario@gmail.com
msg["Subject"] = "Email con allegato"
msg.set_content("In allegato trovi il file.")

# ALLEGATO
with open("file.pdf", "rb") as f:
	msg.add_attachment(
		f.read(),
		maintype="application",
		subtype="pdf",
		filename="file.pdf"
	)

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
	server.login(tuamail@gmail.com, "PASSWORD_APP")
	server.send_message(msg)

print("Email con allegato inviata!")

'''
SERVER AZIENDALE
'''
with smtplib.SMTP("smtp.office365.com", 587) as server:
	server.starttls()
	server.login(utente@azienda.it, "password")
	server.send_message(msg)