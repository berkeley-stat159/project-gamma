"""
Test conv module

Run with::

    nosetests conv.py
"""
import numpy as np
import os
from .. import conv

from numpy.testing import assert_array_equal, assert_almost_equal

def test_conv_target_non_target():
  task_fname = os.path.join(os.path.dirname(__file__), "test_data", "test_cond003.txt")
  error_fname = os.path.join(os.path.dirname(__file__), "test_data", "test_cond007.txt")
  actual_target_convolved, actual_nontarget_convolved, actual_error_convolved = conv.conv_target_non_target(10, task_fname, error_fname, 1, tr_divs = 10)
  expected_target_convolved = np.array([0., 0.00106485, 0.01253479, 0.03499249, 0.05405446, 0.05994645, 0.05305345, 0.03887074, 0.02304214, 0.00929849])
  expected_nontarget_convolved = np.array([ 0., 0.00069492, 0.01071944, 0.03264745, 0.05266825, 0.06, 0.05417416, 0.04044389, 0.02457532, 0.01051738])
  expected_error_convolved = np.array([0.] * 10)
  assert_almost_equal(actual_error_convolved, expected_error_convolved)
  assert_almost_equal(actual_target_convolved, expected_target_convolved)
  assert_almost_equal(actual_nontarget_convolved, expected_nontarget_convolved)
