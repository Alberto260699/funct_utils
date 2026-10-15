import win32com.client as win32

# Avvia Excel
excel = win32.Dispatch('Excel.Application')
excel.Visible = False  # True per vedere Excel
'''
Visible = True
	- VEDI Excel aprirsi
	- Puoi controllare cosa sta succedendo
	- Utile per debug
	- Puoi interagire con Excel mentre gira

Visible = False
	+ Excel gira invisibile
	+ Più pulito e veloce
	+ Ideale per automazioni schedulate
	+ L’utente non si accorge di nulla
'''

# Apri il file con macro
wb = excel.Workbooks.Open(r'C:\percorso\file_macro.xlsm')

# Esecuzione semplice
excel.Application.Run('NomeMacro')

# Esecuzione modulo specifico
excel.Application.Run('Modulo1.NomeMacro')

# Esecuzione con parametri
excel.Application.Run('NomeMacro', 'test', 10)

# Salva e chiudi
wb.Save()
wb.Close()
excel.Quit()


#--------------------------------


import xlwings as xw

app = xw.App(visible=False)
wb = app.books.open(r'C:\percorso\file_macro.xlsm')
wb.macro('NomeMacro')()
wb.macro('Modulo1.NomeMacro')()
wb.macro('NomeMacro')('test', 10)
wb.save()
wb.close()
app.quit()


#--------------------------------
'''
Aspetto				pywin32						xlwings
Livello				Basso (COM puro)			Alto (API semplificata)
Facilità			❌ più complesso				✅ molto più semplice
Controllo Excel		🔥 totale					⚠️ alto ma astratto
Avvio macro			✅ sì						✅ sì
Parametri macro		✅ sì						✅ sì
Debug				❌ difficile					✅ più semplice
Stabilità			⚠️ può bloccarsi				✅ più robusto
Codice				Verboso						Pulito
Multi-file			❌ complesso					✅ semplice
Performance			🔥 leggermente migliori		⚠️ leggermente più lento
Windows				✅ solo Windows				✅ Windows / Mac
'''