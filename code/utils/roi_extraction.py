import numpy as np
import numpy.linalg as npl
import nibabel as nib
import itertools as itt
import matplotlib.pyplot as plt

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

dic = {}
with open ("/Users/Lynn/Desktop/STAT259/project/project_dev/net_roi.txt") as f:
	for lines in f:
		(key_region, k_roi, val1, val2, val3)= lines.split()
		loc = [int(val1),int(val2),int(val3)]
		if key_region not in dic:
			dic[key_region] = {}
		dic[key_region][k_roi] = loc

def get_voxels(mm_to_vox, coor, in_brain_mask):
	b = ROI_region(co2vox(coor,mm_to_vox))
	return filter_ROI(b, in_brain_mask)

	













	
