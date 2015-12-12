## UC Berkeley's Statistics 159/259
### Project Group Gamma, Fall Term 2015 

_**Group members:**_ Nima Hejazi, Feng Lin, Luyun Zhao, & Xinyue Zhou

_**Topic:**_ [Working Memory in Healthy and Schizophrenic Individuals] (https://openfmri.org/dataset/ds000115)

[![Build Status](https://travis-ci.org/berkeley-stat159/project-gamma.svg?branch=master)](https://travis-ci.org/berkeley-stat159/project-gamma?branch=master)
[![Coverage Status](https://coveralls.io/repos/berkeley-stat159/project-gamma/badge.svg?branch=master)](https://coveralls.io/r/berkeley-stat159/project-gamma?branch=master)

### Codebase 

Utils methods are in the subdirectory code/utils. Analysis scripts are in code/ directory. 

### Tests and Coverage

'make test' runs all the tests for the repository. Methods were extracted into individual modules inside the utils/ subdirectory under code/. Plotting helper functions remained inside the analysis scripts and are not tested.

'make coverage' runs the coverage tests and generates the coverage report.

### Data

'make data' downloads all the data except the condition files. Running this takes around 2 hours. 

Directory data/ is initially empty, except for 'net_roi.txt', which is from the supplemental material of the reference paper and may be found [at the link] (http://www.ncbi.nlm.nih.gov/pmc/articles/PMC3081915/bin/NIHMS253634-supplement-01.pdf). We manually extracted the information from Table S1 and make it available here as 'net_roi.txt'.

'make conditionfiles' downloads all of the necessary condition files for the analysis.

The reason that downloading the condition files has been made into a separate command is due to the fact that the condition files are bundled together with the fMRI raw data on the [OpenFMRI site] (https://www.openfmri.org/dataset/ds000115/). Due to this, it would take several hours to download these files. Since we only need the condition files and not the rest of the data in the bundle, we have created the separate command to hasten the download process. Also, to improve accessibility, we made the decision to include the condition files (in TXT format) in the data/ directory in the repository. For reproducibility, you can run this command to obtain the same condition files used in the analysis reported.

### Analysis

'make analysis' runs all the analysis scripts and fills up the results/ directory with diagrams and graphs, which are referenced in the full report.

### Paper

'make paper' produces the full report describing this research project.

