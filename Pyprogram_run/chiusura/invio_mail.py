from email.message import EmailMessage
from pathlib import Path
import smtplib
import argparse
import logging
import sys
import re

LOG_FILE = 'invio_mail.log'

def setup_logging():
	logging.basicConfig(
		filename=LOG_FILE,
		level=logging.INFO,
		format='%(asctime)s [%(levelname)s] %(message)s'
	)

# Definisce il tipo mail e ne verifica la validità
def mail(value):
	if not re.match(r'^[^@]+@[^@]+\.[^@]+$', value):
		raise argparse.ArgumentTypeError(f'Email non valida: {value}')
	return value

def main():
	setup_logging()
	logging.info('Avvio invio mail')
	
	parser = argparse.ArgumentParser(
		description='Invio delle mail'
	)
	
	# Permette di passare più destinatari
	parser.add_argument('dest', nargs='+', type=mail, help='Destinatari') 
	parser.add_argument('--cc', nargs='+', type=mail, help='Destinatari in cc') 
	parser.add_argument('subject', nargs='+', type=str, help='Oggetto')
	parser.add_argument('context', nargs='+', type=str, help='Corpo')
	parser.add_argument('--attach', nargs='+', type=Path, default=None, help='Allegati')
	
	args = parser.parse_args()
	
	try:
		if not args.dest.exists() or not args.subject.exists() or not args.context.exists():
			logging.error("File non trovato: %s", args.file)
			sys.exit(1)
		
		msg = EmailMessage()
		msg['From'] = 'GBS_AllnetSupportoProduzione.it@generali.com'
		msg['To'] = '; '.join(args.dest)
		msg['Subject'] = ' '.join(args.subject)
		msg.set_content(' '.join(args.context))
		
		if args.cc:
			msg['Cc'] = '; '.join(args.cc)
		
		# Allegato
		if args.attach:
			for fl in args.attach:
				with open(fl, 'rb') as f:
					msg.add_attachment(
						f.read(),
						maintype='application',
						subtype='octet-stream',
						filename=fl.name
					)
		
		with smtplib.SMTP('smtp.office365.com', 587) as server:
			server.starttls()
			server.login('utente@azienda.it', 'password')				# sostituisci con credenziali reali
			server.send_message(msg)
		
		logging.info('Email con allegato inviata!')

if __name__ == '__main__':
	main()