import marimo

__generated_with = "0.9.14"
app = marimo.App(width="medium")


@app.cell
def __(mo):
    mo.md(r"""# Record Spectrum using flameSpectra 🔥🌈""")
    return


@app.cell
def __():
    print("Loading extensions...")

    import seabreeze
    # seabreeze.use('cseabreeze')
    from seabreeze.spectrometers import list_devices, Spectrometer
    # Get any spectrometer
    import seatease.spectrometers

    import marimo as mo
    import numpy as np
    import pandas as pd
    import h5py
    import datetime
    import matplotlib.pyplot as plt
    import matplotlib.font_manager as font_manager
    import plotParams
    from dataclasses import dataclass

    print("Successfully loaded extensions!")
    return (
        Spectrometer,
        dataclass,
        datetime,
        font_manager,
        h5py,
        list_devices,
        mo,
        np,
        pd,
        plotParams,
        plt,
        seabreeze,
        seatease,
    )


@app.cell
def __(mo, plotParams, seabreeze):
    ppl = {str(d) : d for d in plotParams.vsdlPpl} # transform list into dictionary for dropdown menu
    experimenter = mo.ui.dropdown(options=ppl, value=next(iter(ppl)),label=r'Experimenter:')

    lightSource = mo.ui.text(value="nameHere", label=r'Light Source: ')

    # deviceList = seatease.spectrometers.list_devices() # get list of devices
    deviceList = seabreeze.spectrometers.list_devices() # get list of devices
    deviceOptions = {str(d) : d for d in deviceList} # transform list into dictionary for dropdown menu
    availableDevices = mo.ui.dropdown(options=deviceOptions, value=next(iter(deviceOptions)),label=r'Available devices:')

    mo.vstack([experimenter,lightSource, availableDevices])
    return (
        availableDevices,
        deviceList,
        deviceOptions,
        experimenter,
        lightSource,
        ppl,
    )


@app.cell
def __(mo):
    # trio of buttons: Connect Stop Reload
    specConnect = mo.ui.run_button(kind = 'success', disabled = False, tooltip = 'Establish connection with Spectrometer', label = 'Connect')

    specDisconnect = mo.ui.run_button(kind = 'danger', disabled = False, tooltip = 'Interrupt connection with Spectrometer', label = 'Disconnect')

    mo.hstack([specConnect, specDisconnect], justify='start')
    return specConnect, specDisconnect


@app.cell
def __(mo, specConnect):
    mo.stop(not specConnect.value)


    nAverageOptions = {str(d) : d for d in [1,2,4,8,16,32]} # transform list into dictionary for dropdown menu
    nAverage = mo.ui.dropdown(options=nAverageOptions, value=next(iter(nAverageOptions)), label=r'Averaging:')

    wLims = mo.ui.range_slider(start=200, stop=1100, step=1, value=[300, 1000], label=r'Wavelength range (nm):', show_value=True)

    plotStyle = mo.ui.dropdown(options=['Dark','Light'], value='Dark', label=r'Plot Style:')


    mo.hstack([nAverage, wLims, plotStyle], justify='start')
    return nAverage, nAverageOptions, plotStyle, wLims


@app.cell
def __(availableDevices, mo, seabreeze, specConnect):
    mo.stop(not specConnect.value)

    specConnect.value

    # spec = seatease.spectrometers.Spectrometer(availableDevices.value)
    spec = seabreeze.spectrometers.Spectrometer(availableDevices.value)

    mo.md(
        f"""
        Saturation value = {spec.max_intensity:,.0f} a.u.  
        Integration limits: &emsp; min = {spec.integration_time_micros_limits[0]/1000:,.0f} ms &emsp; max = {spec.integration_time_micros_limits[1]/1000:,.0f} ms
        """
        )
    return (spec,)


