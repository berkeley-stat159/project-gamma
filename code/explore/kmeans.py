import sklean.cluster

def perform_kMeans_clustering_analysis(img_data, n_clusters, z):

  """ 
  Cluster voxel time courses into n_clusters based on euclean distances 
  between them. It treats all BOLD values of each time course as a separate
  feature, i.e. in total, img_data.shape[-1] features. It then shows clustered
  labels as a 2D image at a depth of z of the volume of the brain.
  """

  kMeans = sklearn.cluster.KMeans(nClusters)
  img_data_2d = img_data.reshape((-2,img_data.shape[-1]))
  labels = kMeans.fit_predict(img_data_2d)
  indices_3d = labels.reshape(img_data.shape[:-1])
  plt.imshow(indices_3d[...,z])
  plt.show()
