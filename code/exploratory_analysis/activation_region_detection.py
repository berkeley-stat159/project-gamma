"""
This script analyzes correlation between BOLD meansurements and a baseline 
value. The baseline value is extracted from convolution between neural 
prediction values and a gamma hrf function (see conv.py).

We employ two methods to find activation regions. A comparison is made.

"""

import project_config
import numpy as np
import nibabel as nib
from kmeans_analysis import prepare_data, plot_all, plot_single_subject
import general_utils
import matplotlib.pyplot as plt
from conv import conv_main

"""
Replace these variables before running the script
"""
subject_num_1 = "001"
subject_num_2 = "002"

TR = project_config.TR

def correlation_map(data, cond_filename):
  tr_times = np.arange(0, 30, TR)
  convolved = conv_main(data.shape[-1], cond_filename, TR)

  corrs = np.zeros((data.shape[:-1]))
  for i in general_utils.vol_index_iter(data.shape[:-1]):
    corrs[i] = np.corrcoef(data[i], convolved)[1,0]
  return corrs

def prepare_cond_filenames(subject_num):
  cond_file_1 = '/Users/fenglin/Desktop/stat159/lab/ds115_sub001-005/sub%s/model/model001/onsets/task001_run001/cond002.txt' % (subject_num)
  cond_file_2 = '/Users/fenglin/Desktop/stat159/lab/ds115_sub001-005/sub%s/model/model001/onsets/task002_run001/cond002.txt' % (subject_num)
  cond_file_3 = '/Users/fenglin/Desktop/stat159/lab/ds115_sub001-005/sub%s/model/model001/onsets/task003_run001/cond002.txt' % (subject_num)
  return cond_file_1, cond_file_2, cond_file_3

def correlation_map_without_convoluation(data, cond_filename):
  n_trs = img.shape[-1]
  time_course = events2neural_rounded(cond_filename, TR, n_trs) 
  time_course=time_course[5:]
  correlations = np.zeros(data.shape[:-1])
  for i in general_utils.vol_index_iter(data.shape[:-1]):
    vox_values = data[i]
    correlations[i] = np.corrcoef(time_course, vox_values)[1, 0]

s1_data_1, s1_data_2, s1_data_3 = prepare_data(subject_num_1)
s1_cond_1, s1_cond_2, s1_cond_3 = prepare_cond_filenames(subject_num_1)
s2_data_1, s2_data_2, s2_data_3 = prepare_data(subject_num_2)
s2_cond_1, s2_cond_2, s2_cond_3 = prepare_cond_filenames(subject_num_2)

shape = s1_data_1.shape
TR = project_config.TR

s1_data_1_corrs, s1_data_2_corrs, s1_data_3_corrs = correlation_map(s1_data_1, s1_cond_1), correlation_map(s1_data_2, s1_cond_2), correlation_map(s1_data_3, s1_cond_3)
s2_data_1_corrs, s2_data_2_corrs, s2_data_3_corrs = correlation_map(s2_data_1, s2_cond_1), correlation_map(s2_data_2, s2_cond_2), correlation_map(s2_data_3, s2_cond_3)

"""
Across subject, task 1
"""
plot_all(s1_data_1_corrs, s2_data_1_corrs, subject_num_1, subject_num_2, "activation_region", "across_subject")
"""
Single subject, different task
"""
plot_single_subject(s1_data_1_corrs, s1_data_2_corrs, s1_data_3_corrs, subject_num_1, "activation_region", "across_subject")

s1_data_1_corrs_no_convol, s1_data_2_corrs_no_convol, s1_data_3_corrs_no_convol = correlation_map_without_convoluation(s1_data_1, s1_cond_1), correlation_map_without_convoluation(s1_data_2, s1_cond_2), correlation_map_without_convoluation(s1_data_3, s1_cond_3)
s2_data_1_corrs_no_convol, s2_data_2_corrs_no_convol, s2_data_3_corrs_no_convol = correlation_map_without_convoluation(s2_data_1, s2_cond_1), correlation_map_without_convoluation(s2_data_2, s2_cond_2), correlation_map_without_convoluation(s2_data_3, s2_cond_3)

"""
Across subject, task 1, without convolution
"""
plot_all(s1_data_1_corrs, s2_data_1_corrs, subject_num_1, subject_num_2, "activation_region", "across_subject_without_convolution")

"""
Single subject, different task, without convolution
"""
plot_single_subject(s1_data_1_corrs, s1_data_2_corrs, s1_data_3_corrs, subject_num_1, "activation_region", "across_subject_without_convolution")