@app.cell
def __(mo):
    # tau = mo.ui.slider(start=3, stop=20000, value=100, label=r'Integration time (ms): $\tau$') # real limits
    getTau, setTau = mo.state(10)
    tau = mo.ui.slider(start=3, stop=20000, value=getTau(), label=r'Integration time (ms): $\tau$', show_value=True, on_change=setTau)
    recordSpectrum = tau.form(submit_button_label = 'Record Spectrum')
    return getTau, recordSpectrum, setTau, tau


@app.cell
def __(getTau, mo, recordSpectrum, setTau):
    tauDark = mo.ui.slider(start=3, stop=20000, value=getTau(), label=r'Integration time (ms): $\tau$', show_value=True, on_change=setTau)
    #lambda v: set_Tau_state(v))
    recordDarkSpectrum = tauDark.form(submit_button_label = 'Record Dark Spectrum')
    mo.hstack([recordSpectrum,recordDarkSpectrum], justify='start')
    return recordDarkSpectrum, tauDark


@app.cell
def __(
    mo,
    nAverage,
    np,
    plotParams,
    plt,
    recordSpectrum,
    spec,
    specDisconnect,
    wLims,
):
    mo.stop(recordSpectrum.value is None, mo.md("Set Integration time and Record Light Spectrum"))

    mo.stop(specDisconnect.value is True, mo.md("Connection closed; re-open connection with Spectrometer"))

    specDisconnect.value 

    # set integration time
    spec.integration_time_micros(recordSpectrum.value * 1000)  #in ms
    # get wavelengths
    wavelength = spec.wavelengths()

    # get intensities
    spectrum = np.empty([nAverage.value,len(wavelength)])
    for _i in np.arange(nAverage.value):
        spectrum[_i,:] = spec.intensities(correct_dark_counts=True, correct_nonlinearity=True)

    meanSpectrum = np.mean(spectrum, axis=0)


    fH1, axH1 = plt.subplots(figsize=(6,4))
    pH1 = plt.plot(wavelength, meanSpectrum, color = '#1ACDD1')
    plt.subplots_adjust(left=0.15, right=.95, top=0.90, bottom=0.1)
    plt.tight_layout()
    axH1.set_xlim(wLims.value)
    axH1.set_xlabel('Wavelength (nm)')
    axH1.set_ylabel('Power (a.u.)')
    axH1.set_title('Spectrum (n={0})'.format(nAverage.value))
    plotParams.formatFigureMain(fH1, axH1, pH1)
    # mo.mpl.interactive(fH1)


    mo.md(
      f"""
      Spectrum recorded! Turn light source off and now record Dark Spectrum...
      {mo.as_html(fH1)}
      """
    )
    return axH1, fH1, meanSpectrum, pH1, spectrum, wavelength


@app.cell
def __(
    mo,
    nAverage,
    np,
    plotParams,
    plt,
    recordDarkSpectrum,
    recordSpectrum,
    spec,
    specDisconnect,
    wLims,
    wavelength,
):
    mo.stop(recordSpectrum.value is None, mo.md("Waiting for Light Spectrum..."))

    mo.stop(recordDarkSpectrum.value is None, mo.md("Waiting for Dark Sepctrum"))

    mo.stop(specDisconnect.value is True, mo.md("Connection closed; re-open connection with Spectrometer"))

    specDisconnect.value 

    # get intensities
    spectrum_dark = np.empty([nAverage.value,len(wavelength)])
    for _i in np.arange(nAverage.value):
        spectrum_dark[_i,:] = spec.intensities(correct_dark_counts=True, correct_nonlinearity=True)

    darkSpectrum = np.mean(spectrum_dark, axis=0)

    fH2, axH2 = plt.subplots(figsize=(6,4))
    pH2 = plt.plot(wavelength, darkSpectrum, color = '#C2C2C2')
    plt.subplots_adjust(left=0.15, right=.95, top=0.90, bottom=0.1)
    plt.tight_layout()
    axH2.set_xlim(wLims.value)
    axH2.set_xlabel('Wavelength (nm)')
    axH2.set_ylabel('Power (a.u.)')
    axH2.set_title('Dark Spectrum (n={0})'.format(nAverage.value))
    plotParams.formatFigureMain(fH2, axH2, pH2)
    # mo.mpl.interactive(fH1)


    mo.md(
      f"""
      dark Spectrum recorded! Calculating results...
      {mo.as_html(fH2)}

      """
    )
    return axH2, darkSpectrum, fH2, pH2, spectrum_dark


