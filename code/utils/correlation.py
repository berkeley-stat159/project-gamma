import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import project_config
import numpy as np
from conv import conv_main
from stimuli_revised import events2neural_rounded
import general_utils as gu

TR = project_config.TR

def correlation_map(data, cond_filename):
  """
  Generate a cross-correlation per voxel between BOLD signals and a convolved 
  gamma baseline function. Assume that the first 5 images are already dropped.
  """
  convolved = conv_main(data.shape[-1] + 5, cond_filename, TR)[5:]
  corrs = np.zeros((data.shape[:-1]))

  for i in gu.vol_index_iter(data.shape[:-1]):
    r = np.corrcoef(data[i], convolved)[1,0]
    if np.isnan(r):
      r = 0
    corrs[i] = r
  
  return corrs

def correlation_map_linear(data, cond_filename):
  """
  This is different from correlation_map in that it accepts a 2d data 
  (n_samples, n_time_slices) so that it is suitable for working with
  brain masks.
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
  (n_samples, n_time_slices) so that it is suitable for working with
  brain masks.
  """
  n_trs = data.shape[-1] + 5
  time_course = events2neural_rounded(cond_filename, TR, n_trs)[5:]
  correlations = np.zeros(data.shape[:-1])

  for i in range(data.shape[0]):
    vox_values = data[i]
    r = np.corrcoef(time_course, vox_values)[1, 0]
    if np.isnan(r):
      r = 0
    correlations[i] = r

  return correlations


def correlation_map_without_convoluation(data, cond_filename):
  """
  Generate a cross-correlation per voxel between BOLD signals and a square wave
  baseline function, which represents the boolean array of the on-off time 
  course. Assume that the first 5 images are already dropped.
  """
  n_trs = data.shape[-1] + 5
  time_course = events2neural_rounded(cond_filename, TR, n_trs)[5:]
  correlations = np.zeros(data.shape[:-1])

  for i in gu.vol_index_iter(data.shape[:-1]):
    vox_values = data[i]
    r = np.corrcoef(time_course, vox_values)[1, 0]
    if np.isnan(r):
      r = 0
    correlations[i] = r

  return correlations

