# Quantum Catch Steps (from Carleton lab)

> Use same fiber optic and/or cosine corrector for calibration as for light source(s) to be calibrated

> What about integration time? How is that normalized?

1. Get spectrum of calibration lamp
2. Baseline subtraction
   - Use data from 175 - 300 nm
   - Test if needed after dark subtraction
3. Bin data to 1 nm steps between 300 and 700 nm
   - Visible range
4. Divide calibrated output given by OceanOptics by binned data
   - The units of this curve should be photons / cm2/msec/nm
   - That way output of division = Calibration Curve [photons / cm2/msec/nm / counts]
5. Multiply spectrum of light source by Calibration Curve
   - Obtain calibrated spectrum ~ [photons / cm2/msec/nm]