"""
Wrapper for k-means clustering that takes cares of reshaping and generating labels.
"""

from __future__ import division
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import project_config
import sklearn.cluster

def perform_kMeans_clustering_analysis(feature_data, n_clusters):

  """ 
  Cluster voxel time courses into n_clusters based on euclean distances 
  between them. It treats all processed BOLD images of each time course as 
  a separate feature, i.e. in total, img_data.shape[-1] features.

  Parameters
  ----------
  feature_data : dimension 1:3 is 3d volumn. The last dimension is a list of feature values.
  n_clusters : no. of clusters to segregate the time courses into.

  Returns
  -------
  labels : array has the same shape as img_data.shape. Each elem is the
  cluster label of the data.

  """

  kMeans = sklearn.cluster.KMeans(n_clusters)
  feature_data_2d = feature_data.reshape((-1,feature_data.shape[-1]))
  labels = kMeans.fit_predict(feature_data_2d)
  return labels.reshape(feature_data.shape[:-1])