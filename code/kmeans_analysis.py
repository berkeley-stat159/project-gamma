"""
An EDA script to understand hidden structure of the brain via
kmeans. One limitation of the script is that the built-in method
hides away the choice of initial values for kmeans. One further step to
extend the analysis is to feed in different initialization values
and see whether the cluster labels will differ drastically.
"""


import project_config
import kmeans, os
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
from pca_utils import first_pcs_removed
from gaussian_filter import spatial_smooth
from matplotlib import colors
from general_utils import prepare_standard_data, prepare_mask, form_cond_filepath
from sklearn.decomposition import PCA

def preprocessing_pipeline(subject_num, task_num, standard_source_prefix):

  data_4d = prepare_standard_data(subject_num, task_num, standard_source_prefix)

  in_brain_mask, in_brain_vols = prepare_mask(data_4d, cutoff)

  data_4d_smoothed = spatial_smooth(data_4d, in_brain_mask, 2.0, 2.0, False)

  in_brain_mask, in_brain_vols = prepare_mask(data_4d_smoothed, cutoff)

  residuals = first_pcs_removed(in_brain_vols, 2)

  return residuals, in_brain_mask

def plot_single(labels, subject_num, output_filename, nice_cmap, brain_structure):
  
  fig = plt.figure()

  for map_index, depth in (((3,3,1), 30),((3,3,2), 35),((3,3,3), 40),
                          ((3,3,4), 45),((3,3,5), 50),((3,3,6), 55),
                          ((3,3,7), 60),((3,3,8), 65),((3,3,9), 70)):
    ax = fig.add_subplot(*map_index)
    ax.set_title("z=%d" % (depth))
    ax.imshow(brain_structure[...,40], alpha=0.5)
    ax.imshow(labels[...,depth], cmap=nice_cmap, alpha=0.5)

  plt.tight_layout()
  plt.suptitle("Sub011,control,kmeans with k=6")
  plt.savefig(os.path.join(output_filename, "sub011_kmeans_6_groups_smoothed.png"), format='png', dpi=500)


def single_subject_kmeans(standard_source_prefix, cond_filepath, subject_num, task_num):

  residuals, in_brain_mask = preprocessing_pipeline(subject_num, task_num, standard_source_prefix)

  labels = kmeans.perform_kMeans_clustering_analysis(residuals.reshape((-1, residuals.shape[-1])), 6)

  b_vols = np.zeros(in_brain_mask.shape)
  b_vols[in_brain_mask] = labels
  b_vols[~in_brain_mask] = np.nan

  return b_vols


if __name__ == "__main__": 

  data_dir_path = os.path.join(os.path.dirname(__file__), "..", "data")
  brain_structure_path = os.path.join(data_dir_path, "mni_icbm152_csf_tal_nlin_asym_09c_2mm.nii")

  standard_source_prefix = data_dir_path
  cond_filepath_011 = form_cond_filepath("011", "001", "003", data_dir_path)
  output_filename = os.path.join(os.path.dirname(__file__), "..", "results")

  subject_num = "011"
  task_num = "001"
  cond_num = "002"

  plt.rcParams['image.cmap'] = 'gray'
  plt.rcParams['image.interpolation'] = 'nearest'

  cutoff = project_config.MNI_CUTOFF

  nice_cmap_values_path = os.path.join(data_dir_path, "actc.txt")
  brain_structure = nib.load(brain_structure_path).get_data()
  nice_cmap_values = np.loadtxt(os.path.join(data_dir_path, "actc.txt"))
  nice_cmap = colors.ListedColormap(nice_cmap_values, 'actc')

  labeled_b_vols = single_subject_kmeans(standard_source_prefix, cond_filepath_011, subject_num, task_num)
  plot_single(labeled_b_vols, subject_num, output_filename, nice_cmap, brain_structure)