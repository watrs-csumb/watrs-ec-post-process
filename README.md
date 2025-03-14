# watrs_ec_processing
This repository includes scripts used by the Water, Agriculture, Technology and Remote Sensing (WATRS) Lab at California State University Monterey Bay (CSUMB) to quality control and post-process eddy covariance data. The WATRS Lab primarily deploys eddy covariance towers in commericial and research agricultural fields. Setting up and maintaining towers in these settings presents data collection continuity and quality challenges. We share examples of how our team documents field maintenance visits and strategy regarding real-time diagnostic analysis. Our goal is to iteratively improve station configuration and set up each field season.

## Maintenance and Real Time Data Review Strategy
We plan weekly maintenance visits to each eddy covariance tower. Our team uses the following [checklist](link to template) during visits and documents maintenance using this [maintenance log](https://github.com/sciencebyAJ/watrs_ec_processing/blob/main/WATRS_ECMaintenanceChecklist.pdf). In addition to weekly visits we use Campbell's Real Time Monitoring and Control (RTMC) software to monitor live recordings. We evaluate key meteorological variables (Rn, G, Tair, RH, etc), soil wetness (VWC), irgason signal strength, and record battery voltage [link to RTMC training doc](https://docs.google.com/document/d/1fzJ8uuLHWqN2UCtyTnv2iDTehMgVidCRe7j_HXM3OSU/edit?usp=sharing). Together, these diagnostics guide our team's decision on when to visit towers outside of regularly scheduled maintenance to ensure continuous, quality data collection. 

## Eddy Covariance Post Processing
The scripts provided here are meant to be run in series to combine outputs from Campbell Scientific data loggers running EasyFlux DL software.
1.   Combine Ameriflux formated .dat files ([script](https://github.com/sciencebyAJ/watrs_ec_processing/blob/main/WATRS_COMBINE_EC_DATA.ipynb)).
2.   Evaluate, quality control, and gap-fill combined data files ([script](https://github.com/sciencebyAJ/watrs_ec_processing/blob/main/WATRS_QC_EC_DATA.ipynb)).
3.   Post-process quality-controlled EC data with fluxdata qaqc script. For more information on [fluxdata-qaqc](https://flux-data-qaqc.readthedocs.io/en/latest/install.html) see the link.
4.   Generate footprints for each field-season using [Kljun Flux Footprint Prediction](https://footprint.kljun.net/) model 

Additionally, our team uses the above scripts to generate figures for weekly tower reports
1.  Plotting half-hourly and daily SEB values [script](link to script)

## Meta Data Table of Available CSUMB Sites
The scripts are set up to draw meta data information for an eddy covariance tower.
* Edit the [csumb_field_meta Google Sheet](https://docs.google.com/spreadsheets/d/1fmik1-lOcGyLyLe6RmBseVzpIddQEU-9-KNh1p_4lpU/edit?usp=sharing) to include all necesary information.

## PI Flagging table with notes
The scripts require a PI flagging table.
* An example can be found [here](https://docs.google.com/spreadsheets/d/18cgmlfcnE9vQzkihyo3zWgqpbzG-EEce7tROzAs_OkI/edit?usp=sharing)


## Contributing team
Contributions to this repository include WATRS lab members including: AJ Purdy, Ryan Solymar, Michael Biedebach

### Acknowledgements
These scripts relied on Open Source methods from [fluxdata-qaqc](https://flux-data-qaqc.readthedocs.io/en/latest/install.html) and [oneflux](https://github.com/FLUXNET/ONEFlux) groups that were adopted to support near-real-time quality evaluation.
