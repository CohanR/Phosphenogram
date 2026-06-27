# Phosphenogram

## Phosphene documentation and quantification tool

<p align="center">
  <a href="https://neuropsis.org/phosphenogram_web_v2.html">
    <img width="340" src="https://img.shields.io/badge/Launch%20Phosphenogram-222222?style=for-the-badge&labelColor=222222&color=222222" alt="Launch Web-based Phosphenogram">
</p>

**Phosphenogram** is a computer-based phosphene documentation and quantification tool developed to record TMS-evoked phosphenes. It supports standardised documentation of perceived phosphene **location**, **shape**, and **size**. Participants report the perceived phosphene using a drawing interface, and the resulting output can be used to quantify phosphene size and spatial location in screen, physical, and visual-field coordinates. The main application is Python-based and can be run as a script in your Mac terminal or you can use the above button and launch the web-based version. 

*The scripts have been tested and validated on Intel-based and silicon based Mac OS 13 or higher.

---

## Experimental context

In the associated study, participants were seated in a dimly lit room at a fixed viewing distance of **57 cm** from a **27-inch monitor**. The drawing window was **800 × 600 pixels** and used a dim grey and black colour scheme. The physical drawing-window dimensions were **530 mm × 400 mm**, and the monitor refresh rate was **60 Hz**.

Before stimulation, participants were introduced to the drawing window and instructed that they would use a computer mouse to report the perceived location, shape, and size of any TMS-induced phosphene. The drawing interface used a low-luminance dark grey background. Testing was performed in a dimly lit room using an indirect warm light source directed toward the floor.

---

## Eye-state procedure

Because eye state and fixation can influence phosphene threshold, size, and spatial location, both **eyes-open** and **eyes-closed** testing may be relevant depending on the experimental goal.

In the associated study, participants kept their eyes closed during phosphene thresholding. After thresholding, they opened their eyes and used the drawing interface to report the perceived phosphene. Eyes-closed testing was used to support threshold detection, whereas eyes-open testing may be preferable in protocols where fixation control and retinotopic localisation are the main goals.

---

## Running the Python script locally

For the desktop Python version, download the `Phosphenogram.py` file from this repository, install the required dependencies, and run it on your machine. For the features see the browser version. 

```bash
pip install pygame pandas matplotlib

python3 Phosphenogram.py

Other non-pip installations:

sudo apt install python3-tk
```

## Browser version

The browser version (simillar to the desktop version) allows users to configure:

* drawing window width and height
* physical monitor dimensions
* viewing distance
* brush size
* background colour
* uploaded still image or GIF background (usefull if you are assessing patients with neuro-ophtalmological disorders e.g., Visual Snow syndrome or Charles Bonnet) 
* quadrant line visibility
* quadrant line colour, width, and opacity
* participant, session, and condition labels

The current browser version also includes fullscreen drawing mode so the participant or resaercher can first enter the display parameters and then draw in a less distracting fullscreen interface.



## Output

The tool records the participant drawing and generates:

* a PNG image of the reported phosphene;
* a comma separated values file;
* x and y coordinates of the drawn polygon;
* stroke start and end coordinates;
* bounding box dimensions;
* size metrics in pixels, physical units, and visual angle units;
* area estimates in px², mm², and deg²;
* perimeter estimates in px, mm, and degrees.

Files are saved locally through the browser. GitHub Pages is static hosting, so the web tool does not automatically upload participant files to a server.

---

## Example screenshots and data output

Add screenshots to a folder such as:

```text
docs/screenshots/
```

files:

```text
docs/screenshots/phosphenogram_interface.png
docs/screenshots/fullscreen_drawing_mode.png
docs/screenshots/example_phosphene_output.png
docs/screenshots/example_csv_output.png
```


### Interface

<p align="center">
  <img src="docs/screenshots/phosphenogram_interface.png" width="750" alt="Phosphenogram browser interface">
</p>

### Fullscreen drawing mode

<p align="center">
  <img src="docs/screenshots/fullscreen_drawing_mode.png" width="750" alt="Phosphenogram fullscreen drawing mode">
</p>

### Example phosphene drawing output

<p align="center">
  <img src="docs/screenshots/example_phosphene_output.png" width="750" alt="Example phosphene drawing output">
</p>

### Example CSV/data output

<p align="center">
  <img src="docs/screenshots/example_csv_output.png" width="750" alt="Example Phosphenogram CSV output">
</p>

---

## Area calculation

Drawn phosphenes typically do not follow regular geometric shapes. Polygon area is therefore estimated using the **shoelace formula**, also known as **Gauss's area formula**.

Pixel area is converted to physical area using the drawing-window dimensions and pixel density. Physical area can then be converted into visual-angle units using the viewing distance.

---

## Intended use

Phosphenogram was developed for perceptual neuroscience and visual cortex stimulation studies where participant-reported phosphenes need to be recorded in a standardised way.

Potential use cases include:

* TMS-evoked phosphene mapping;
* phosphene threshold experiments;
* invasive and non-invasive visual cortex stimulation protocols;
* assessing patients with neuro-ophtalmological disorders e.g., Visual Snow Syndrome or Charles Bonnet
* eyes-open versus eyes-closed phosphene documentation;
* retinotopic localisation workflows;
* reproducible reporting of subjective visual percepts.

---

## Repository status

This repository contains materials for the Phosphenogram phosphene documentation and quantification tool. The browser-based version is designed for static web deployment and local PNG/CSV export.

Additional scripts, example data, screenshots, and documentation will be added in later updates.

---

## Citation and use

If using or adapting this tool, please cite and acknowledge (the main manuscript including the effects of eye state on PTs and phosphene size has been submitted and will be added when published):

```text
Cohan, R., Moro, S. S., & Steeves, J. K. E. (2025). Quantifying phosphene size using MRI-guided transcranial magnetic stimulation to primary visual cortex. Journal of Vision, 25(9), 2652. https://doi.org/10.1167/jov.25.9.2652
```

Repository:

```text
https://github.com/CohanR/Phosphenogram
```

Other tools:

  </a>
  <br><br>
  <a href="https://neuropsis.org/">
    <img width="340" src="https://img.shields.io/badge/Open%20NIfTI%20Viewer-6f42c1?style=for-the-badge&labelColor=6f42c1&color=6f42c1" alt="Open NIfTI Viewer">
  </a>


## Versions

**Initial release:** July 2022
**Updates:** February 2023; September 2025; May 2026
**Current version:** May 2026

---

## Author

**Remy Cohan**
Perceptual Neuroscience Laboratory
Centre for Integrative and Applied Neuroscience
Centre for Vision Research
York University, Toronto, Canada

Contact: [rcohan@yorku.ca](mailto:rcohan@yorku.ca)
