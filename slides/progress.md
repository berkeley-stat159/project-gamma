% Project Gamma Progress Report
% Nima Hejazi, Feng Lin, Luyun Zhao, Xinyue Zhou
% November 12, 2015


# Background

## The Paper (Nima)

- "Working memory in healthy and schizophrenic individuals"
- Accession number: ds000115 (from the OpenFMRI.org website)
- The paper(s) used ANOVA to explore within/between network connectivity wrt working memory measures.
- The goal was to identify regions contributing to impaired cognitive function in schizophrenics.

## The Data (Nima)

- The method was fcMRI, collecting activation and connectivity (resting) fMRI data.
- 102 subjects: individuals with schizophrenia, their healthy siblings, and controls.
- A task in which subjects identified repeating letters in an interval was administered.
- The data includes anatomical (MRI) and functional (BOLD fMRI) with condition files.

## The Method (Nima)

- After appropriate preprocessing (e.g., Talairach transform), the paper(s) used ANOVA to compare groups.
- The main comparisons examined resting connectivity between and within network regions of interest.
- In order to assess reported analyses, we performed voxel-wise linear models (as seen in lecture).
- Going further, we attempt to define network regions based on activity patterns with machine learning.

# Initial work (~30 sec)

## Exploratory Data Analysis I (Lynn)

- On one subject (Sub011-- Control)
- Load the data --> remove the first five --> remove the RMS outliers
- Correlations between the voxel time course and neural prediction for all voxels
- Residuals analysis to evaluate the basic linear model 

## Exploratory Data Analysis II (Lynn)

- Work on 8 subjects:
	(1) Subject 01 & 02 : SCZ, SCZ-SIB
	(2) Subject 04 & 05 : SCZ, SCZ-SIB
	(3) Subject 10 & 11 : CON-SIB, CON
	(4) Subject 12 & 13:  CON, CON-SIB
	(correlation plots)

# Next steps (~3 min)

## Pre-processing and Validation (Lynn & Xinyue)

- Use the entire data sets of 102 subjects
- Preprocessing: drop first five, remove outliers and normalized the data. 

## Statistical Analysis (Xinyue)
- Identify activation regions 
- Simple linear regression on a per-voxel basis within subjects
- Check the validation of linear model
- K-Means
- Anova


## Unsupervised Learning with K-Means (Liam)

- Use K-means to cluster voxels into 5 groups with different feature set.
- Combine multiple clustering results via a voting algorithm.
- Features used per voxel: 
    (1) mean BOLD measurements over timecouse
    (2) BOLD over timecourse
    (3) normalized BOLD over timecourse

## K-Means Results and Diagnosis
![Comparison across feature sets for the same subject](https://s3-us-west-2.amazonaws.com/stat159datascience/subject_across_methods.pdf)

## Future

- Extend and fine-tune K-Means to focus on functional aspect of the data
    (1) Improve features by inspecting and removing first principle components
    (2) Improve features by 
        i. fitting them to a linear models (e.g. with a drift term in the design matrix) 
        ii. taking the residuals
- Explore 


## Future
![An example: residuals after removing the first two PCs](https://s3-us-west-2.amazonaws.com/stat159datascience/first_pcs_removed.pdf)

# Process (~1 min)

## What has been the hardest part? (...)

- problem 1: fMRI data and having an open assignment (figuring out how to use resources to develop a coherent analytic plan) Xinyue
- problem 2: how to figure appropriate analyses and understand validity of results Liam
- problem 3: dealing with functional connectivity in the data (Nima)

## Success in overcoming obstacles (...)

- Found out that the condition files were not ideal for our analyses (mismatch between the theoretical techniques and the messiness of provided data -- spoke to Matthew about TR issues with time alignment, and had to decide between mean/median/first unit in the timecourses)
- What parts of the class have been the most useful? (1) assignment too open/vagueness and learning to deal with ambiguity in research, (2) collaboration with git (Nima)

## Issues with reproducibility? (...)

- Reproducibility not as much of a problem as initially thought...
- Learning to work with the git model (using code review with merging, etc.) has made reproducibility not too much of an obstacle
