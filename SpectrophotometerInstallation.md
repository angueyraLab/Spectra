# Image analysis software installation

> Created by Juan Angueyra (2023_02_27)

## Some basics

Read [this blog by Robert Haase](https://focalplane.biologists.com/2022/12/08/managing-scientific-python-environments-using-conda-mamba-and-friends/)

## Instructions

1. **Install mambaforge:**
    1. Go to [this link](https://github.com/conda-forge/miniforge#mambaforge)
    2. Download the **appropriate** mambaforge installer with Mamba in the base environment
    3. Open a Terminal(Mac)/CommandPrompt(Windows) and run:

        ```bash
        #replace uname by version downloaded
        bash Mambaforge-$(uname)-$(uname -m).sh
        ```

    4. Press Enter to page through the license
    5. Accept the license
    6. Install locally (not for all users, but in your home folder only)
    7. Wait for the installer to finish (at least 30 seconds)
    8. When asked “Do you want to installer to initialize Miniconda by running conda init” then type “yes”
    9. Exit Terminal(Mac)/CommandPrompt(Windows) and reopen it
    10. Test that installation went ok by typing:

        ```bash
        mamba --version
        ```

2. **Create a new environment for image analysis: Spectra** (every big project should have its own environment!)

    1. In terminal/Command Prompt:

        ```bash
        mamba create --name Spectra python jupyterlab textual textual-dev marimo pandas matplotlib seabreeze scikit-learn -c conda-forge
        ```

    1. This creates the _Spectra_ environment with some basics.
    2. We will also use other packages. To maimtain compatiblity, we will install them using _mamba_ (avoid using _pip_ commands!! (unless absolutely necessary))
    3. Packages have to be installed **inside** the _Spectra_ environment (and not the _base_ environment)
    4. **Before** installing any packages or starting any work, make sure to activate the _Spectra_ environment
3. **Activate the _Spectra_ environment:**  
    1. This is required to install any package and before starting any analysis routine

        ```bash
        mamba activate Spectra
        ```

    1. Install all other packages needed for analysis

        ```bash
        seabreeze_os_setup
        pip install seatease
        mamba install -c conda-forge svgutils cmcrameri
        mamba install -c conda-forge h5py
        mamba install -c conda-forge textual textual-dev
        ```  

    2. Missing ones right now:

        ```bash
        mamba install -c conda-forge tqdm ipywidgets
        ```

    3. Finish installation

        ```bash
        mamba deactivate
        ```

1. Start analysis

    1. Open Terminal(Mac)/CommandPrompt(Windows) and type:

    ```bash
    mamba activate Spectra
    ```

    2. Launch the interactive Marimo Notebook by typing (a browser window should open)

    ```python
            marimo run flameSpectra.py --host=localhost --no-token --port=2718 --headless
    ```
    2. If browser didn't open, then manually open a new tab and use this URL:
    ```python
       http://localhost:2718
    ```

    15. To finish shut down the Marimo Notbeook
    16. Alternatively, go to Terminal/Command Prompt and press Ctrl+C twice (this shuts down Marimo)
    17. Finally, deactivate the environment by typing:

        ```bash
        mamba deactivate
        ```

---
---
---

!!!danger Environment broke
    If the environment broke, sometimes the only solution is to deactivate and delete the environment and reinstall all dependencies. To do this:<br>```mamba env remove --name Spectra```
---

---
---
