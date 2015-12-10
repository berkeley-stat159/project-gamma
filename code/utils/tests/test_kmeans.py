"""
Test kmeans module

Run with::

    nosetests conv.py
"""
import numpy as np
import os
from .. import kmeans

from numpy.testing import assert_array_equal, assert_almost_equal

def test_perform_kMeans_clustering_analysis():
  feature_data = np.zeros((3,3,3,1))
  # only one value is large. Given k = 2, this value will be clusterd to
  # a group by itself
  feature_data[1,1,1] = 10000
  labels = kmeans.perform_kMeans_clustering_analysis(feature_data, 2)
  # the check is necessary because labeling is not guaranteed to be
  # determinstic for kmeans
  
  if labels[0,0,0] == 1:
    labels = 1 - labels

  expected = np.zeros((3,3,3))
  expected[1,1,1] = 1
  assert_almost_equal(labels, expected)
