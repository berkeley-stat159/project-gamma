"""
Test connectivity_utils module

Run with::

    nosetests connectivity_utils.py
"""
import numpy as np
import sys
import random
import os
import pandas as pd
from .. import connectivity_utils

from numpy.testing import assert_array_equal, assert_almost_equal

def test_c_within_and_c_between():

  # mocking the correlation values store
  test_c_values_store = {"test_network_1":{"test_roi_1":((0,0,0),(0,0,1)), "test_roi_2":((0,1,0),(0,1,1))},
                    "test_network_2":{"test_roi_3":((1,0,0),(1,0,1)), "test_roi_4":((1,1,0),(1,1,1))}}


  data = np.zeros((2,2,2,3))
  data[0,0,0] = [1,2,3]
  data[0,0,1] = [1,2,3]
  data[0,1,0] = [-1,-2,-3]
  data[0,1,1] = [-1,-2,-3]
  data[1,0,0] = [5,4,37]
  data[1,0,1] = [5,4,37]
  data[1,1,0] = [-3,-244,-1]
  data[1,1,1] = [-3,-244,-1]


  actual = connectivity_utils.c_within(data, test_c_values_store)

  # expected values are explicitly calculated according to the rules explained in the paper
  expected = {'test_network_1':(np.corrcoef([1,2,3],[-1,-2,-3])[1,0],), 'test_network_2': (np.corrcoef([5,4,37],[-3,-244,-1])[1,0],)}

  assert_almost_equal(expected['test_network_1'], expected['test_network_1'])
  assert_almost_equal(expected['test_network_2'], expected['test_network_2'])

  actual = connectivity_utils.c_between(data, test_c_values_store)

  # expected values are explicitly calculated according to the rules explained in the paper
  expected = [np.corrcoef([1,2,3],[5,4,37])[1,0], np.corrcoef([1,2,3],[-3,-244,-1])[1,0],np.corrcoef([-1,-2,-3],[5,4,37])[1,0], np.corrcoef([-1,-2,-3],[-3,-244,-1])[1,0]]

  assert_almost_equal(np.sort(expected), np.sort(actual['test_network_1-test_network_2']))

def test_permute():
  r1 = np.linspace(0,1,num=30).tolist()
  r2 = np.linspace(0,1,num=20).tolist()
  
  random.seed(0)
  actual = connectivity_utils.permute(r1,r2)

  # this is to specifically deal with python 3 & 2 compatibility because
  # random.seed implements different seeding algorithm. A potential
  # workaround is to subclass and implement our own random module, but
  # this is not done for the project.
  if sys.version_info[0] < 3:
    expected = 0.5103999999999
  else:
    expected = 0.49590
  assert_almost_equal(actual,expected)

def test_pandas():
  permute_results = {"bDMN-CER": 0, "bCO-CER": 0, "bDMN-CO": 0, "bFP-CER": 0, "bDMN-FP": 0, "bFP-CO": 0}
  permute_pd = pd.DataFrame(permute_results, index=["Permution Test P Values"])
  assert_almost_equal(permute_pd, np.array([[0,0,0,0,0,0]]))
