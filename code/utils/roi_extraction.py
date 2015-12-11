"""
Helpers for extracting voxel time courses based on the
spherical shape assumption of a ROI.
"""

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import project_config
import numpy as np
import numpy.linalg as npl
import nibabel as nib
import itertools as itt
import matplotlib.pyplot as plt
import os
from scipy.spatial.distance import pdist
from general_utils import vol_index_iter
from scipy.spatial import cKDTree

def co2vox(coordinate,mm_to_vox):
	"""
	Return the indices of MNI brain given coordinate of ROI center
	
	Parameters:
	---------
	Input
	coordinate: center coordinate of ROI
	mm_to_vox: Map from coordinate to MNI brain indices

	Return
	MNI brain indices
	"""
	ind = nib.affines.apply_affine(mm_to_vox, coordinate)
	return [int(x) for x in ind]

def ROI_region(fmri):
	"""
	Get all the index within one ROI region, given the center index of it.
	
	Parameters:
	---------
	Input
	fmri: standard brain ROI center

	Return
	List of tuples, which represent indices of voxel within given ROI.
	"""
	x = range(max(fmri[0]-4,0),min(fmri[0]+4,91))
	y = range(max(fmri[1]-4,0),min(fmri[1]+4,109))
	z = range(max(fmri[2]-4,0),min(fmri[2]+4,91))
	a = [x,y,z]
	roi = list(itt.product(*a))
	return roi

def filter_ROI(vox_indc, in_brain_mask):
	"""
	Filter the voxels in the ROI so that promise remaining voxels within the brain.
	
	Parameters:
	---------
	Input
	vox_indc: list of tuples representing the voxels within the ROI.
	in_brain_mask: a list of True and False. True represent valid voxels with in the brain.

	Return
	List of tuples, which represent indices of filtered voxel within given ROI.
	"""
	return [v for v in vox_indc if in_brain_mask[v]]

def min_roi_roi_distance(network_map):
	"""
	Compute shortest pairwise euclidean distance of all ROI centers in all networks.
	The purpose of this is to check whether the choice of diameter for a ROI sphere
	will cause overlaps of voxels.
	"""
	centers = [center for v in network_map.values() for center in v.values()]
	return min(pdist(centers, 'euclidean'))

def get_voxels(mm_to_vox, coor, in_brain_mask):
	"""
	Get voxels of a given center coordinate of ROI.
	
	Parameters:
	---------
	Input
	mm_to_vox: Map from coordinate to MNI brain indices
	coor: center coordinate of ROI
	in_brain_mask: a list of True and False. True represent valid voxels with in

	Return
	List of tuples, which represent indices of filtered voxel within given ROI.
	"""
	b = ROI_region(co2vox(coor,mm_to_vox))
	return filter_ROI(b, in_brain_mask)	

class SphereExtractor(object):
	def __init__(self, in_brain_mask, dist_from_center):
		points = [i for i in vol_index_iter(in_brain_mask.shape) if in_brain_mask[i]]
		self.tree = cKDTree(np.array(points))
		self.points = points
		self.dist_from_center = dist_from_center

	def get_voxels(self, mm_to_vox, coor):
		"""
		Get voxels that are within a distance from a given center coordinate of ROI.
		
		Parameters:
		---------
		Input
		mm_to_vox: Map from coordinate to MNI brain indices
		coor: center coordinate of ROI in mm
		in_brain_mask: a list of True and False. True represent valid voxels with in

		Return
		List of tuples, which represent indices of filtered voxel within given ROI.
		"""
		center = co2vox(coor, mm_to_vox)
		return [self.points[i] for i in self.tree.query_ball_point(center, self.dist_from_center)]
	
dic = {}

net_roi_filename = os.path.join(os.path.dirname(__file__), '../../data/net_roi.txt')
with open (net_roi_filename) as f:
	for lines in f:
		(key_region, k_roi, val1, val2, val3)= lines.split()
		loc = [int(val1),int(val2),int(val3)]
		if key_region not in dic:
			dic[key_region] = {}
		dic[key_region][k_roi] = loc














	
