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

def find_peaks(x, trigger_max=None, trigger_min=None, mode='both'):
    '''
    Trova i massimi e/o minimi locali in un array.

    Args:
        x: array dei dati (1D)
        trigger_max: soglia minima per accettare un massimo (facoltativa)
        trigger_min: soglia massima per accettare un minimo (facoltativa, deve essere negativa o zero)
        mode: 'max', 'min', o 'both'

    Returns:
        dict con chiavi: 'max' e/o 'min', ognuna contenente:
            - 'values': np.array dei valori dei picchi
            - 'indices': np.array degli indici originali
    '''
    x = np.asarray(x)
    #x = sig.savgol_filter(x, 21, 3)
    result = {}

    if mode in ['max', 'both']:
        mask_max = (x[1:-1] >= x[:-2]) & (x[1:-1] >= x[2:])
        peak_indices_max = np.where(mask_max)[0] + 1
        peak_values_max = x[peak_indices_max]  # usa x originale!

        if trigger_max is not None:
            valid = peak_values_max > float(trigger_max)
            peak_indices_max = peak_indices_max[valid]
            peak_values_max = peak_values_max[valid]

        result['max'] = {'values': peak_values_max, 'indices': peak_indices_max}

    if mode in ['min', 'both']:
        mask_min = (x[1:-1] <= x[:-2]) & (x[1:-1] <= x[2:])
        peak_indices_min = np.where(mask_min)[0] + 1
        peak_values_min = x[peak_indices_min]  # usa x originale!

        if trigger_min is not None:
            valid = peak_values_min < float(trigger_min)
            peak_indices_min = peak_indices_min[valid]
            peak_values_min = peak_values_min[valid]

        result['min'] = {'values': peak_values_min, 'indices': peak_indices_min}

    return result
    
def find_max(x):
    '''Trova i massimi locali assoluti in un array'''
    x = np.asarray(x)
    #x = sig.savgol_filter(x, 21, 3)
    original_indices = np.arange(len(x))
    mask = (x[1:-1] >= x[:-2]) & (x[1:-1] >= x[2:])
    x_peaks = x[1:-1][mask]
    local_peak_indices = np.array([i + 1 for i, x_max in enumerate(mask) if x_max])
    x_idx_peaks = original_indices[local_peak_indices]
    return x_peaks, x_idx_peaks

def find_min(x):
    '''Trova i minimi locali assoluti in un array'''
    x = np.asarray(x)
    #x = sig.savgol_filter(x, 21, 3)
    original_indices = np.arange(len(x))
    mask = (x[1:-1] <= x[:-2]) & (x[1:-1] <= x[2:])
    x_peaks = x[1:-1][mask]
    local_peak_indices = np.array([i + 1 for i, x_min in enumerate(mask) if x_min])
    x_idx_peaks = original_indices[local_peak_indices]
    return x_peaks, x_idx_peaks

def fattoriale(n):
    '''Calcolo del fattoriale'''
    if n == 1:
        return 1
    else:
        return n * fattoriale(n - 1)