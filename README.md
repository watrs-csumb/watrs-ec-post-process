# watrs_ec_processing
This repository includes scripts used by the Water, Agriculture, Technology and Remote Sensing (WATRS) Lab at California State University Monterey Bay (CSUMB) to quality control and post-process eddy covariance data.

# WATRS EC-OpenET Processing Pipeline
The scripts provided here are meant to be run in series to combine outputs from Campbell Scientific data loggers running EasyFlux DL software.
1.   Combine Ameriflux formated .dat files ([script](https://github.com/sciencebyAJ/watrs_ec_processing/blob/main/WATRS_COMBINE_EC_DATA.ipynb)).
2.   Evaluate, quality control, and gap-fill combined data files script.
3.   Post-process quality-controlled EC data with fluxdata qaqc script

For more information on [fluxdata-qaqc](https://flux-data-qaqc.readthedocs.io/en/latest/install.html) see the link.

# Meta Data Table of Available CSUMB Sites
The scripts are set up to draw meta data information for an eddy covariance tower.
* Edit the [csumb_field_meta Google Sheet](https://docs.google.com/spreadsheets/d/1fmik1-lOcGyLyLe6RmBseVzpIddQEU-9-KNh1p_4lpU/edit?usp=sharing) to include all necesary information.

Contributions to this repository include WATRS lab members including: AJ Purdy, Ryan Solymar, Michael Biedebach
