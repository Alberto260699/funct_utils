import numpy as np
import scipy.signal as sig

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
    x = np.asarray(x)
    x = sig.savgol_filter(x, 21, 3)
    original_indices = np.arange(len(x))
    if trigger is not None and str(trigger).strip() != '' and str(trigger) != '0':
        trigger = float(trigger)
        if trigger > 0:
            mask = x > trigger
        else:
            mask = x < trigger
        x = x[mask]
        original_indices = original_indices[mask]  # aggiorna anche gli indici
    
    x = np.abs(x)
    mask = (x[1:-1] >= x[:-2]) & (x[1:-1] >= x[2:])
    x_peaks = x[1:-1][mask]
    local_peak_indices  = np.array([i + 1 for i, x_max in enumerate(mask) if x_max])
    x_idx_peaks = original_indices[local_peak_indices]
    return x_peaks, x_idx_peaks
    
def find_max(x):
    '''Trova i massimi locali assoluti in un array'''
    x = np.asarray(x)
    x = sig.savgol_filter(x, 21, 3)
    mask = (x[1:-1] >= x[:-2]) & (x[1:-1] >= x[2:])
    x_peaks = x[1:-1][mask]
    x_idx_peaks = np.array([i + 1 for i, x_max in enumerate(mask) if x_max])
    return x_peaks, x_idx_peaks

def find_min(x):
    '''Trova i minimi locali assoluti in un array'''
    x = np.asarray(x)
    x = sig.savgol_filter(x, 21, 3)
    mask = (x[1:-1] <= x[:-2]) & (x[1:-1] <= x[2:])
    x_peaks = x[1:-1][mask]
    x_idx_peaks = np.array([i + 1 for i, x_min in enumerate(mask) if x_min])
    return x_peaks, x_idx_peaks

def fattoriale(n):
    '''Calcolo del fattoriale'''
    if n == 1:
        return 1
    else:
        return n * fattoriale(n - 1)