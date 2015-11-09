import project_config
import kmeans
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
from sklearn.preprocessing import normalize

"""
Replace these variables before running the script
"""
output_filename = "/Users/fenglin/Desktop/stat159/liam_results/"
subject_num_1 = "001"
subject_num_2 = "002"


def prepare_data(subject_num):
  BOLD_file_1 = '/Users/fenglin/Desktop/stat159/lab/ds115_sub001-005/sub%s/BOLD/task001_run001/bold.nii.gz' % (subject_num)
  BOLD_file_2 = '/Users/fenglin/Desktop/stat159/lab/ds115_sub001-005/sub%s/BOLD/task002_run001/bold.nii.gz' % (subject_num)
  BOLD_file_3 = '/Users/fenglin/Desktop/stat159/lab/ds115_sub001-005/sub%s/BOLD/task003_run001/bold.nii.gz' % (subject_num)

  cond_file_1 = '/Users/fenglin/Desktop/stat159/lab/ds115_sub001-005/sub%s/model/model001/onsets/task001_run001/cond002.txt' % (subject_num)
  cond_file_2 = '/Users/fenglin/Desktop/stat159/lab/ds115_sub001-005/sub%s/model/model001/onsets/task002_run001/cond002.txt' % (subject_num)
  cond_file_3 = '/Users/fenglin/Desktop/stat159/lab/ds115_sub001-005/sub%s/model/model001/onsets/task003_run001/cond002.txt' % (subject_num)

  img_1 = nib.load(BOLD_file_1)
  data_1 = img_1.get_data()
  data_1 = data_1[..., 5:]

  img_2 = nib.load(BOLD_file_2)
  data_2 = img_2.get_data()
  data_2 = data_2[..., 5:]

  img_3 = nib.load(BOLD_file_3)
  data_3 = img_3.get_data()
  data_3 = data_3[..., 5:]

  return data_1, data_2, data_3

def generate_clusters(subject_num, feature_list_1, feature_list_2, feature_list_3):

  n_clusters = 5
  TR = project_config.TR

  labels_1 = kmeans.perform_kMeans_clustering_analysis(feature_list_1, n_clusters)
  labels_2 = kmeans.perform_kMeans_clustering_analysis(feature_list_2, n_clusters)
  labels_3 = kmeans.perform_kMeans_clustering_analysis(feature_list_3, n_clusters)

  labels_list = [labels_1, labels_2, labels_3]

  result_labels = kmeans.merge_n_clusters(labels_list, n_clusters, labels_1.shape)

  return result_labels

def generate_clusters_multiple(subject_num, feature_list_1, feature_list_2, feature_list_3):

  n_clusters = 5
  TR = project_config.TR

  labels_1 = kmeans.perform_kMeans_clustering_analysis(feature_list_1, n_clusters)
  labels_2 = kmeans.perform_kMeans_clustering_analysis(feature_list_2, n_clusters)
  labels_3 = kmeans.perform_kMeans_clustering_analysis(feature_list_3, n_clusters)

  return labels_1, labels_2, labels_3


def plot_all(result_labels_1, result_labels_2, subject_num_1, subject_num_2, title):
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

  plt.savefig(output_filename + "subject%s_%s_kmeans_%s" % (subject_num_1, subject_num_2, title))

  plt.show()

