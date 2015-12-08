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


def generate_clusters(subject_num, feature_list_1, feature_list_2, feature_list_3, n_clusters = 5):

  labels_list = generate_clusters_multiple(subject_num, feature_list_1, feature_list_2, feature_list_3, n_clusters)

  result_labels = kmeans.merge_n_clusters(labels_list, n_clusters, feature_list_1.shape)

  return result_labels

def generate_clusters_multiple(subject_num, feature_list_1, feature_list_2, feature_list_3, n_clusters = 5):

  labels_1 = kmeans.perform_kMeans_clustering_analysis(feature_list_1, n_clusters)
  labels_2 = kmeans.perform_kMeans_clustering_analysis(feature_list_2, n_clusters)
  labels_3 = kmeans.perform_kMeans_clustering_analysis(feature_list_3, n_clusters)

  return labels_1, labels_2, labels_3


def plot_all(result_labels_1, result_labels_2, subject_num_1, subject_num_2, analysis_name, title):
  fig = plt.figure()

  ax1 = fig.add_subplot(321)
  ax1.set_title("Subject%s, z = 15, %s" % (subject_num_1, title))
  ax1.imshow(result_labels_1[...,15])
  ax2 = fig.add_subplot(323)
  ax2.set_title("Subject%s, z = 20, %s" % (subject_num_1, title))
  ax2.imshow(result_labels_1[...,20])
  ax3 = fig.add_subplot(325)
  ax3.set_title("Subject%s, z = 25, %s" % (subject_num_1, title))
  ax3.imshow(result_labels_1[...,25])

  ax4 = fig.add_subplot(322)
  ax4.set_title("Subject%s, z = 15, %s" % (subject_num_2, title))
  ax4.imshow(result_labels_2[...,15])
  ax5 = fig.add_subplot(324)
  ax5.set_title("Subject%s, z = 20, %s" % (subject_num_2, title))
  ax5.imshow(result_labels_2[...,20])
  ax6 = fig.add_subplot(326)
  ax6.set_title("Subject%s, z = 25, %s" % (subject_num_2, title))
  ax6.imshow(result_labels_2[...,25])

  plt.savefig(output_filename + "subject%s_%s_%s_%s" % (subject_num_1, subject_num_2, analysis_name, title))

  plt.show()

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