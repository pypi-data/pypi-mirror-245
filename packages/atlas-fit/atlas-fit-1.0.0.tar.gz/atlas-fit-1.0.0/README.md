# Atlas-Fit

Python tools to fit solar spectra with known atlantes for 
 - **wavelength calibration**
 - **continuum correction**
 - stray-light analysis
 - effective FWHM computation
 - chi^2 error computation of the atlas fit

This package provides two tools:

- `bin/prepare`:  
    This script is used to generate a list of lines from the atlas and data
    to use for finding a wavelength solution (dispersion). 
    If you have a list of lines already you can still use this to test and 
    fine-tune your configuration and to inspect the fitting and analysis 
    results with interactive plots.
- `bin/amend_spectroflat`:  
    This tool allows to amend the calibration results from the
    `spectroflat` library. The fitted dispersion can be applied 
    to the `OffsetMap` (to include wavelength calibration) and 
    the continuum correction can be included with the soft-flat.

Both tools can (and should) be run with the same configuration. 
Run the `prepare` first to find the right configuration values 
and use the `amend_spectroflat` script to apply the results.

#### Configuration
Lines to be used for dispersion fitting can be selected interactively:
![Interactive Line Selection](examples/line_selection.png)
After the `prepare` script ran successful on the selected lines, it will 
create an `atlas_fit_lines.yaml` configuration file to be used with 
`amend_spectroflat` script. Find an example under `examples/line_selection.yml`

```yaml 
label: "Test config"
input:
  path: examples/test.fits.gz
  roi: "[25,10:]"
  wl_start: 410.6
  wl_end: 413.4
  fwhm: 0.00112
  stray_light: 7
  line_window: 12

atlas:
  key: 'hhdc'
  line_window: 50
```

Find a fully commented example under `examples/config.yml`

#### Usage 
Run either script with `<script-name> path/to/config.yml [path/to/linefile.yml]`

##### `prepare`
This script allows you to inspect the fit of your data 
against the selected atlas and lines in detail. 
Use this to fine-tune the configuration and generate plots. 

##### `amend_spectroflat`
This script creates an improved version of the calibration 
data created with `spectroflat`. It will add the dispersion
correction (and error information) to the `OffsetMap` and 
the continuum correction to the soft flat. 

Using the amended calibration data results in a fully corrected 
dataset suitable for demodulation and spectral restoration.  

#### Support
Developed and maintained by `hoelken@mps.mpg.de`