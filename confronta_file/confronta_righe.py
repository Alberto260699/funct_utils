'''
# Confronto base (semplice):
	python confronta_righe.py fileA.txt fileB.txt

# Confronto ignorando spazi e maiuscole
	python confronta_righe.py fileA.txt fileB.txt --ignore-space --ignore-case

# Mostra output in stile diff (unified) e salva report
	python confronta_righe.py fileA.txt fileB.txt --mode diff --report diff_report.txt
'''

#si chiama shebang (o hashbang) ed è una istruzione speciale che indica con quale interprete eseguire lo script quando lo lanci come un programma.
#!/usr/bin/env python3
'''
confronta_righe.py

Confronta due file riga per riga.
Uso:
	python confronta_righe.py file1.txt file2.txt [--ignore-space] [--ignore-case]
											  [--mode simple|diff] [--context N]
											  [--report report.txt]
'''

import argparse
import sys
import difflib
from pathlib import Path

def read_lines(path):
	# Legge tutte le righe mantenendo '\n' alla fine per diff leggibile.
	with open(path, 'r', encoding='utf-8', errors='replace') as f:
		return f.readlines()

def normalize_line(line, ignore_space=False, ignore_case=False):
	s = line
	if ignore_space:
		# rimuove spazi iniziali/finali e normalizza spazi interni multipli in uno
		s = ' '.join(s.split())
	if ignore_case:
		s = s.lower()
	return s

def simple_compare(lines1, lines2, ignore_space=False, ignore_case=False, show_identical=False):
	'''
	Confronto riga per riga semplice. Restituisce lista di tuple (num_riga, linea1, linea2, equal_bool)
	linee contate a partire da 1. Se un file è più corto, linea vuota mostrata per il file mancante.
	'''
	results = []
	maxlen = max(len(lines1), len(lines2))
	for i in range(maxlen):
		l1 = lines1[i] if i < len(lines1) else ''
		l2 = lines2[i] if i < len(lines2) else ''
		n1 = normalize_line(l1, ignore_space, ignore_case)
		n2 = normalize_line(l2, ignore_space, ignore_case)
		equal = (n1 == n2)
		if not equal or show_identical:
			results.append((i+1, l1, l2, equal))
	return results

def print_simple(results):
	for num, l1, l2, equal in results:
		if equal:
			print(f'{num:6d}  (=) {l1.rstrip()}')
		else:
			print(f'{num:6d}  (<) {l1.rstrip()}')
			print(f'{'':8s}  (>) {l2.rstrip()}')
			print('-' * 60)

def print_unified(path1, path2, lines1, lines2, ignore_space=False, ignore_case=False, context=3):
	# Se ignoring, dobbiamo passare le righe normalizzate per il diff ma mantenere testo originale nella label.
	if ignore_space or ignore_case:
		# Normalizziamo senza alterare i ritorni a capo per difflib comparatore.
		norm1 = [normalize_line(l, ignore_space, ignore_case) for l in lines1]
		norm2 = [normalize_line(l, ignore_space, ignore_case) for l in lines2]
		# difflib lavora meglio con sequenze di stringhe: ma vogliamo che l'output mostri le righe originali.
		# Qui costruiremo un diff sulle righe normalizzate ma mostreremo l'originale usando indices.
		# Semplice strategia: se normalizzato differisce -> mostriamo unified diff sulle originali.
		# Quindi usiamo difflib.unified_diff direttamente sulle originali: è più leggibile.
		pass

	ud = difflib.unified_diff(
		lines1, lines2,
		fromfile=str(path1),
		tofile=str(path2),
		lineterm='',
		n=context
	)
	for line in ud:
		print(line)

def write_report(path, content_lines):
	with open(path, 'w', encoding='utf-8') as f:
		for line in content_lines:
			f.write(line + '\n')

def main():
	parser = argparse.ArgumentParser(description='Confronta due file riga per riga.')
	parser.add_argument('file1', type=Path, help='Primo file')
	parser.add_argument('file2', type=Path, help='Secondo file')
	parser.add_argument('--ignore-space', action='store_true', help='Ignora spazi iniziali/finali e sequenze multiple di spazi')
	parser.add_argument('--ignore-case', action='store_true', help='Ignora differenze tra maiuscole/minuscole')
	parser.add_argument('--mode', choices=['simple', 'diff'], default='simple',
						help="Modalità di output: 'simple' (mostra righe con differenze) o 'diff' (unified diff)")
	parser.add_argument('--context', type=int, default=3, help='Numero di righe di contesto per unified diff (default 3)')
	parser.add_argument('--report', type=Path, default=None, help='Salva il report su file di testo')
	parser.add_argument('--show-identical', action='store_true', help='Nella modalità semplice mostra anche le righe identiche')
	
	args = parser.parse_args()

	if not args.file1.exists() or not args.file2.exists():
		print('Errore: uno o entrambi i file non esistono.', file=sys.stderr)
		sys.exit(2)

	lines1 = read_lines(args.file1)
	lines2 = read_lines(args.file2)

	if args.mode == 'simple':
		results = simple_compare(lines1, lines2, args.ignore_space, args.ignore_case, args.show_identical)
		# Prepariamo anche il contenuto testuale del report (se richiesto)
		out_lines = []
		for num, l1, l2, equal in results:
			if equal:
				out_lines.append(f'{num:6d}  (=) {l1.rstrip()}')
			else:
				out_lines.append(f'{num:6d}  (<) {l1.rstrip()}')
				out_lines.append(f'{'':8s}  (>) {l2.rstrip()}')
				out_lines.append('-' * 60)
		# Stampa a video
		print(f'Confronto semplice: {args.file1} vs {args.file2}')
		print('-' * 60)
		print('\n'.join(out_lines))
		# Salvataggio report
		if args.report:
			write_report(args.report, out_lines)
			print(f'\nReport salvato in: {args.report}')
	else:
		# modalità diff unificata
		print(f'Unified diff: {args.file1} vs {args.file2} (context={args.context})')
		print('-' * 60)
		# Se ci sono opzioni di ignore, per leggibilità useremo difflib sulle righe originali:
		# l'utente dovrebbe sapere che ignore_* ha effetto sul confronto logico nella modalità simple,
		# ma unified diff mostra cambi reali. Qui applichiamo normalize per decidere se una riga è
		# considerata 'uguale' e se tutte le righe normalizzate sono uguali stampiamo 'Nessuna differenza'.
		if args.ignore_space or args.ignore_case:
			# Confronto logico: determiniamo prima se differiscono a livello normalizzato
			norm1 = [normalize_line(l, args.ignore_space, args.ignore_case) for l in lines1]
			norm2 = [normalize_line(l, args.ignore_space, args.ignore_case) for l in lines2]
			if norm1 == norm2:
				print('Nessuna differenza significativa con le opzioni di normalizzazione attivate.')
				if args.report:
					write_report(args.report, ['Nessuna differenza significativa.'])
					print(f'Report salvato in: {args.report}')
				return
			# Altrimenti mostriamo il diff classico (suggerimento: le differenze sono significative)
		print_unified(args.file1, args.file2, lines1, lines2, args.ignore_space, args.ignore_case, args.context)
		if args.report:
			# raccogliamo il diff in memoria e salviamo
			ud = list(difflib.unified_diff(lines1, lines2, fromfile=str(args.file1), tofile=str(args.file2), lineterm='', n=args.context))
			write_report(args.report, ud)
			print(f'\nReport salvato in: {args.report}')

if __name__ == '__main__':
	main()
