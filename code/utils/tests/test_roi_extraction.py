"""
Test roi_extraction module

Run with::

    nosetests test_roi_extraction.py
"""
import numpy as np
import nibabel as nib
import numpy.linalg as npl
import math
import itertools as itt
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


def test_co2vox():
    coordinate = np.array([0.0,0,0])
    affine_matrix = [[  -2.,    0.,    0.,   90.],
                     [   0.,    2.,    0., -126.],
                     [   0.,    0.,    2.,  -72.],
                     [   0.,    0.,    0.,    1.]]
    mm_to_vox = npl.inv(affine_matrix)
    vox_to_mm = affine_matrix
    new  = roi_extraction.co2vox( coordinate,mm_to_vox)
    actual = nib.affines.apply_affine(vox_to_mm, new)
    if actual is None:
        raise RuntimeError("function returned None")
    assert_array_equal(coordinate, actual)

def test_ROI_region():
    x_range = range(41,49)
    y_range = range(51,59)
    z_range  = range(41,49)
    center = [(41+49)/2,(51+59)/2,(41+49)/2]
    tmp = [x_range,y_range,z_range]
    actual = list(itt.product(*tmp))
    expected = roi_extraction.ROI_region(center)
    if actual is None:
        raise RuntimeError("function returned None")
    assert_array_equal(actual, expected)

def test_filter_ROI():
    x_range = range(41,49)
    y_range = range(51,59)
    z_range  = range(41,49)
    tmp = [x_range,y_range,z_range]
    vox_indc = list(itt.product(*tmp))
    in_brain_mask = np.zeros((91,109,91), dtype=bool) 
    in_brain_mask[45:91,55:109,45:91] = True #half of the brain are true
    actual = roi_extraction.filter_ROI(vox_indc, in_brain_mask)
    expected = list(itt.product(*[range(45,49),range(55,59),range(45,49)]))
    if actual is None:
        raise RuntimeError("function returned None")
    assert_array_equal(actual, expected)

def test_get_voxel():
    coor = np.array([0.0,0,0])
    affine_matrix = [[  -2.,    0.,    0.,   90.],
                     [   0.,    2.,    0., -126.],
                     [   0.,    0.,    2.,  -72.],
                     [   0.,    0.,    0.,    1.]]
    mm_to_vox = npl.inv(affine_matrix)
    in_brain_mask = np.zeros((91,109,91), dtype=bool) 
    in_brain_mask[45:91,63:109,36:91] = True #half of the brain are true
    actual = roi_extraction.get_voxels(mm_to_vox, coor, in_brain_mask)
    x_range = range(45,49)
    y_range = range(63,67)
    z_range  = range(36,40)
    tmp = [x_range,y_range,z_range]
    expected = list(itt.product(*tmp))
    #a = roi_extraction.co2vox( coordinate,mm_to_vox), the index is (45,63,36)
    if actual is None:
        raise RuntimeError("function returned None")
    assert_array_equal(actual, expected)













