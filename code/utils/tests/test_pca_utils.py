"""
Test pca_utils module

Run with::

    nosetests test_pca_utils.py
"""
import numpy as np
import nibabel as nib
import os
import numpy.linalg as npl
import math
from .. import pca_utils

from numpy.testing import assert_almost_equal, assert_equal

def test_pca_utils():
  data_2d = np.array([[5000,80000],[100,10],[20,30],[40,60]])
  actual = pca_utils.first_pcs_removed(data_2d, 2)
  assert_almost_equal(actual, np.zeros(data_2d.shape))

  data_2d = np.array([[5000,3],[5000,10],[5000,30],[5000,60]])
  actual = pca_utils.first_pcs_removed(data_2d, 1)
  assert_almost_equal(actual, np.zeros(data_2d.shape))

def test_project_onto_first_pcs():
  data_2d = np.array([[0,0],[0,1],[0,2],[0,3]])
  actual = pca_utils.project_onto_first_pcs(data_2d, 2)
  expected = np.array([[-1.5,0],[-0.5,0],[0.5,0],[1.5,0]])
  assert_almost_equal(actual, expected)  
