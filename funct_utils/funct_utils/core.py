import numpy as np

def find_FWHM(a):
    '''Calcola la larghezza a metà altezza (FWHM) di un segnale e la relativa risoluzione'''
    x_idx = [i for i, x in enumerate(a) if x in a]
    peak = max(a)
    idx_peak = [i for i, x in enumerate(a) if x == peak]

    if not idx_peak:
        return None

    idx_FWHM_min = [idx for idx in x_idx if idx < idx_peak[0]]
    idx_FWHM_max = [idx for idx in x_idx if idx > idx_peak[0]]

    if not idx_FWHM_min or not idx_FWHM_max:
        return None

    FWHM_min = min(idx_FWHM_min, key=lambda idx: abs(a[idx] - peak / 2))
    FWHM_max = min(idx_FWHM_max, key=lambda idx: abs(a[idx] - peak / 2))
    return FWHM_max - FWHM_min, (FWHM_max - FWHM_min) / idx_peak

def find_peaks(x, trigger):
    '''Trova i picchi locali assoluti in un array'''
    if trigger == 0:
        pass
    elif trigger > 0:
        mask = x > trigger
        x = x[mask]
    else:
        mask = x < trigger
        x = x[mask]
    
    x = np.abs(x)
    mask = (x[1:-1] >= x[:-2]) & (x[1:-1] >= x[2:])
    x_peaks = x[1:-1][mask]
    x_idx_peaks = [i for i, x_max in enumerate(x) if x_max in x_peaks]
    return x_peaks, x_idx_peaks
    
def find_max(x):
    '''Trova i massimi locali assoluti in un array'''
    mask = (x[1:-1] >= x[:-2]) & (x[1:-1] >= x[2:])
    x_peaks = x[1:-1][mask]
    x_idx_peaks = [i for i, x_max in enumerate(x) if x_max in x_peaks]
    return x_peaks, x_idx_peaks

def find_min(x):
    '''Trova i minimi locali assoluti in un array'''
    mask = (x[1:-1] <= x[:-2]) & (x[1:-1] <= x[2:])
    x_peaks = x[1:-1][mask]
    x_idx_peaks = [i for i, x_min in enumerate(x) if x_min in x_peaks]
    return x_peaks, x_idx_peaks

def fattoriale(n):
    '''Calcolo del fattoriale'''
    if n == 1:
        return 1
    else:
        return n * fattoriale(n - 1)