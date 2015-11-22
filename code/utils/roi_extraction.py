import numpy as np
import numpy.linalg as npl
import nibabel as nib
import itertools as itt
import matplotlib.pyplot as plt

def co2vox(coordinate,mm_to_vox):
	#I find this will give me some decimal number, which is unreasonable
	#indices
	#return: standard brain ROI center
	ind = nib.affines.apply_affine(mm_to_vox, coordinate)
	return ([int(x) for x in ind])

def ROI_region(fmri):
	# fmri: standard brain ROI center
	x = range(max(fmri[0]-4,0),min(fmri[0]+4,91))
	y = range(max(fmri[1]-4,0),min(fmri[1]+4,109))
	z = range(max(fmri[2]-4,0),min(fmri[2]+4,91))
	a = [x,y,z]
	roi = list(itt.product(*a))
	return roi

'''
Input: fmri data index of the center of RIO region
return: corresponding frm indices in that region
'''
def filter_ROI(vox_indc, in_brain_mask):
	return [v for v in vox_indc if in_brain_mask[v]]
	# tmp = np.array([in_brain_mask[ind] for ind in vox_indc])
	# return(np.array(vox_indc)[tmp])

dic = {}
with open ("/Users/Xinyue_star/Desktop/Final_Proj/project-gamma/code/tmp_xinyue/net_roi.txt") as f:
	for lines in f:
		(key_region, k_roi, val1, val2, val3)= lines.split()
		loc = [int(val1),int(val2),int(val3)]
		if key_region not in dic:
			dic[key_region] = {}
		dic[key_region][k_roi] = loc

in_brain_mask = np.mean(fmri_data, axis=-1) > 5000

mm_to_vox = npl.inv(img.affine)

coor = dic['Default']['LIP']
b = ROI_region(co2vox(coor,mm_to_vox))
a = filter_ROI(b, in_brain_mask)













	
