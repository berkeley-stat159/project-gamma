"""
Helper functions for connectivity analysis including separating network regions down to voxels and calculating correlations.
"""

from __future__ import division
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import project_config
import random
import numpy as np

def permute (r1,r2):
  """
  This function performs the permuation test to two lists of r-values (r1:scz; r2:con).
  Ho: mu_r1 = mu_r2
  H1: muri < mu_r2
  input:
  1.r1 and r2 are two arrays containing the r-values
  output:
  1. one sided p-values
  """
  n1 = len(r1)
  n2 = len(r2)
  t_obs = np.mean(r1)-np.mean(r2)
  pool = r1+r2
  diff = []
  for i in range(0,1000):
    sample = random.sample(pool,n1)
    diff.append(np.mean(sample)-(sum(pool)-sum(sample))/n2)
  p_value = sum(list(i <= t_obs for i in diff))/len(diff)
  return p_value

def roi_cor (data, roi1,roi2):
  """
  Parameters
  ----------
  roi1, roi2: two list of tuples indicating the voxel coordinates, only 
  necessary to call this method if roi1 and roi2 are different ROIs
  data: BOLD time courses
  
  Returns
  ----------
  Correlations among voxels in ROI1 and ROI2
  """

  timecourse1 = [data[roi1[i]] for i in range(0,len(roi1))]
  avg_time1 = np.mean(timecourse1,axis=0)
  timecourse2 = [data[roi2[j]] for j in range(0,len(roi2))]
  avg_time2 = np.mean(timecourse2,axis=0)
  cor = np.corrcoef(avg_time1,avg_time2)[1,0]
  return cor

def network_cor(data, net1, net2, is_same):
  """
  Parameters
  ----------

  net1, net2 : dictionaries of ROI names to voxels belonging to that ROI

  Returns
  ----------

  A list of correlations
  """

  roi_names_1 = net1.keys()
  roi_names_2 = net2.keys()

  if is_same:
    z_values_list = []
    for i in range(0,len(roi_names_1)):
      for j in range(i + 1,len(roi_names_2)):
        roi_name_1 = roi_names_1[i]
        roi_name_2 = roi_names_2[j]
        val = roi_cor(data,net1[roi_name_1],net2[roi_name_2])
        z_values_list.append(val)
    return z_values_list

  else:
    return [roi_cor(data,voxels_1, voxels_2) for roi_name_1, voxels_1 in net1.items() for roi_name_2, voxels_2 in net2.items()]

def c_within (data,dic):
  """
  Parameters
  ----------
  dic: a dictionary mapping networks to individual ROIs to voxels belonging to the ROI key
  data: BOLD time courses

  Returns
  ----------
  A dictionary with the same structure as dic but with ROI centers replaced by correlation values,
  investigating intra-network connectivity
  """
  return {network_name: network_cor(data,rois,rois, True) for network_name, rois in dic.items()}


def c_between (data,dic):
  """
  Parameters
  ----------
  dic: a dictionary mapping networks to individual ROIs to voxels belonging to the ROI key
  data: BOLD time courses

  Returns
  ----------
  A dictionary with the same structure as dic but with ROI centers replaced by correlation values,
  investigating inter-network connectivity
  """

  z_bet = {}
  networks = dic.keys()
  for i in range(0,len(networks)):
    for j in range(i+1,len(networks)):
      network_name_1 = networks[i]
      network_name_2 = networks[j]
      z_bet[network_name_1+"-"+network_name_2] = network_cor(data,dic[network_name_1],dic[network_name_2], False)
  return z_bet
