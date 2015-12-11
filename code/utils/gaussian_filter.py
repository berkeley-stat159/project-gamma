"""
Wrapper for gaussian filter that supports padding of the
boundary with voxel values inside the brain boundary. The
purpose of padding is so that gaussian filter results
are not distorted too badly nearly the brain boundary because
of the extremely low fMRI measurements outside the brain
boundary.
"""

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import project_config
from scipy.spatial import cKDTree
from general_utils import vol_index_iter
from scipy.ndimage.filters import gaussian_filter
import numpy as np
import math

def pad_boundary_per_image(data, brain_mask, pad_thickness):
  brain_points, non_brain_points = [], []
  for i in vol_index_iter(data.shape):
    if brain_mask[i]:
      brain_points.append(i)
    else:
      non_brain_points.append(i)
  tree = cKDTree(np.array(brain_points))
  non_brain_points = [i for i in vol_index_iter(data.shape) if (not brain_mask[i])]
  neighbors_list = tree.query_ball_point(non_brain_points, pad_thickness)
  for list_i, neighbors in enumerate(neighbors_list):  
    i = non_brain_points[list_i]
    if len(neighbors) != 0:
      data[i] = np.mean([data[brain_points[j]] for j in neighbors])

def spatial_smooth(data_4d, brain_mask, pad_thickness, sigma, should_pad):
  copy_data = np.array(data_4d)
  if should_pad:
    for i in range(data_4d.shape[-1]):
      print "padded volumn " + str(i)
      pad_boundary_per_image(data_4d[..., i], brain_mask, pad_thickness)
  return gaussian_filter(copy_data, [sigma, sigma, sigma, 0])