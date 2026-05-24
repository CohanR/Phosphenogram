# Phosphenogram


## Phosphene documentation and quantification tool

This repository contains placeholder materials for a computer-based phosphene documentation and quantification procedure used to record participant-reported transcranial magnetic stimulation (TMS)-induced phosphenes.

The tool was developed to support standardised documentation of perceived phosphene location, shape, and size. Participants report the perceived phosphene using a drawing interface, and the resulting output can be used to quantify phosphene size and spatial location in visual-field coordinates.

### Experimental context

In the associated study, participants were seated in a dimly lit room at a fixed viewing distance of 57 cm from a 27-inch monitor. The drawing window was 800 × 600 pixels and used a dim grey and black colour scheme. The physical drawing-window dimensions were 530 mm × 400 mm, and the monitor refresh rate was 60 Hz.

Before stimulation, participants were introduced to the drawing window and instructed that they would use a computer mouse to report the perceived location, shape, and size of any TMS-induced phosphenes. The drawing interface used a low-luminance dark grey background. Testing was performed in a dimly lit room using an indirect warm light source directed toward the floor.

### Eye-state procedure

Because previous work has shown that eye state and fixation can influence phosphene threshold, size, and spatial location, both eyes-open and eyes-closed testing may be relevant depending on the experimental goal.

In the associated study, participants kept their eyes closed during phosphene thresholding. After thresholding, they opened their eyes and used the drawing interface to report the perceived phosphene. Eyes-closed testing was used to support threshold detection, whereas eyes-open testing may be preferable in protocols where fixation control and retinotopic localisation are the main goals.

### Output

The intended tool records a participant drawing and generates:

- a screenshot of the reported phosphene;
- a comma-separated values file;
- x and y coordinates of the drawn polygon;
- size metrics in pixels, physical units, and visual-angle units;
- area estimates in px², mm², and deg².

### Area calculation

Drawn phosphenes typically do not follow regular geometric shapes. Polygon area can therefore be estimated using the shoelace formula, also known as Gauss's area formula.

Pixel area is converted to physical area using the screen dimensions and pixel density. Physical area can then be converted into visual-angle units using the viewing distance.

### Repository status

This repository currently contains placeholder code and documentation. Full scripts, example data, and additional documentation will be added in later updates.

### Citation and use

If using or adapting this tool, please cite the associated manuscript once available and acknowledge this repository.

Repository: https://github.com/CohanR/Phosphenogram

### Versions
Initial release: July 2022
Updates: Feb 2023; September 2025; May 2026
Current version: May 2026
Remy Cohan (rcohan@yorku.ca)
