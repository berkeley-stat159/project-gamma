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

def spatial_smooth(data_4d, brain_mask, pad_thickness, fwhm):
  """
  Copy data_4d
  """

  sig = sigma(fwhm)

  copy_data = np.array(data_4d)
  for i in range(data_4d.shape[-1]):
    image = data_4d[..., i]
    pad_boundary_per_image(image, brain_mask, pad_thickness)
    copy_data[..., i] = gaussian_filter(image, sig)
  return copy_data

def sigma(fwhm):
  return fwhm / math.sqrt((8.0 * math.log(2.0)))