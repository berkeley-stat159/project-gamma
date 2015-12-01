import project_config
import kmeans
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
from pca_utils import first_pcs_removed
from general_utils import prepare_data_single, prepare_mask
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

def prepare_residuals(subject_num, task_num, standard_source_prefix):

  data_4d = prepare_data_single(subject_num, task_num, True, standard_source_prefix)

  # mean_vols = np.mean(data_4d, axis=-1)
  # plt.hist(np.ravel(mean_vols), bins=100)
  # plt.show()

  # Chose cutoff = 5500 from the histogram
  cutoff = 5500

  in_brain_mask, in_brain_vols = prepare_mask(data_4d, cutoff)

  # We justified in pca_analysis.py that the first two PCs represent anatomical features.

  residuals = first_pcs_removed(in_brain_vols, 2)
  return residuals, in_brain_mask

def plot_single(labels, subject_num, output_filename):
  
  fig = plt.figure()

  for map_index, depth in (((3,3,1), 30),((3,3,2), 35),((3,3,3), 40),
                          ((3,3,4), 45),((3,3,5), 50),((3,3,6), 55),
                          ((3,3,7), 60),((3,3,8), 65),((3,3,9), 70)):
    ax = fig.add_subplot(*map_index)
    ax.set_title("z=%d" % (depth))
    ax.imshow(labels[...,depth], interpolation="nearest", cmap="gray")

  plt.tight_layout()
  plt.suptitle("Sub011, Control Group")
  plt.savefig(output_filename + "kmeans_across_cluters_single_sub.pdf", format='pdf', dpi=1000)
  plt.show()


def single_subject_kmeans(standard_source_prefix, cond_filepath, subject_num, task_num):

  residuals, in_brain_mask = prepare_residuals(subject_num, task_num, standard_source_prefix)

  labels = kmeans.perform_kMeans_clustering_analysis(residuals.reshape((-1, residuals.shape[-1])), 6)

  b_vols = np.zeros(in_brain_mask.shape) + float('inf')
  b_vols[in_brain_mask] = labels

  return b_vols


if __name__ == "__main__": 

  standard_source_prefix = "/Volumes/G-DRIVE mobile USB/fmri_con/"
  standard_group_source_prefix = "/Volumes/G-DRIVE mobile USB/"
  cond_filepath_011 = "/Volumes/G-DRIVE mobile USB/fmri_non_mni/ds115_sub010-014/sub011/model/model001/onsets/task001_run001/cond002.txt"
  cond_filepath_prefix = "/Volumes/G-DRIVE mobile USB/fmri_non_mni/"
  output_filename = "/Users/fenglin/Desktop/stat159/liam_results/"

  subject_num = "011"
  task_num = "001"
  cond_num = "002"

  labels = single_subject_kmeans(standard_source_prefix, cond_filepath_011, subject_num, task_num)
  plot_single(labels, subject_num, output_filename)