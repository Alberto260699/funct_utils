import numpy as np

def find_FWHM(a):
    """Calcola la larghezza a metà altezza (FWHM) di un segnale."""
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
    return FWHM_max - FWHM_min

def find_peaks(x):
    """Trova i picchi locali assoluti in un array."""
    x = np.abs(x)
    mask = (x[1:-1] >= x[:-2]) & (x[1:-1] >= x[2:])
    x_peaks = x[1:-1][mask]
    x_idx_peaks = [i + 1 for i, val in enumerate(mask) if val]
    return x_peaks, x_idx_peaks
