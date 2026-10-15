import sys
import subprocess
import shutil
import itertools				# per creare una sequenza infinita di caratteri
import threading			 	# per eseguire l'animazione in parallelo rispetto all'attività principale
import time
import xlwings as xw
from pathlib import Path		# per spostarsi tra le cartelle, consigliato anzichè os
import json
 
def animate_loading():
	for c in itertools.cycle(['|', '/', '-', '\\']):
		if stop_loading:
			break
		sys.stdout.write('\rCaricamento' + c)
		sys.stdout.flush()
		time.sleep(0.1)


#######################################################
################# Variabili generali ##################
#######################################################
orig_path = Path.cwd()

chius_path = orig_path / 'da Riccardo' / 'dati per chiusura'
path_722 = orig_path / 'da Mariotti' / '722 calcoli'
fonti_path = orig_path / 'da Mariotti' / 'dettaglio fondi fonti'
plc_path = orig_path / 'da Mariotti' / 'plc calcoli'
excel_path = orig_path / 'Fogli Excel Automatici' / 'Versione mppdbp02' / 'ARCHIVIO FOGLI EXCEL2023'

file_722 = 'Foglio quadratura Alleanza.xls'
quadr_file = 'Piano dei conti 722 723 dal 202407.xls'
fondi_PIP = 'Report Dettaglio Fondi722 Polizze PIP.xls'
fondi_AM = 'Report Fondi Fonti AlMeglio.xls'
macro_751_722 = 'Quadratura 751-722 - GAR.xlsm'
macro_FD = 'Report Fondi FuturoDoro.xlsm'
macro_VF = 'Report Fondi ValoreFuturo.xlsm'

var_chius = int(input('Quale chiusura stai effettuando (YYYYMM): '))
chius_prec = var_chius - 1
var_chius = str(var_chius)
chius_prec = str(chius_prec)

delete_file = []
rename_file = {	f'Q15.Rimb.PIP.{var_chius[:4]}.{chius_prec[-2:]}': f'Q15.Rimb.PIP.{var_chius[:4]}.{var_chius[-2:]}',
				f'Q17.Rimborsi Tasse SR {var_chius[:4]}.{chius_prec[-2:]}': f'Q17.Rimborsi Tasse SR {var_chius[:4]}.{var_chius[-2:]}',
				f'Q18.Rimborsi Valore Futuro {var_chius[:4]}.{chius_prec[-2:]}': f'Q18.Rimborsi Valore Futuro {var_chius[:4]}.{var_chius[-2:]}',
				f'Q19.Rimborsi Futuro Oro {var_chius[:4]}.{chius_prec[-2:]}': f'Q19.Rimborsi Futuro Oro {var_chius[:4]}.{var_chius[-2:]}',
				f'Rimborsi Tasse SR {var_chius[:4]}.{chius_prec[-2:]}': f'Rimborsi Tasse SR {var_chius[:4]}.{var_chius[-2:]}'
			}


#######################################################
############# Gestione delle cartelle #################
#######################################################
shutil.copytree(chius_path / chius_prec, chius_path / var_chius)
shutil.copytree(path_722 / chius_prec, path_722 / var_chius)
shutil.copytree(fonti_path / chius_prec, fonti_path / var_chius)
shutil.copytree(plc_path / chius_prec, plc_path / var_chius)


#eliminare
result = subprocess.run(
	[
		sys.executable,
		'cambio_file.py',
		'--mode', 'delete',
		json.dumps(delete_file),
		'--path', str(chius_path / var_chius)
	],
	cwd = chius_path / var_chius
)

if result.returncode == 0:
	print(f'SUCCESSO: {file_722} completato')
else:
	print(f'ERRORE IMPREVISTO {file_722}(code={result.returncode})')
	sys.exit(result.returncode)

#rename
result = subprocess.run(
	[
		sys.executable,
		'cambio_file.py',
		'--mode', 'rename',
		json.dumps(rename_file),
		'--path', str(chius_path / var_chius)
	],
	cwd = chius_path / var_chius
)

if result.returncode == 0:
	print(f'SUCCESSO: {file_722} completato')
else:
	print(f'ERRORE IMPREVISTO {file_722}(code={result.returncode})')
	sys.exit(result.returncode)



