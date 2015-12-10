"""
Test hypothesis module

Run with::

    nosetests test_hypothesis.py
"""
import numpy as np
import nibabel as nib
import os
import numpy.linalg as npl
import math
from .. import hypothesis

from numpy.testing import assert_almost_equal, assert_equal

def test_hypothesis():
  X = np.ones((5,1))
  Y = np.ones((5,2)) * 100.0
  betas_hat = np.ones((1,2)) * 100.0
  t_values = hypothesis.compute_t_values(X, betas_hat, Y, 0)
  # t_values should be inf because both models are a perfit fit
  assert_almost_equal(t_values, [float('inf'), float('inf')])