def plot_single_subject(result_labels_1, result_labels_2, result_labels_3, subject_num, title):
  fig = plt.figure()

  ax1 = fig.add_subplot(331)
  ax1.set_title("Subject%s, Task001, z = 15, %s" % (subject_num, title))
  ax1.imshow(result_labels_1[...,15])
  ax2 = fig.add_subplot(332)
  ax2.set_title("Subject%s, Task002, z = 15, %s" % (subject_num, title))
  ax2.imshow(result_labels_2[...,15])
  ax3 = fig.add_subplot(333)
  ax3.set_title("Subject%s, Task003, z = 15, %s" % (subject_num, title))
  ax3.imshow(result_labels_3[...,15])

  ax4 = fig.add_subplot(334)
  ax4.set_title("Subject%s, Task001, z = 20, %s" % (subject_num, title))
  ax4.imshow(result_labels_1[...,20])
  ax5 = fig.add_subplot(335)
  ax5.set_title("Subject%s, Task002, z = 20, %s" % (subject_num, title))
  ax5.imshow(result_labels_2[...,20])
  ax6 = fig.add_subplot(336)
  ax6.set_title("Subject%s, Task003, z = 20, %s" % (subject_num, title))
  ax6.imshow(result_labels_3[...,20])

  ax7 = fig.add_subplot(337)
  ax7.set_title("Subject%s, Task001, z = 25, %s" % (subject_num, title))
  ax7.imshow(result_labels_1[...,25])
  ax8 = fig.add_subplot(338)
  ax8.set_title("Subject%s, Task002, z = 25, %s" % (subject_num, title))
  ax8.imshow(result_labels_2[...,25])
  ax9 = fig.add_subplot(339)
  ax9.set_title("Subject%s, Task003, z = 25, %s" % (subject_num, title))
  ax9.imshow(result_labels_3[...,25])

  plt.savefig(output_filename + "subject%s_kmeans_%s" % (subject_num, title))

  plt.show()


s1_data_1, s1_data_2, s1_data_3 = prepare_data(subject_num_1)
s2_data_1, s2_data_2, s2_data_3 = prepare_data(subject_num_2)

shape = s1_data_1.shape

s1_mean1, s1_mean2, s1_mean3 = np.mean(s1_data_1, axis=3), np.mean(s1_data_2, axis=3), np.mean(s1_data_3, axis=3)
s1_mean1, s1_mean2, s1_mean3 = [elem.reshape(elem.shape + (1,)) for elem in (s1_mean1, s1_mean2, s1_mean3)]
s2_mean1, s2_mean2, s2_mean3 = np.mean(s2_data_1, axis=3), np.mean(s2_data_2, axis=3), np.mean(s2_data_3, axis=3)
s2_mean1, s2_mean2, s2_mean3 = [elem.reshape(elem.shape + (1,)) for elem in (s2_mean1, s2_mean2, s2_mean3)]

"""
Single subject, different tasks, means
"""
s1_mean_1_result, s1_mean_2_result, s1_mean_3_result = generate_clusters_multiple(subject_num_1, s1_mean1, s1_mean2, s1_mean3)
plot_single_subject(s1_mean_1_result, s1_mean_2_result, s1_mean_3_result, subject_num_1, "single_subject_mean")

"""
Across subjects, average of all tasks, means
"""
result_labels_s1_mean = generate_clusters(subject_num_1, s1_mean1, s1_mean2, s1_mean3)
result_labels_s2_mean = generate_clusters(subject_num_2, s2_mean1, s2_mean2, s2_mean3)
plot_all(result_labels_s1_mean, result_labels_s2_mean, subject_num_1, subject_num_2, "mean")

"""
Single subject, different tasks, normalized full time courses
"""
s1_scaled_1, s1_scaled_2, s1_scaled_3 = [normalize(elem.reshape((-1, elem.shape[-1])), axis=0, copy=True).reshape(shape) for elem in (s1_data_1, s1_data_2, s1_data_3)]
s2_scaled_1, s2_scaled_2, s2_scaled_3 = [normalize(elem.reshape((-1, elem.shape[-1])), axis=0, copy=True).reshape(shape) for elem in (s2_data_1, s2_data_2, s2_data_3)]

s1_scaled_1_result, s1_scaled_2_result, s1_scaled_3_result = generate_clusters_multiple(subject_num_1, s1_scaled_1, s1_scaled_2, s1_scaled_3)
plot_single_subject(s1_scaled_1_result, s1_scaled_2_result, s1_scaled_3_result, subject_num_1, "single_subject")

"""
Across subjects, average of all tasks, normalized full time courses
"""
s1_result_labels_data = generate_clusters(subject_num_1, s1_scaled_1, s1_scaled_2, s1_scaled_3)
s2_result_labels_data = generate_clusters(subject_num_2, s2_scaled_1, s2_scaled_2, s2_scaled_3)
plot_all(s1_result_labels_data, s2_result_labels_data, subject_num_1, subject_num_2, "normalized")
