% Project Gamma Progress Report
% Nima Hejazi, Liam Feng Lin, Lynn Zhao, Xinyue Zhou
% November 12, 2015


# Background (~30sec)

## The Paper (Nima)

- "Working memory in healthy and schizophrenic individuals"
- Accession number: ds000115 (from OpenFMRI.org)
- The data is mainly functional connectivity imaging (fcMRI)

## The Data (Nima)

- 102 subjects, consisting of healthy individuals and those with Schizophrenia, as well as their siblings
- 2 conditions per subject???

## The Method (Nima)

- The paper used linear regression (ANOVA) after transformation to Talairach space
- The goal was to examine connectivity within four brain network regions (e.g., the default mode network)...


# Initial work (~30 sec)

## Exploratory Data Analysis (Slide 1) (Lynn)

- We downloaded and worked with a subset of the subjects (8 chosen from among the first 15 subjects in the dataset)
- simple plots, summary statistics

## Exploratory Data Analysis (Slide 2) (Lynn)

- fit a basic linear model using OLS on a per-voxel basis within subjects
- used the residuals from the linear model to examine normality of the errors
- tried to find activation regions using the time-coruse (without convolution)
- multiple testing...


# Next steps (~3 min)

## Pre-processing and Validation (Xinyue)

- dropped the first 5 volumes
- for some methods we normalized the data
- on/off times, sometimes we dropped the off times
- Since convolved neural prediction has a unit of 0.1 second while TR has a unit of 2.5 seconds, our strategy picks the median of the span of neural prediction values that correspond to a TR.
- Read on-off neural prediction from condition file in FILENAME, convolve the neural prediction with a predefined HRF function.

## Statistical Analysis (Xinyue)

- fit a basic linear model using OLS on a per-voxel basis within subjects
- used the residuals from the linear model to examine normality of the errors
- tried to find activation regions using the time-coruse (without convolution)
- used convolved neural prediction values as a baseline function, we attempted to visualize the activation regions based on the correlation coefficients...

## Unsupervised Learning with K-Means (Liam)

- used K-means by clustering voxels (in groups of 5) with different features
- features used: (1) mean BOLD over timecouse per voxel, (2) BOLD over timecourse per voxel, (3) normalized BOLD over timecourse per voxel
- pictures...

## Future (Liam)

- stuff we want to do


# Process (~1 min)

## What has been the hardest part? (...)

- problem 1: fMRI data and having an open assignment (figuring out how to use resources to develop a coherent analytic plan) Xinyue
- problem 2: how to figure appropriate analyses and understand validity of results Liam
- problem 3: dealing with functional connectivity in the data

## Success in overcoming obstacles (...)

- Found out that the condition files were not ideal for our analyses (mismatch between the theoretical techniques and the messiness of provided data -- spoke to Matthew about TR issues with time alignment, and had to decide between mean/median/first unit in the timecourses)
- What parts of the class have been the most useful? (1) assignment too open/vagueness and learning to deal with ambiguity in research, (2) collaboration with git

## Issues with reproducibility? (...)

- Reproducibility not as much of a problem as initially thought...
- Learning to work with the git model (using code review with merging, etc.) has made reproducibility not too much of an obstacle
