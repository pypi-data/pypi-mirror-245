import numpy as np
from scipy.signal import hanning, linregress
from scipy.fft import fft


def pwrspc(time, quantity, noline=False, nohanning=False, bin=3, notperhz=False):
    """
    Compute the power spectrum of a given signal.

    Parameters:
    time (array-like):
        The time array.
    quantity (array-like):
        The function for which you want to obtain a power spectrum.
    noline (bool, optional):
        If True, no straight line is subtracted. Default is False.
    nohanning (bool, optional):
        If True, no Hanning window is applied. Default is False.
    bin (int, optional):
        Bin size for binning of the data. Default is 3.
    notperhz (bool, optional):
        If True, the output units are the square of the input units. Default is False.

    Returns:
    tuple: Contains two arrays - frequencies and the corresponding power spectrum.

    Note:
    The function assumes equally spaced time intervals.
    This function is similar to the IDL function pwrspc.pro.
    """

    # Convert inputs to numpy arrays and normalize time
    t = np.array(time) - time[0]
    x = np.array(quantity)

    # Subtract a straight line if noline is not set
    if not noline:
        slope, intercept = linregress(t, x)[:2]
        x -= slope * t + intercept

    # Apply a Hanning window if nohanning is not set
    if not nohanning:
        window = hanning(len(x))
        x *= window

    # Ensure even number of data points
    if len(t) % 2 != 0:
        t = t[:-1]
        x = x[:-1]

    # Compute the FFT and power spectrum
    xs2 = np.abs(fft(x)) ** 2
    bign = len(t)
    dfreq = 1.0 / (np.median(np.diff(t)) * bign)
    fk = np.arange(bign // 2 + 1) * dfreq

    # Calculate power spectrum
    pwr = xs2[: bign // 2 + 1] / bign**2
    if not nohanning:
        wss = bign * np.sum(window**2)
        pwr /= wss

    # Binning, if necessary
    if bin > 1:
        bins = np.arange(0, len(pwr), bin)
        binned_pwr = np.array([np.sum(pwr[i : i + bin]) for i in bins[:-1]])
        binned_fk = fk[bins[:-1]] + dfreq * bin / 2.0
        pwr, fk = binned_pwr, binned_fk

    # Adjust for units
    if not notperhz:
        pwr /= dfreq

    return fk, pwr
