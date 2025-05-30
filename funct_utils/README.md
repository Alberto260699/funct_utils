# funct_utils

Una semplice libreria Python per il calcolo della larghezza a metà altezza (FWHM) e l'individuazione dei picchi nei dati numerici.

## Installazione

Clona la cartella e poi usa:

```bash
pip install .
```

oppure, per sviluppo:

```bash
pip install -e .
```

## Uso

```python
from funct_utils import find_FWHM, find_peaks

# Esempio di uso
a = [0, 1, 3, 7, 10, 7, 3, 1, 0]
print(find_FWHM(a))

x = [0, 1, 3, 2, 5, 1, 0]
peaks, indices = find_peaks(x, 1)
print(peaks, indices)
```
