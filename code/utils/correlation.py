"""
EDA: 

Different methods for calculating correlations between the fMRI time courses 
and the neural prediction values.Both methods are needed so that we can compare 
the results from different baseline functions (square wave and gamma function) in the analysis.
"""

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import project_config
import numpy as np
from conv import conv_main
from stimuli_revised import events2neural_rounded
import general_utils as gu

TR = project_config.TR

def correlation_map_linear(data, cond_filename):
  """
  This function computes the correlation matrix based on the baseline method.

  Input: 
    data: brain image data
    cond_filename: condition file which contains the info about time time_course
  Output:
    correlation matrix 
  """
  convolved = conv_main(data.shape[-1] + 5, cond_filename, TR)[5:]
  corrs = np.zeros((data.shape[:-1]))

  for i in range(data.shape[0]):
    r = np.corrcoef(data[i], convolved)[1,0]
    if np.isnan(r):
      r = 0
    corrs[i] = r
  
  return corrs

def correlation_map_without_convoluation_linear(data, cond_filename):
  """
  This is different from correlation_map_without_convoluation in that it accepts a 2d data 
  (n_samples, n_time_slices) and compute the correlations based on the square-wave time course 
  using the given condition file. 

  """
  n_trs = data.shape[-1] + 5
  time_course = events2neural_rounded(cond_filename, TR, n_trs)
  time_course = time_course[5:]
  correlations = np.zeros(data.shape[:-1])

  for i in range(data.shape[0]):
    vox_values = data[i]
    r = np.corrcoef(time_course, vox_values)[1, 0]
    if np.isnan(r):
      r = 0
    correlations[i] = r

  return correlations