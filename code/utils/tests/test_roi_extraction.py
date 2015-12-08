"""
Test roi_extraction module

Run with::

    nosetests test_roi_extraction.py
"""
import numpy as np
import nibabel as nib
import numpy.linalg as npl
import math
from .. import roi_extraction

from numpy.testing import assert_array_equal, assert_almost_equal


def test_sphere_extractor():
    in_brain_mask = np.zeros((91,109,91), dtype=bool)
    in_brain_mask[1:,1:,1:] = True
    affine_matrix = [[  -2.,    0.,    0.,   90.],
                     [   0.,    2.,    0., -126.],
                     [   0.,    0.,    2.,  -72.],
                     [   0.,    0.,    0.,    1.]]
    mm_to_vox = npl.inv(affine_matrix)
    # test the index (1, 1, 1)
    coor_mm = nib.affines.apply_affine(affine_matrix, [1, 1, 1])
    se = roi_extraction.SphereExtractor(in_brain_mask, 1)
    expected = np.array(((1, 1, 1), (1, 1, 2), (1, 2, 1), (2, 1, 1)))
    actual = se.get_voxels(mm_to_vox, coor_mm)

    if actual is None:
        raise RuntimeError("function returned None")
    assert_array_equal(actual, expected)

def test_min_roi_roi_distance():
    test_dic =  {
                    'Cerebellar': {'LIC': [0, 0, 0]},
                    'Cingulo-Opercular': {'LaPFC': [5, 5, 5]},
                    'Default': {'CT': [4, 4, 4], 'LIP': [2, 2, 2]}
                }
    expected = math.sqrt(3)
    actual = roi_extraction.min_roi_roi_distance(test_dic)
    if actual is None:
        raise RuntimeError("function returned None")
    assert_almost_equal(actual, expected)