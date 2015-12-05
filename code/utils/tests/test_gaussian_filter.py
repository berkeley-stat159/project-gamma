"""
Test gaussian_filter module

Run with::

    nosetests test_gaussian_filter.py
"""
import numpy as np
import nibabel as nib
import numpy.linalg as npl
import math
from .. import gaussian_filter

from numpy.testing import assert_array_equal, assert_almost_equal


def test_pad_boundary_per_image():
    
    data = np.zeros((3,3,3))
    data[1,1,1] = 1
    brain_mask = np.zeros(data.shape, dtype=bool)
    brain_mask[1,1,1] = True
    pad_thickness = 2

    gaussian_filter.pad_boundary_per_image(data, brain_mask, pad_thickness)
    actual = data
    expected = np.ones(data.shape)

    if actual is None:
        raise RuntimeError("function returned None")
    assert_array_equal(actual, expected)

def test_spatial_smooth():

    data_4d = np.zeros((3,3,3,2))
    data_4d[1,1,1,0] = 1
    data_4d[1,1,1,1] = 1
    brain_mask = np.zeros(data_4d.shape[0:-1], dtype=bool)
    brain_mask[1,1,1] = True
    actual = gaussian_filter.spatial_smooth(data_4d, brain_mask, 2, 2, True)
    expected = np.array(
        [[[[ 0.03702152,  0.03702152],
         [ 0.03703703,  0.03703703],
         [ 0.03702152,  0.03702152]],

        [[ 0.03703703,  0.03703703],
         [ 0.03705256,  0.03705256],
         [ 0.03703703,  0.03703703]],

        [[ 0.03702152,  0.03702152],
         [ 0.03703703,  0.03703703],
         [ 0.03702152,  0.03702152]]],

       [[[ 0.03703703,  0.03703703],
         [ 0.03705256,  0.03705256],
         [ 0.03703703,  0.03703703]],

        [[ 0.03705256,  0.03705256],
         [ 0.03706808,  0.03706808],
         [ 0.03705256,  0.03705256]],

        [[ 0.03703703,  0.03703703],
         [ 0.03705256,  0.03705256],
         [ 0.03703703,  0.03703703]]],


       [[[ 0.03702152,  0.03702152],
         [ 0.03703703,  0.03703703],
         [ 0.03702152,  0.03702152]],

        [[ 0.03703703,  0.03703703],
         [ 0.03705256,  0.03705256],
         [ 0.03703703,  0.03703703]],

        [[ 0.03702152,  0.03702152],
         [ 0.03703703,  0.03703703],
         [ 0.03702152,  0.03702152]]]])
    assert_almost_equal(actual, expected)