"""
Test correlation module

Run with::

    nosetests test_correlation.py
"""
import numpy as np
import os
import nibabel as nib
import numpy.linalg as npl
import math
from .. import correlation

from numpy.testing import assert_array_equal, assert_almost_equal


def test_correlation_map_linear():
  task_fname = os.path.join(os.path.dirname(__file__), "test_data", "test_cond003.txt")
  # assume the first five TRs are already removed
  # faked data ensures that it is perfectly correlated
  data = np.array([[-0.5, -0.2]])
  corrs = correlation.correlation_map_linear(data, task_fname)    
  assert_almost_equal(1.0, corrs[0])

  # according to pearson correlation coefficient, this case is undefined and we
  # assume that the correlation coefficient with a constant time seris is zero
  data = np.array([[3.0, 3.0]])
  corrs = correlation.correlation_map_linear(data, task_fname)    
  assert_almost_equal(0.0, corrs[0])


def test_correlation_map_without_convoluation_linear():
  task_fname = os.path.join(os.path.dirname(__file__), "test_data", "test_cond004.txt")
  # assume the first five TRs are already removed
  # faked data ensures that it is perfectly inversely correlated
  data = np.array([[0.0, 0.0, 0.0, -0.4, -0.4]])
  corrs = correlation.correlation_map_without_convoluation_linear(data, task_fname)    
  assert_almost_equal(corrs[0], -1.0)

  # according to pearson correlation coefficient, this case is undefined and we
  # assume that the correlation coefficient with a constant time seris is zero
  data = np.array([[3.0, 3.0]])
  corrs = correlation.correlation_map_without_convoluation_linear(data, task_fname)    
  assert_almost_equal(0.0, corrs[0])