#######################################################
## Lancio fogli excel (vengono salvati in Documents) ##
#######################################################
result = subprocess.run(
	[
		sys.executable,
		'quadratura.py',
		str(excel_path / quadr_file)
	],
	check=False,			# non solleva eccezione se returncode != 0
	capture_output=True,	# cattura stdout e stderr
	text=True				# decodifica l’output come stringa (non byte)
)
'''
ATTENZIONE: sarebbero inutili questi flag perchè nel programma che vai a lanciare sta facendo il logging
'''

# Gestione return code
if result.returncode == 0:
	print(f'SUCCESSO: {quadr_file} completato')
else:
	print(f'ERRORE IMPREVISTO {quadr_file}(code={result.returncode})')
	sys.exit(result.returncode)

result = subprocess.run(
	[
		sys.executable,
		'quadratura.py',
		str(excel_path / file_722)
	]
)

if result.returncode == 0:
	print(f'SUCCESSO: {file_722} completato')
else:
	print(f'ERRORE IMPREVISTO {file_722}(code={result.returncode})')
	sys.exit(result.returncode)

'''
spostare e rinominare nelle cartelle corrette
'''



#######################################################
################# Invio delle mail ####################
#######################################################
result = subprocess.run(
	[
		sys.executable,
		'invio_mail.py',
# Vengono trattati come inserimenti multipli
		'dest', 'giuseppe.introcaso@generali.com', 'Alessandra.Oggioni@alleanza.it', 'stefano.manera@generali.com', 'massimiliano.sala@generali.com', 'mariateresa.ruzza@generali.com', 'cristiano.raffaele@accenture.com', 'Sistemi.Alleanza.SP@accenture.com',
		'--cc', 'massimo.mauriello@generali.com', 'mara.liperoti@generali.com', 'Sistemi.Alleanza.CTB@accenture.com', 'monica.ominetti@generali.com', 'GBS_AllnetSupportoProduzione.it@generali.com', 'silvia.derossi@generali.com',
		'subject', f'Foglio di quadratura {var_chius[-2:]}/{var_chius[:4]}',
# Se metti gli apici allora viene trattato come elemento singolo
		'context', f'Buongiorno\nVi allego il foglio di quadratura vita/danni per il mese di {var_chius[-2:]}/{var_chius[:4]}.\nI dati potrebbero subire piccole rettifiche in seguito ai risultati comunicati nel Report 722, ancora in esame.\nA disposizione.',
		'--attach', str(Path('C:\Users\Samuele') / 'Documents' / f'Foglio quadratura Alleanza.{var_chius[:4]}-{var_chius[-2:]}-01.xls')
	]
)

if result.returncode == 0:
	print(f'SUCCESSO: Foglio quadratura Alleanza.{var_chius[:4]}-{var_chius[-2:]}-01.xls completato')
else:
	print(f'ERRORE IMPREVISTO in Foglio quadratura Alleanza.{var_chius[:4]}-{var_chius[-2:]}-01.xls (code={result.returncode})')
	sys.exit(result.returncode)

result = subprocess.run(
	[
		sys.executable,
		'invio_mail.py',
		'dest', 'Sistemi.Alleanza.SP@accenture.com', 'cristiano.raffaele@accenture.com',
		'--cc', 'GBS_AllnetSupportoProduzione.it@generali.com', 'silvia.derossi@generali.com',
		'subject', f'Piano dei conti 722-723 {var_chius}',
		'context', f'Buongiorno\nAllego quanto in oggeto',
		'file', str(Path('C:\Users\Samuele') / 'Documents' / f'Piano dei conti 722 723 dal 202407.{var_chius}.xls')
	]
)

if result.returncode == 0:
	print(f'SUCCESSO: Piano dei conti 722 723 dal 202407.{var_chius}.xls completato')
else:
	print(f'ERRORE IMPREVISTO in Piano dei conti 722 723 dal 202407.{var_chius}.xls (code={result.returncode})')
	sys.exit(result.returncode)



#######################################################
################# Lancio REPORT.sh ####################
#######################################################
print('Lanciare da Schema-L il processo REPORT.sh')
while True:
	result = str(input('Processo completato? Y/N'))
	if result == 'Y':
		break
	else:
		continue



