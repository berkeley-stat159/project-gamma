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
  actual_target_convolved, actual_nontarget_convolved, actual_error_convolved = conv.conv_target_non_target(10, task_fname, error_fname, 2.5, tr_divs = 10)
  expected_target_convolved = np.array([0., 0.00106485, 0.01253479, 0.03499249, 0.05405446, 0.05994645, 0.05305345, 0.03887074, 0.02304214, 0.00929849])
  expected_nontarget_convolved = np.array([ 0., 0.00069492, 0.01071944, 0.03264745, 0.05266825, 0.06, 0.05417416, 0.04044389, 0.02457532, 0.01051738])
  expected_error_convolved = np.array([0.] * 10)
  assert_almost_equal(actual_error_convolved, expected_error_convolved)
  assert_almost_equal(actual_target_convolved, expected_target_convolved)
  assert_almost_equal(actual_nontarget_convolved, expected_nontarget_convolved)

def test_conv_std():
  task_fname = os.path.join(os.path.dirname(__file__), "test_data", "test_cond003.txt")
  actual_std = conv.conv_std(10, task_fname, 1)
  expected_std = np.array([ 0., -0.00030452, -0.00358456, -0.01000677, -0.01545791,-0.01714284, -0.01517165, -0.01111583, -0.00658934, -0.00265908])
  assert_almost_equal(actual_std, expected_std )
  

def test_conv_main():
  task_fname = os.path.join(os.path.dirname(__file__), "test_data", "test_cond003.txt")
  actual_main = conv.conv_main(10, task_fname, 1)
  expected_main = np.array([  3.46786253e-05,3.90603366e-03, 1.65702768e-02,2.96511947e-02, 3.50123290e-02, 3.24253327e-02, 2.45289911e-02, 1.51282388e-02, 6.69815333e-03, 4.15265073e-04])
  assert_almost_equal(actual_main, expected_main )
  
