import project_config
from __future__ import division
import sklearn.cluster
import numpy as np
from itertools import product
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D
from general_utils import vol_index_iter


def perform_kMeans_clustering_analysis(img_data, n_clusters):

  """ 
  Cluster voxel time courses into n_clusters based on euclean distances 
  between them. It treats all BOLD values of each time course as a separate
  feature, i.e. in total, img_data.shape[-1] features.

  Parameters
  ----------
  img_data : 4D nii array
  n_clusters : no. of clusters to segregate the time courses into.

  Returns
  -------
  labels_3d : array has the same shape as img_data.shape. Each elem is the
  cluster label of the data.

  """

  kMeans = sklearn.cluster.KMeans(n_clusters)
  img_data_2d = img_data.reshape((-2,img_data.shape[-1]))
  labels = kMeans.fit_predict(img_data_2d)
  return labels.reshape(img_data.shape[:-1])
  

def imshow_clusters(labels_3d, z):
  """
  It shows clustered labels as a 2D image at a depth of z of the volume of 
  the brain.
  """
  plt.imshow(labels_3d[...,z])
  plt.show()

def plot_cluster_3d(labels_3d, cluster_index):
  Xs, Ys, Zs = [], [], []
  for i, j, k in vol_index_iter(labels_3d.shape):
    if labels_3d[i, j, k] == cluster_index:
      Xs.append(i)
      Ys.append(j)
      Zs.append(k)
  fig = plt.figure()
  ax = Axes3D(fig)
  ax.scatter(Xs, Ys, Zs)
  ax.show()

def merge_n_clusters(labels_list, k, shape):

  """
  Merge multiple clusters to form a single cluster.

  Parameters
  ----------
  labels_list : 4D np array: [cluster_index, labels_3d_index_x, labels_3d_index_y, labels_3d_index_z]
  k : no. of clusters
  shape : shape of elems in labels_list

  Returns
  -------
  labels_3d : array has the same shape as img_data.shape. Each elem is the
  cluster label of the merged data.

  """

  result_labels_weights = form_initial_weights(labels_list[0], k)
  for i in range(1, len(labels_list)):
    labels_b = labels_list[i]
    merge_clusters(result_labels_weights, i + 1, labels_b, k)
  return assign_points(result_labels_weights, shape)

def merge_clusters(labels_a_weights, n, labels_b, k):
  """
  The merge strategy is described in Section C: Voting Procedure in the paper 
  Detecting Regions of Interest in fMRI, found in the link 
  http://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=1006726

  Parameters
  ----------
  labels_a_weights : 3D np array: [labels_3d_index_x, labels_3d_index_y, labels_3d_index_z]. This
  is the weights of the primary volume. This is the outcome of merging n volumes of labels together
  n : no. of volumes already merged into labels_a
  labels_b : 3D np array: [labels_3d_index_x, labels_3d_index_y, labels_3d_index_z]. We merge
  this volume of labels into labels_a
  k : no. of clusters

  Returns
  -------
  labels_3d : array has the same shape as img_data.shape. Each elem is the
  cluster label of the merged data.

  """

  assert labels_a_weights.shape[1:] == labels_b.shape

  shape = labels_b.shape

  # separate all points to their respective clusters
  cluster_to_point_map_b = [set() for i in range(k)]
  for i in vol_index_iter(shape):
    cluster_to_point_map_b[labels_b[i]].add(i)

  # compute a k * k matrix A with A[i, j] indicating similarity between cluster i in a and cluster j in b
  inter_cluster_similarity = np.zeros((k, k)) - 1
  for a_i, b_i in product(range(k), range(k)):
    if a_i != b_i:
      inter_cluster_similarity[(a_i, b_i)] = weighted_similarity(labels_a_weights[a_i], cluster_to_point_map_b[b_i])
  
  # based on the inter-cluster-similarity matrix, decide cluster mapping, matching the most similar a-b pair of clusters first.
  cluster_map = {}
  while len(cluster_map) < k:
    a_index, b_index = np.unravel_index(np.argmax(inter_cluster_similarity), (k, k))
    cluster_map[a_index] = b_index
    inter_cluster_similarity[a_index,:] = -1
    inter_cluster_similarity[:, b_index] = -1

  # update weights on the primary volume
  for i, j in cluster_map.items():
    for index in vol_index_iter(shape):
      if labels_a_weights[i][index] == 0: continue
      labels_a_weights[i][index] += n / (n + 1) 
      new_cluster_index = i if index in cluster_to_point_map_b[j] else find_cluster(cluster_to_point_map_b, index)
      labels_a_weights[new_cluster_index][index] += 1 / (n + 1)

def form_initial_weights(labels, n_clusters):
  shape = labels.shape
  result_labels_weights = np.zeros((n_clusters,) + shape)
  for i, j, k in vol_index_iter(shape):
    result_labels_weights[labels[i, j, k], i, j, k] = 1
  return result_labels_weights

def find_cluster(cluster_to_point_map, target):
  for i, points in enumerate(cluster_to_point_map):
    if target in points:
      return i

def assign_points(labels_weights, shape):
  labels = np.zeros((shape))
  for x,y,z in vol_index_iter(shape):
    labels[x,y,z] = np.argmax(labels_weights[:,x,y,z])
  return labels

def weighted_similarity(cluster_a_weights, cluster_b):
  shape = cluster_a_weights.shape
  accu_weight = 0
  for i in vol_index_iter(shape):
    if i in cluster_b: 
      accu_weight += cluster_a_weights[i]
  return accu_weight / np.sum(cluster_a_weights)