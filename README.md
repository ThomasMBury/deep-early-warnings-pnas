# Deep learning for early warning signals of regime shifts
This repository contains code to accompany the publication:
#### *Deep learning for early warning signals of regime shifts*. In review at *PNAS*, 18 May 2021 <https://doi.org/number_here> Thomas M. Bury [![](https://orcid.org/sites/default/files/images/orcid_16x16.png)](https://orcid.org/0000-0003-1595-9444), R. I Sujith, Induja Pavithran, Marten Scheffer, Timothy M. Lenton, Madhur Anand, and Chris T. Bauch. 


## Requirements

Python 3.7 is required. To install python package dependencies, use the command

```setup
pip install -r requirements.txt
```
preferably within a new virtual environment.

The bifurcation continuation software AUTO-07P is required. Installation instructions are provided at
http://www.macs.hw.ac.uk/~gabriel/auto07/auto.html


## Directories

**/dl_train:** Code to train the DL algorithm

**/figures_pnas:** Code to generate figures used in manuscript.

**/test_models:** Code to simulate and compute early warning signals for the test models. These include the Consumer-Resource model, May's harvesting model and an SEIRx model.

**/test_empirical:** Code to pre-process and compute early warning signals for the empirical datasets (see below).

**/training_data:** Code to generate training data for the deep learning algorithm. Execute the script *run_job.sh* to generate two models and time series for each bifurcation type [~1 minute].


## Data sources

The empirical data used in this study are available from the following sources:
1. **Sedimentary archive** data from the Mediterranean Sea are available at the [PANGAEA](https://doi.pangaea.de/10.1594/PANGAEA.923197) data repository. Data were preprocessed according to the study [Hennekam, Rick, et al. "Early‐warning signals for marine anoxic events." Geophysical Research Letters 47.20 (2020): e2020GL089183.](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2020GL089183)
2. **Thermoacoustic instability** data are available in this repository [here](test_empirical/thermoacoustic/data/thermo_experiments). Data were collected by Induja Pavithran and R. I. Sujith and were first published in [Pavithran, I. and Sujith, R.I. "Effect of rate of change of parameter on early warning signals for critical transitions" Chaos: An Interdisciplinary Journal of Nonlinear Science 31.1 (2021): 013116.](https://aip.scitation.org/doi/full/10.1063/5.0025533?casa_token=isaRQyMz9J0AAAAA%3AnT4dG70bROSFkRSDm-7U6wDx20NTnSFuyUqAsobZKEjkwrnneG8ienGwLPkKmj56ZU7f3-aRH5F-&)
3. **Paleoclimate transition** data are available from the [World Data Center for Paleoclimatology](http://www.ncdc.noaa.gov/paleo/data.html), National Geophysical Data Center, Boulder, Colorado. Data were preprocessed according to the study [Dakos, Vasilis, et al. "Slowing down as an early warning signal for abrupt climate change." Proceedings of the National Academy of Sciences 105.38 (2008): 14308-14312.](https://www.pnas.org/content/105/38/14308.short)


## License
Shield: [![CC BY-NC-SA 4.0][cc-by-nc-sa-shield]][cc-by-nc-sa]

This work is licensed under a
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa].

[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg

Copyright © 2021, Thomas Bury (McGill University), Chris Bauch (University of Waterloo), Madhur Anand (University of Guelph)
