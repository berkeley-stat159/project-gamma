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
from kmeans_analysis import plot_all
from general_utils import vol_index_iter, prepare_standard_data, plane_index_iter, prepare_mask, form_cond_filepath
import matplotlib.pyplot as plt
from correlation import correlation_map_linear, correlation_map_without_convoluation_linear
from conv import conv_main
from stimuli_revised import events2neural_rounded
from pca_utils import first_pcs_removed
from os.path import join
import pdb

TR = project_config.TR

def plot_across_methods(corrs_square_wave, corrs_conv, subject_num):
  
  fig = plt.figure()

  for map_index, depth in ((321, 20),(323, 40),(325, 50)):

    ax = fig.add_subplot(map_index)
    ax.set_title("Subject%s, z = %d, %s" % (subject_num, depth, "sw"))
    ax.imshow(corrs_square_wave[...,depth], interpolation="nearest", cmap="gray")

    plane = corrs_square_wave[...,depth]
    points = [(i[1],i[0]) for i in plane_index_iter(plane.shape) if plane[i] >= 0.20]
    if len(points) > 0:
      ax.scatter(*zip(*points))

  for map_index, depth in ((322, 20),(324, 40),(326, 50)):

    ax = fig.add_subplot(map_index)
    ax.set_title("Subject%s, z = %d, %s" % (subject_num, depth, "conv"))
    ax.imshow(corrs_conv[...,depth], interpolation="nearest", cmap="gray")

    plane = corrs_conv[...,depth]
    points = [(i[1],i[0]) for i in plane_index_iter(plane.shape) if plane[i] >= 0.20]
    if len(points) > 0:
      ax.scatter(*zip(*points))

  plt.tight_layout()
  plt.savefig(output_filename + "activation_region_across_methods_same_sub.pdf", format='pdf', dpi=1000)      

  plt.show()

def prepare_residuals(subject_num, task_num, standard_source_prefix):

  data_4d = prepare_standard_data(subject_num, task_num, standard_source_prefix)

  # mean_vols = np.mean(data_4d, axis=-1)
  # plt.hist(np.ravel(mean_vols), bins=100)
  # plt.show()

  # Chose cutoff = 5500 from the histogram
  cutoff = 5500

  in_brain_mask, in_brain_vols = prepare_mask(data_4d, cutoff)

  # We justified in pca_analysis.py that the first two PCs represent anatomical features.

  residuals = first_pcs_removed(in_brain_vols, 2)
  return residuals, in_brain_mask


def single_subject_activation_across_methods(standard_source_prefix, cond_filepath, subject_num, task_num):

  residuals, in_brain_mask = prepare_residuals(subject_num, task_num, standard_source_prefix)

  corrs_square_wave = correlation_map_without_convoluation_linear(residuals, cond_filepath)
  corrs_conv = correlation_map_linear(residuals, cond_filepath)

  b_vols_corrs_sw = np.zeros(in_brain_mask.shape)
  b_vols_corrs_sw[in_brain_mask] = corrs_square_wave

  b_vols_corrs_conv = np.zeros(in_brain_mask.shape)
  b_vols_corrs_conv[in_brain_mask] = corrs_conv

  plot_across_methods(b_vols_corrs_sw, b_vols_corrs_conv, subject_num)

def plot_group(group_activation_result, output_filename):
  
  fig = plt.figure()

  for map_index, depth, group in (((4,3,1), 20, "fmri_con"),((4,3,2), 40, "fmri_con"),((4,3,3), 50, "fmri_con"),
                                 ((4,3,4), 20, "fmri_con_sib"),((4,3,5), 40, "fmri_con_sib"),((4,3,6), 50, "fmri_con_sib"),
                                 ((4,3,7), 20, "fmri_scz"),((4,3,8), 40, "fmri_scz"),((4,3,9), 50, "fmri_scz"),
                                 ((4,3,10), 20, "fmri_scz_sib"),((4,3,11), 40, "fmri_scz_sib"),((4,3,12), 50, "fmri_scz_sib")):

    ax = fig.add_subplot(*map_index)
    ax.set_title("z=%d,%s" % (depth, group))
    ax.imshow(group_activation_result[group][...,depth], interpolation="nearest", cmap="gray")

    plane = group_activation_result[group][...,depth]
    points = [(i[1],i[0]) for i in plane_index_iter(plane.shape) if plane[i] >= 0.10]
    if len(points) > 0:
      ax.scatter(*zip(*points))

  plt.tight_layout()
  plt.savefig(output_filename + "activation_regions_across_groups.pdf", format='pdf', dpi=1000)

  plt.show()

def group_activation_conv(standard_group_source_prefix, cond_filepath_prefix, cond_num, grouping = None):
  task_nums = ("001", "002", "003")
  res = {}

  group_info = grouping if grouping else project_config.group
  
  for group, subject_nums in group_info.items():
    group_corrs_conv = []
    for sn in subject_nums:
      residuals, masks = zip(*[prepare_residuals(sn, tn, join(standard_group_source_prefix, group)) for tn in task_nums])
      corrs_conv = [correlation_map_linear(r, form_cond_filepath(sn, tn, cond_num, cond_filepath_prefix)) for r, tn in zip(residuals, task_nums)]
      b_vols = [np.zeros(masks[0].shape) for i in task_nums]
      b_vols[0][masks[0]] = corrs_conv[0]
      b_vols[1][masks[1]] = corrs_conv[1]
      b_vols[2][masks[2]] = corrs_conv[2]
      group_corrs_conv.extend(b_vols)
    res[group] = np.mean(group_corrs_conv, axis=0)
  return res

if __name__ == "__main__":

  standard_source_prefix = "/Volumes/G-DRIVE mobile USB/fmri_con/"
  standard_group_source_prefix = "/Volumes/G-DRIVE mobile USB/"
  cond_filepath_011 = "/Volumes/G-DRIVE mobile USB/fmri_non_mni/sub011/model/model001/onsets/task001_run001/cond002.txt"
  cond_filepath_prefix = "/Volumes/G-DRIVE mobile USB/fmri_non_mni/"
  output_filename = "/Users/fenglin/Desktop/stat159/liam_results/"

  subject_num = "011"
  task_num = "001"
  cond_num = "002"

  single_subject_activation_across_methods(standard_source_prefix, cond_filepath_011, subject_num, task_num)



  small_group_info = {"fmri_con":("011", "012", "015", "020"),
          "fmri_con_sib":("010", "013", "014", "016"),
          "fmri_scz":("007", "009", "017", "027"),
          "fmri_scz_sib":("006", "008", "018", "019")}


  results = group_activation_conv(standard_group_source_prefix, cond_filepath_prefix, cond_num, small_group_info)
  plot_group(results, output_filename)


  
