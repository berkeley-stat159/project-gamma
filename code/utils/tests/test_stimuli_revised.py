"""
Test stimuli_revised module

Run with::

    nosetests test_stimuli_revised.py
"""
import numpy as np
import nibabel as nib
import numpy.linalg as npl
import math
import os
from .. import stimuli_revised
from .. import general_utils

from numpy.testing import assert_array_equal, assert_almost_equal

def test_events2neural_target_non_target():
  task_fname = os.path.join(os.path.dirname(__file__), "test_data", "test_cond003.txt")
  error_fname = os.path.join(os.path.dirname(__file__), "test_data", "test_cond007.txt")
  actual_target_neural, actual_nontarget_neural, actual_error_neural = stimuli_revised.events2neural_target_non_target(task_fname, error_fname, 1, 10, TR=1)
  expected_target_neural = np.array([1., 1., 0., 0., 0., 0., 0., 0., 0., 0.])
  expected_nontarget_neural = np.array([ 0., 0.,  0.,  1.,  1., 0., 0., 0., 0., 0.])
  expected_error_neural = np.array([0.] * 10)
  assert_almost_equal(actual_error_neural, expected_error_neural)
  assert_almost_equal(actual_target_neural, expected_target_neural)
  assert_almost_equal(actual_nontarget_neural, expected_nontarget_neural)


  empty_fname = os.path.join(os.path.dirname(__file__), "test_data", "test_cond007.txt")
  error_fname = os.path.join(os.path.dirname(__file__), "test_data", "test_cond007.txt")
  try:
      stimuli_revised.events2neural_target_non_target(empty_fname, error_fname, 1, 10, TR=1)
  except ValueError:
      pass
  except e:
    raise AssertionError("Test test_events2neural_target_non_target failed. %s"%e)
  else:
    raise AssertionError("Expected exception to be thrown. However, exception is not thrown.")

def test_events2neural():
  empty_fname = os.path.join(os.path.dirname(__file__), "test_data", "test_cond007.txt")
  try:
      stimuli_revised.events2neural(empty_fname, 0.01, 10)
  except ValueError:
      pass
  except e:
    raise AssertionError("Test test_events2neural_target_non_target failed. %s"%e)
  else:
    raise AssertionError("Expected exception to be thrown. However, exception is not thrown.")

def test_events2neural_rounded():
  empty_fname = os.path.join(os.path.dirname(__file__), "test_data", "test_cond007.txt")
  try:
      stimuli_revised.events2neural_rounded(empty_fname, 0.01, 10)
  except ValueError:
      pass
  except e:
    raise AssertionError("Test test_events2neural_target_non_target failed. %s"%e)
  else:
    raise AssertionError("Expected exception to be thrown. However, exception is not thrown.")
