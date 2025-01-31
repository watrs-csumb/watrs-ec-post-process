# watrs_ec_processing

# CSUMB EC-OpenET Processing Pipeline
This pipeline is an end-to-end script that combines pre and post-processing steps to evaluate OpenET data for a given list of Eddy Covariance Sites.
1.   Combine EC .dat files ([script](https://github.com/sciencebyAJ/watrs_ec_processing/blob/main/WATRS_COMBINE_EC_DATA.ipynb))
2.   Apply PI Quality Flags script
3.   Post-process EC data with fluxdata qaqc script

For more information on [fluxdata-qaqc](https://flux-data-qaqc.readthedocs.io/en/latest/install.html) see the link.

# Meta Data Table of Available CSUMB Sites
* Edit the [csumb_field_meta Google Sheet](https://docs.google.com/spreadsheets/d/1cUHT0Rb0n39I0qk-bYY194spSWr7MNqkFX15PWnxXlI/edit?usp=sharing) to include all necesary information.
