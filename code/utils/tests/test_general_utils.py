"""
Test general_utils module

Run with::

    nosetests test_general_utils.py
"""
import numpy as np
import nibabel as nib
import os
import numpy.linalg as npl
import math
from .. import general_utils

from numpy.testing import assert_almost_equal, assert_equal

def test_vol_index_iter():
  actual = list(general_utils.vol_index_iter([1,1,1]))
  expected = [(0,0,0)]
  assert_almost_equal(actual, expected)

def test_plane_index_iter():
  actual = list(general_utils.plane_index_iter([2,2]))
  expected = [(0, 0), (0, 1), (1, 0), (1, 1)]
  assert_almost_equal(actual, expected)  

def test_data_fetching():
  expected = nib.Nifti1Image(np.ones((2,2,2,6)),np.eye(4))
  filename = 'sub001_task001_run001_func_data_mni.nii.gz'
  nib.save(expected, os.path.join(os.path.dirname(__file__), 'test_data', filename))
  source_prefix = os.path.join(os.path.dirname(__file__), 'test_data')
  actual = general_utils.prepare_standard_img('001', '001', source_prefix)
  assert_almost_equal(actual.get_data(), expected.get_data())

  actual = general_utils.prepare_standard_data('001', '001', source_prefix)
  assert_almost_equal(actual, expected.get_data()[...,5:])  

  os.remove(os.path.join(source_prefix, filename))

def test_form_cond_filepath():
  expected = os.path.join(os.path.dirname(__file__), "test_data", "sub001", "model", "model001", "onsets", "task001_run001", "cond001.txt")
  cond_filepath_prefix = os.path.join(os.path.dirname(__file__), 'test_data')
  actual = general_utils.form_cond_filepath("001", "001", "001", cond_filepath_prefix)
  assert_equal(actual, expected)

def test_prepare_mask():
  data_4d = np.zeros([2,2,2,1])
  data_4d[1,1,1] = 10
  actual_mask, actual_in_brain_vols = general_utils.prepare_mask(data_4d, 3)
  expected_mask = np.zeros([2,2,2], dtype=bool)
  expected_mask[1,1,1] = True
  expected_in_brain_vols = np.array([[10.0]])
  assert_almost_equal(actual_mask, expected_mask)
  assert_almost_equal(actual_in_brain_vols, expected_in_brain_vols)
