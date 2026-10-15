import csv
import sys
from pathlib import Path

def leggi_file(percorso):
	'''Legge le righe di un file in una lista, senza rimuovere i ritorni a capo.'''
	try:
		with open(percorso, 'r', encoding='utf-8', errors='replace') as f:
			return f.readlines()
	except FileNotFoundError:
		print(f'Errore: il file {percorso} non esiste.')
		sys.exit(1)

def confronta_file(file1, file2):
	'''Confronta due file riga per riga e restituisce una lista di risultati.'''
	righe1 = leggi_file(file1)
	righe2 = leggi_file(file2)

	risultati = []
	max_len = max(len(righe1), len(righe2))

	for i in range(max_len):
		r1 = righe1[i].rstrip('\n') if i < len(righe1) else ''
		r2 = righe2[i].rstrip('\n') if i < len(righe2) else ''

		if i >= len(righe1):
			stato = 'only_in_file2'
		elif i >= len(righe2):
			stato = 'only_in_file1'
		elif r1 == r2:
			stato = 'equal'
		else:
			stato = 'different'

		risultati.append({
			'line_number': i + 1,
			'file1_line': r1,
			'file2_line': r2,
			'status': stato
		})
	return risultati

def salva_csv(risultati, percorso_csv):
	'''Salva i risultati in un file CSV.'''
	with open(percorso_csv, 'w', newline='', encoding='utf-8') as csvfile:
		fieldnames = ['line_number', 'file1_line', 'file2_line', 'status']
		writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		writer.writeheader()
		for r in risultati:
			writer.writerow(r)

def main():
	print('=== Confronto riga per riga con report CSV ===')
	file1 = input('Percorso del primo file: ').strip()
	file2 = input('Percorso del secondo file: ').strip()
	output_csv = input('Percorso del file CSV di output: ').strip()

	risultati = confronta_file(file1, file2)
	salva_csv(risultati, output_csv)

	print(f'\nConfronto completato. Report salvato in: {output_csv}')
	print('Statistiche:')
	print(f'  Totale righe confrontate: {len(risultati)}')
	print(f'  Righe uguali: {sum(r['status']=='equal' for r in risultati)}')
	print(f'  Righe diverse: {sum(r['status']=='different' for r in risultati)}')
	print(f'  Solo nel primo file: {sum(r['status']=='only_in_file1' for r in risultati)}')
	print(f'  Solo nel secondo file: {sum(r['status']=='only_in_file2' for r in risultati)}')

if __name__ == '__main__':
	main()
