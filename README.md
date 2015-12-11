## UC Berkeley's Statistics 159/259
### Project Group Gamma, Fall Term 2015 

group members: Nima Hejazi, Feng Lin, Luyun Zhao, Xinyue Zhou

topic: [Working memory in healthy and schizophrenic individuals] (https://openfmri.org/dataset/ds000115)

[![Build Status](https://travis-ci.org/berkeley-stat159/project-gamma.svg?branch=master)](https://travis-ci.org/berkeley-stat159/project-gamma?branch=master)
[![Coverage Status](https://coveralls.io/repos/berkeley-stat159/project-gamma/badge.svg?branch=master)](https://coveralls.io/r/berkeley-stat159/project-gamma?branch=master)

## Codebase 

Utils methods are in code/utils. Analysis scripts are in code/ directory. 

## Tests and Coverage

make test runs all the tests for the repo. Methods were extracted into individual modules inside the Utils folder. Plotting helper functions remained inside the analysis scritps. Please note that plotting helpers are not tested.

make coverage runs the test and generates the coverage report on top of that.

## Data

make data downloads all the data except the condition files. This takes around 2 hours. 

Before downloading the data, Data/ is empty except for net_roi.txt, which is from the reference paper supplemental material in the link http://www.ncbi.nlm.nih.gov/pmc/articles/PMC3081915/bin/NIHMS253634-supplement-01.pdf. We manually extracted out the table from Table S1.

make conditionfiles download all the condition files 

The reason that download of condition files is made a separate command because condition files are bundled together with the fMRI raw data on https://www.openfmri.org/dataset/ds000115/. It would take a few hours to download these files but we only need the condition files and not the rest of the bundle. Hence, we made the decision to include the condition files (in txt format) in the data folder along with the repo. For reproducibility, you can run this command to obtain the same condition files.

## Analysis

make analysis runs all the analysis scripts and fill up the results/ directory with diagrams and graphs, which are referenced in the paper.

## Paper

make paper produces the final paper.