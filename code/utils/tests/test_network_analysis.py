"""
Test network_analysis module

Run with::

    nosetests test_network_analysis.py
"""
import numpy as np
import random
from ... import network_analysis
from numpy.testing import assert_array_equal, assert_almost_equal

def test_permute():
	r1 = np.linspace(0,1,num=30).tolist()
	r2 = np.linspace(0,1,num=20).tolist()
	random.seed(0)
	actual = network_analysis.permute(r1,r2)
	expected = 0.496
	assert_almost_equal(actual,expected)
