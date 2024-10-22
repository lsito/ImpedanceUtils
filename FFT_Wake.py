# %% Importing modules
import os, sys
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from functools import partial
from scipy.constants import c
import scipy.special as sc

# %% FFT of Wakefunction from CST folder

def FFT_Wake(FolderName, Wz=None, sigmaz=20e-3, N=10001, sub_sampling=20, component="z"):
    
    """
    Computes the impedance using the FFT of a CST-calculated wake function.

    Parameters:
    -----------
    FolderName : str
        Path to the folder containing the CST export data.
    
    Wz : pd.DataFrame
        DataFrame containing the wake function data with:
        - Column 's': distance values.
        - Column 'Real': corresponding wake function values.
    
    sigmaz : float
        Bunch length used in the CST simulation.
    
    N : int, optional (default=10001)
        Number of points for the FFT computation.
    
    sub_sampling : int, optional (default=20)
        Subsampling factor for the wake function data; selects every nth point (default is every 20th point).
    
    component : str, optional (default='z')
        Specifies the component of the wake function to extract from the CST export data.

    Returns:
    --------
    f : np.ndarray
        Array of frequency samples for the impedance in Hz.
    
    Z : np.ndarray of complex
        Array of complex impedance values in Ohms.
    """
    
    import math
    import scipy.special as sc

    from scipy.fft import fft, fftfreq
    from scipy.fft import rfft, rfftfreq

    # Elena's code
    q = 1e-9 # Charge of the bunch
    sigmaz = 20*1e-3 # Sigma of the charge distribution
    c = 299792458

    # read charge distribution in space
    # CST charge distribution in space
    charge = pd.read_csv(FolderName+r"/Export/Particle Beams_ParticleBeam1_Charge distribution (distance).txt", sep='\t', header=None, names=['s', 'Real'])

    lambdaz = charge['Real']
    z = charge['s']*1e-3 # Convert to m

    # read wake potential WPz(s)
    if Wz == None:
        if component=="z":
            Wz = pd.read_csv(FolderName+r"/Export/Particle Beams_ParticleBeam1_Wake potential_Z.txt", sep='\t', header=None, names=['s', 'Real'])
        if component=="y":
            Wz = pd.read_csv(FolderName+r"/Export/Particle Beams_ParticleBeam1_Wake potential_Y.txt", sep='\t', header=None, names=['s', 'Real'])
        if component=="y":
            Wz = pd.read_csv(FolderName+r"/Export/Particle Beams_ParticleBeam1_Wake potential_X.txt", sep='\t', header=None, names=['s', 'Real'])
    
    # Original
    # WP = Wz['Real']
    # s = Wz['s']*1e-3

    # Undersampling the wake signal for faster computation
    # !n.b. there should be a better computation based on the max frequency we want to arrive to
    WP = np.array(Wz['Real'][::sub_sampling])
    s = np.array(Wz['s'][::sub_sampling])*1e-3

    # Set up the DFT computation
    ds = s[1]-s[0]
    fmax=1*c/sigmaz/3
    
    N=int((c/ds)//fmax*N) #to obtain a 1000 sample single-sided DFT

    # interpolate charge dist to s
    lambdas = np.interp(s, z, lambdaz/q)

    # Obtain DFTs
    lambdafft = np.fft.fft(lambdas*c, n=N)

    WPfft = np.fft.fft(WP*1e12, n=N)
    ffft=np.fft.fftfreq(len(WPfft), ds/c)

    # Mask invalid frequencies
    mask  = np.logical_and(ffft >= 0 , ffft < fmax)
    WPf = WPfft[mask]*ds
    lambdaf = lambdafft[mask]*ds
    f = ffft[mask]            # Positive frequencies

    # Compute the impedance
    if component=="z":
        Z = -WPf / lambdaf
    if component=="y":
        Z = -1j*WPf / lambdaf
    
    return f, Z