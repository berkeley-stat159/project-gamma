"""
This script analyzes correlation between BOLD meansurements and a baseline 
value. The baseline value is extracted from convolution between neural 
prediction values and a gamma hrf function (see conv.py).

We employ two methods to find activation regions. A comparison is made.

Using only the convolved baseline function, we conduct an analysis across
group (con, con_sib, scz, scz_sib) averages.

"""

import project_config
import numpy as np
import nibabel as nib
import os
import matplotlib.pyplot as plt
from general_utils import prepare_standard_data, plane_index_iter, prepare_mask
from correlation import correlation_map_linear, correlation_map_without_convoluation_linear
from gaussian_filter import spatial_smooth
from conv import conv_main
from pca_utils import first_pcs_removed
from os.path import join
from matplotlib import colors
import pdb

TR = project_config.TR

def plot_across_methods(corrs_square_wave, corrs_conv, subject_num, brain_structure, nice_cmap_values, in_brain_mask):
  
  fig = plt.figure()

  nice_cmap = colors.ListedColormap(nice_cmap_values, 'actc')

  for map_index, depth in (((3,2,1), 20),((3,2,3), 40),((3,2,5), 50)):

    plt.subplot(*map_index)
    plt.title("z=%d, %s" % (depth, "sw"))

    corrs_square_wave[~in_brain_mask] = np.nan
    plt.imshow(brain_structure[...,depth], alpha=0.5)
    plt.imshow(corrs_square_wave[...,depth], cmap=nice_cmap, alpha=0.5)
    plt.colorbar()
    plt.tight_layout()

  for map_index, depth in (((3,2,2), 20),((3,2,4), 40),((3,2,6), 50)):

    plt.subplot(*map_index)
    plt.title("z=%d, %s" % (depth, "conv"))

    corrs_conv[~in_brain_mask] = np.nan
    plt.imshow(brain_structure[...,depth], alpha=0.5)
    plt.imshow(corrs_conv[...,depth], cmap=nice_cmap, alpha=0.5)
    plt.colorbar()
    plt.tight_layout()

  plt.savefig(os.path.join(output_filename, "sub%s_voxel_wise_correlation_across_methods.png" % (subject_num)), format='png', dpi=500)

def prepare_residuals(subject_num, task_num, standard_source_prefix):

  data_4d = prepare_standard_data(subject_num, task_num, standard_source_prefix)

  in_brain_mask, in_brain_vols = prepare_mask(data_4d, cutoff)

  data_4d_smoothed = spatial_smooth(data_4d, in_brain_mask, 2.0, 2.0, False)

  in_brain_mask, in_brain_vols = prepare_mask(data_4d_smoothed, cutoff)

  residuals = first_pcs_removed(in_brain_vols, 2)

  return residuals, in_brain_mask


def single_subject_activation_across_methods(standard_source_prefix, cond_filepath, subject_num, task_num, brain_structure, nice_cmap_values):

  residuals, in_brain_mask = prepare_residuals(subject_num, task_num, standard_source_prefix)

  corrs_square_wave = correlation_map_without_convoluation_linear(residuals, cond_filepath)
  corrs_conv = correlation_map_linear(residuals, cond_filepath)

  b_vols_corrs_sw = np.zeros(in_brain_mask.shape)
  b_vols_corrs_sw[in_brain_mask] = corrs_square_wave

  b_vols_corrs_conv = np.zeros(in_brain_mask.shape)
  b_vols_corrs_conv[in_brain_mask] = corrs_conv

  plot_across_methods(b_vols_corrs_sw, b_vols_corrs_conv, subject_num, brain_structure, nice_cmap_values, in_brain_mask)

if __name__ == "__main__":

  brain_structure_path = os.path.join(os.path.dirname(__file__), "..", "data", "mni_icbm152_csf_tal_nlin_asym_09c_2mm.nii")
  nice_cmap_values_path = os.path.join(os.path.dirname(__file__), "..", "data", "actc.txt")

  plt.rcParams['image.cmap'] = 'gray'
  plt.rcParams['image.interpolation'] = 'nearest'

  standard_source_prefix = "/Volumes/G-DRIVE mobile USB/fmri_con/"
  cond_filepath_011 = "/Volumes/G-DRIVE mobile USB/fmri_non_mni/sub011/model/model001/onsets/task001_run001/cond003.txt"
  cond_filepath_prefix = "/Volumes/G-DRIVE mobile USB/fmri_non_mni/"
  output_filename = os.path.join(os.path.dirname(__file__), "..", "data")

  subject_num = "011"
  task_num = "001"
  cond_num = "003"

  cutoff = project_config.MNI_CUTOFF

  brain_structure = nib.load(brain_structure_path).get_data()
  nice_cmap_values = np.loadtxt(nice_cmap_values_path)

  single_subject_activation_across_methods(standard_source_prefix, cond_filepath_011, subject_num, task_num, brain_structure, nice_cmap_values)
  