@app.cell
def __(
    darkSpectrum,
    meanSpectrum,
    mo,
    nAverage,
    plotParams,
    plt,
    wLims,
    wavelength,
):
    fH, axH = plt.subplots(figsize=(6,4))
    pH = plt.plot(wavelength, meanSpectrum-darkSpectrum, color = '#1ACDD1')
    plt.subplots_adjust(left=0.15, right=.95, top=0.90, bottom=0.1)
    plt.tight_layout()
    axH.set_xlim(wLims.value)
    axH.set_xlabel('Wavelength (nm)')
    axH.set_ylabel('Power (a.u.)')
    axH.set_title('Difference Spectrum (n={0})'.format(nAverage.value))
    plotParams.formatFigureMain(fH, axH, pH)
    # mo.mpl.interactive(fH)

    mo.md(
      f"""
      {mo.as_html(fH)}
      """
    )
    return axH, fH, pH


@app.cell
def __(mo, recordDarkSpectrum, recordSpectrum):
    mo.stop(recordSpectrum.value is None)
    mo.stop(recordDarkSpectrum.value is None)

    saveSpectra = mo.ui.run_button(kind = 'warn', disabled = False, tooltip = 'SaveSpectra using Path and Filename', label = 'Save Spectra')
    fName = mo.ui.text(value="filename", label=r'fileName: ')
    dPath = mo.ui.file_browser(initial_path="/Users/juanangueyra/Library/CloudStorage/GoogleDrive-angueyra@umd.edu/Shared drives/vldImaging/LightCalibration/", selection_mode = 'directory', multiple=False, label=r'Choose folder to save file...')
    dPath
    mo.vstack([saveSpectra, fName, dPath])
    return dPath, fName, saveSpectra


@app.cell
def __(
    availableDevices,
    dPath,
    darkSpectrum,
    datetime,
    experimenter,
    fName,
    h5py,
    lightSource,
    meanSpectrum,
    mo,
    np,
    saveSpectra,
    wavelength,
):
    mo.stop(not saveSpectra.value)

    _filePath = dPath.path() + '/' + fName.value + '.csv'
    _metadataPath = dPath.path() + '/' + fName.value + '.h5'

    #Writing data
    _metaFile = h5py.File(_metadataPath, "w")
    _metaGroup = _metaFile.create_group("Spectra")
    _metaWavelength = _metaFile.create_dataset("Spectra/wavelength", data=np.astype(wavelength,np.float64))
    _metaWavelength = _metaFile.create_dataset("Spectra/dark", data=np.astype(darkSpectrum,np.float64))
    _metaWavelength = _metaFile.create_dataset("Spectra/spectrum", data=np.astype(meanSpectrum,np.float64))
    #set metadata directly
    _metaFile.attrs['date'] = str(datetime.datetime.now())
    _metaFile.attrs['experimenter'] = str(experimenter.value)
    _metaFile.attrs['spectrometer'] = str(availableDevices.value)
    _metaFile.attrs['lightsource'] = str(lightSource.value)

    _metaFile.close()

    # #Reading data
    # hf1 = h5py.File("test_data.h5", "r")
    # for name in hf1:
    #     print(name)

    # print(hf1.attrs.keys())
    # hf1.close()

    np.savetxt(_filePath, np.c_[wavelength, darkSpectrum, meanSpectrum], delimiter=',', header='wavelength,dark,spectrum', comments='')

    mo.md(
      f"""
      Saved '{_filePath}'  
      Saved '{_metadataPath}'
      """
    )
    return


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