#######################################################
################ Lancio download.vbs ##################
#######################################################
result = subprocess.run(
	["cscript", "download.vbs"],
	check=True,
	cwd = chius_path / var_chius		# esegue il comando nella cartella target
)



#######################################################
######## Lancio Quadratura 751-722 - GAR.xlsm #########
#######################################################
stop_loading = False
t = threading.Thread(target=animate_loading)
t.start() 

app = xw.App(visible=False)
wb = app.books.open(chius_path / var_chius / macro_751_722)
wb.macro('Start_Macro')()
#wb.save()
wb.close()
app.quit()

app = xw.App(visible=False)
wb = app.books.open(chius_path / var_chius / macro_FD)
wb.macro('macro1')()
#wb.save()
wb.close()
app.quit()

app = xw.App(visible=False)
wb = app.books.open(chius_path / var_chius / macro_VF)
wb.macro('macro1')()
#wb.save()
wb.close()
app.quit()

stop_loading = True
t.join()
print("\nCaricamento completato delle macro di quadratura!")



#######################################################
## Lancio fogli excel (salvataggio in dir corrente) ###
#######################################################
result = subprocess.run(
	[
		sys.executable,
		'dettaglio_fondi.py',
		str(chius_path / var_chius / fondi_PIP)
	]
)

# Gestione return code
if result.returncode == 0:
	print(f'SUCCESSO: {fondi_PIP} completato')
else:
	print(f'ERRORE IMPREVISTO {fondi_PIP}(code={result.returncode})')
	sys.exit(result.returncode)

result = subprocess.run(
	[
		sys.executable,
		'dettaglio_fondi.py',
		str(chius_path / var_chius / fondi_AM)
	]
)

# Gestione return code
if result.returncode == 0:
	print(f'SUCCESSO: {fondi_AM} completato')
else:
	print(f'ERRORE IMPREVISTO {fondi_AM}(code={result.returncode})')
	sys.exit(result.returncode)
	
print('Controllare i report, fare di nuovo le autosomme e controllare il mese nel file')
while True:
	result = str(input('Processo completato? Y/N'))
	if result == 'Y':
		break
	else:
		continue



#######################################################
################# Invio delle mail ####################
#######################################################
result = subprocess.run(
	[
		sys.executable,
		'invio_mail.py',
		'dest', 'mara.liperoti@generali.com', 'Sistemi.Alleanza.CTB@accenture.com', 'cristiano.raffaele@accenture.com',
		'--cc', 'massimo.mauriello@generali.com', 'annarita.caccia@accenture.com', 'andrea.frigo@accenture.com', 'Sistemi.Alleanza.SP@accenture.com', 'monica.ominetti@generali.com', 'GBS_AllnetSupportoProduzione.it@generali.com', 'silvia.derossi@generali.com',
		'subject', f'Chiusura contabile {var_chius[-2:]}/{var_chius[:4]}',
		'context', f'Buongiorno\nin allegato il dettaglio della quadratura tra Report 751 e Report 722 ed i report dettaglio fondi/fonti aggiornati per il mese contabile di {var_chius[-2:]}/{var_chius[:4]}\na disposizione,\nAlberto Sala.',
		'file', str(chius_path / var_chius / '.xls'.join('_'.join('invio_Report_751_722_GAR_01_', var_chius[-2:], var_chius[:4]))) 
				str(chius_path / var_chius/ '.xls'.join('_'.join('invio_report_fondi_almeglio', var_chius))) 
				str(chius_path / var_chius / '.xls'.join('_'.join('invio_report_fondi_pip', var_chius))) 
				str(chius_path / var_chius / '.xls'.join('_'.join('invio_report_fondi_va', var_chius))) 
				str(chius_path / var_chius / '.xls'.join('_'.join('invio_report_fondi_fd', var_chius)))
	]
)

# Gestione return code
if result.returncode == 0:
	print(f'SUCCESSO: dei report fondi completato')
else:
	print(f'ERRORE IMPREVISTO in report fondi (code={result.returncode})')
	sys.exit(result.returncode)



#######################################################
################ Lancio delle Query ###################
#######################################################
print('Lanciare ed estrarre le query da Mariotti/722 calcoli')
while True:
	result = str(input('Processo completato? Y/N'))
	if result == 'Y':
		break
	else:
		continue