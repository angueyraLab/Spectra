import numpy as np
import os.path

#peak of spectral sensitivities of zebrafish opsins
zfLmax = {
    'R' : 500,
    'U' : 355,
    'S' : 416,
    'M1' : 467,
    'M2' : 476,
    'M3' : 488,
    'M4' : 505,
    'L1' : 558, 
    'L2' : 548,
}

# Tsujimura (2015): 
# In the case of zebrafish, all the four subtypes of RH2 are expressed in the short (or accessory) member of double cones (SDCs) and both two LWS subtypes are expressed in the long (or principal) member of double cones (LDCs)
# However, they are differentiated in the expression pattern in the retina [13]. 
# Fish eyes continue to grow through the lifetime by adding new cells to the peripheral zones [17]. 
# Concomitantly, early-expressed subtypes are located centrally in the adult retina. 
# The shortest wavelength RH2 subtype (RH2-1) is expressed earliest and in the central to the dorsal area of the adult retina. 
# The second shortest wave subtype (RH2-2) is expressed subsequently overlapping with RH2-1 but extending outside of it. 
# The longer wave RH2 subtype (RH2-3) is expressed later and in a region surrounding the RH2–2 area, and 
# the longest wave RH2 subtype (RH2-4) is also expressed later and outside of the RH2-3 area, broadly occupying the ventral area. 
# Similarly, the shorter wave LWS subtype (LWS-2) is expressed earlier and in the central-to-dorsal area in the adult retina, 
# and the longer wave LWS subtype (LWS-1) is expressed later in the development and confined peripherally with largely occupying the ventro-nasal area of the adult retina [13]

#peak of spectral sensitivities of A. burtoni opsins
abLmax = {
    'R' : 500,
    'U' : 360,  # sws1
    'S1' : 425, # sws2b
    'S2' : 456, # sws2a
    'M1' : 472, # mws2
    'M2' : 518, # mws1a
    'M3' : 528, # mws1b
    'L' : 561,  # lws
}




def govardovskiiTemplateA1(lmax = 500, wavelengths = np.linspace(300,800,num=800-300-1), A1_chrom = 100):
    """
    govardovskiiTemplateA1(lmax = 500, lambda = np.linspace(300,800,num=800-300-1), A1_chrom = 1)
    
    Calculate visual pigments absorption using templates from Govardovskii et al., 2000 

    Args:
        lmax (int, optional): peak wavelength of spectral sensitivity. Defaults to 500.
        wavelengths (numpy.array, optional): wavelength axis. Defaults to np.linspace(300,800,num=800-300-1).
        A1_chrom (int, optional): percent of A1 chromophore. Defaults to 1.

    Returns:
        normSensitivity: normalized spectral sensitivity (numpy.array)
    """
    #fit A1 peak
    a1 = 0.8795+0.0459*np.exp(-np.power((lmax-300),2)/11940)
    lmb1 = 189+0.315*lmax
    p1=-40.5+0.195*lmax  #Govardovskii calls this b but this confuses it with the alpha peak equation
    x = lmax/wavelengths
    Salpha_A1 = 1/((np.exp(69.7*(a1-x))+np.exp(28*(0.922-x))+np.exp(-14.9*(1.104-x))+0.674))
    Sbeta_A1 = 0.26*np.exp(-np.power(((wavelengths-lmb1)/p1),2))
    Speak_A1 = Salpha_A1+Sbeta_A1
    # fit A2 peak
    a2 = 0.875+0.0268*(np.exp((lmax-665)/40.7))  
    A2 = 62.7 + 1.834*np.exp((lmax-625)/54.2)
    lmb2 = 216.7+0.287*lmax
    p2 = 317-1.149*lmax+0.00124*lmax*lmax  #Govardovskii calls this b but this confuses it with the alpha peak equation
    Salpha_A2 = 1/((np.exp(A2*(a2-x))+np.exp(20.85*(0.9101-x))+np.exp(-10.37*(1.1123-x))+0.5343))
    Sbeta_A2 = 0.26*np.exp(-np.power(((wavelengths-lmb1)/p1),2))
    Speak_A2 = Salpha_A2+Sbeta_A2
    # weight by chromophore, sum and normalize
    Speaktot = A1_chrom*Speak_A1+(100-A1_chrom)*Speak_A2
    normSensitivity = Speaktot/np.max(Speaktot)
    return normSensitivity

# ----------
