% Project Gamma Progress Report
% Nima Hejazi, Feng Lin, Luyun Zhao, Xinyue Zhou
% December 1, 2015

# Background

## Essential Background

- "Working memory in healthy and schizophrenic individuals"
- Accession number: ds000115 (from the OpenFMRI.org website)
- The paper(s) used ANOVA to explore within/between network connectivity wrt working memory measures.
- The goal was to identify regions contributing to impaired cognitive function in schizophrenics.
- The method was fcMRI, collecting activation and connectivity (resting) fMRI data.
- 102 subjects: individuals with schizophrenia, their healthy siblings, and controls.
- N-back memeory tasks

## Goals (GLM)

- A target is the event that the current letter that is the same as the nth preceeding letter
- A non-target is the opposite of a target, in which the current letter is not the same
- An activation cluster: to a group of neighboring voxels activated beyond certain statistical threshold (t-test p value) by defined events
- Goal of GLM: detect the activation clusters of target and non-target events in one subject in the control (healthy) group
- Subgoals: 
  (1) Compare 0-back and 2-back tasks for one subject
  (2) Identify noise regressors so that we can remove them in data for connectivity analysis

## Goals (Connectivity)

- The goal of connectivity analysis is to compare the functional brain connectivity, measured by ROI-ROI correlations of 2-back task data between the four networks of the brain (DMN,FP,CO,CER), across CON and SCZ groups. 

	(1) 2-back task: difficult to perform, requires highest memory load, more likely to reveal the difference
	(2) four networks: DMN,FP,CO,CER are thought to be critical for cognitive function and defined in the paper		 	 	 		
	(3) CON: control and their siblings
        	     SCZ: schizophrenia and their siblings

## The Method (GLM - Confition Files)

- cond001: Start cues for both blocks of the run
- cond002: The letters presenteed to the subject. The intensities are all one becasue there is only one homogeneous event type
- cond003: The target and non-target events during the run
- cond004: Done cues for both blocks of the run
- cond005: Start and durations of the two blocks with a rest (i.e. fixation) period in between the blocks.
- cond006: Excludede; Unknown and unexplained in the paper
- cond007: Errors made by the subject when responding for each letter shown whether it was the same as a pre-specified (0-back) or preceding (1,2-back) letter



## The Method (GLM - Regressors)

- Condition file on-off time course at a time unit of 0.01 TR with a gamma function and take the convolved values at the start of each TR
- reg001: Convolution of target events
- reg002: Convolution of non-target events
- reg003: On-off time course for the two blocks
- reg004: Convolution of start cues. Separated from the target and non-target regressors because it is not likely to involve heavy working memory load compared to task regressors
- reg005: Convolution of done cues
- reg006 and reg007: A linear drift term and a quadratic drift term as potential nuisansance regressors. Their significance is investigated below
[graph]
- reg008 and reg009: The first two principal components of the data. Based on the projections shown below, we decide that the first two are not functional features.
![Control subject, First four principal components]
- reg010: Intercept term.

## The Method (GLM - Analysis)
- Standard processed brain -> pad brain boundary -> pass through Gaussian filter of sigma=2 -> GLM
- For each $\beta$ on each voxel time course, a linear regression two-tailed t-test
    (1) null hypothesis: $\beta=0$ 
    (2) alternative hypothesis: $\beta\neq0$
- Assumptions: 
    (1) Residuals of each linear model are independent and identically distribued (i.i.d)
    (2) Residuals for the model are normally distributed
        i. Shapiro-Wilk Test per voxel: 37703 out of 207766 voxels failed
        ii. Test normality of several models together. perform Hochberg (6 / 207766 voxels failed) and Benjamini-Hochberg tests (all passed)

## Method (Connectivity)

- Remove noise regressors identified in the GLM from the voxel time series
- Extract the voxels per ROI and validate: given the center index and the diameter
	(1) ROIs are non-overlapping
	(2) regions vs cubic regions


## Method (Connectivity)

- Compute the ROI-ROI correlation
	(1) for each ROI, get the average time series;
	(2) for any two networks, obtain the correlation matrix containing the r-values of any two ROIs for the two networks;
	(3) for each subject, we get the correlation matrix;  
	(4) for several subjects, group the r-values into CON and SCZ group based on the category of the subjects
	pic to explain the process

## Results (GLM)


## Results (Connectivity)
- Analyze on 20 subjects, 12 SCZ and 8 CON 
- the individuals with schizophrenia and their siblings (SCZ) showed an overall reduction in connectivity between the cognitive control networks as compared to CON 
	 	 	 							
## 
![Boxplots of the r-values](connectivity_plot.png)

## Discussion

- Expand the number of sujects
- Perform permutation test to statistically validate the difference of connectivity between SCZ and CON

