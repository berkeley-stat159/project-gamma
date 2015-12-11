"""
Test multiple_comparison module

Run with::
	nosetests test_multiple_comparison.py
"""

import numpy as np
from .. import multiple_comparison
from numpy.testing import assert_array_equal, assert_almost_equal

def test_multiple_comp():
	res = np.linspace(0,1,100)
	res.shape = (10,10)
	actual = multiple_comparison.multiple_comp(res)
	expected = [0, 0, 0, 0]
	assert_array_equal(actual, expected)