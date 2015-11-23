from __future__ import division
import numpy as np
import math
from scipy import stats
import nibabel as nib
import numpy.linalg as npl
import roi_extraction

file_name_con = "sub011_task001_run001_func_data_mni.nii.gz"
file_name_scz = "sub001_task001_run001_func_data_mni.nii.gz"
img_con = nib.load(file_name_con)
img_scz = nib.load(file_name_scz)
data_con = img_con.get_data()[..., 5:]
data_scz = img_scz.get_data()[..., 5:]

def roi_cor (data, roi1,roi2):
	"""
	#input: 
		# roi1 and roi2 are two list of tuples indicating the voxel 
		# only necessary to call this method if roi1 != roi2
		# indexes of the ROI1 and ROI2 respectively
		# data
	#output: 
		# returns the mean Fisher's z value of all the correlations among voxels in ROI1 and ROI2
	"""

	cor_z = np.zeros((len(roi1),len(roi2)))

	for i in range(0,len(roi1)):
		for j in range(0,len(roi2)):

			data1 = data[roi1[i]]
			data2 = data[roi2[j]]
			cor=np.corrcoef(data1,data2)[1,0]
			if cor >= 1:
				cor=0.99999
			cor_z[i,j] = 1/2*(math.log((1+cor)/(1-cor)))  # Q: how to deal with cor=1 

	return np.mean(cor_z)

def network_cor(data,net1,net2, is_same):
	"""
	#Input:
		#net1 and net2 are two lists of lists: (1) list of ROIs (2)list of tuples of one ROI
	#Output: 
		#95 percent Confidence Interval of the z-values between networks, a tuple 
	"""

	if is_same:
		z_values_list = []
		for i in range(0,len(net1)):
			for j in range(i + 1,len(net2)):
				val = roi_cor(data,net1[i],net2[j])
				z_values_list.append(val)

				print "found roi " + str((i, j)) + ". its value is " + str(val)

		return z_values_list

	else:
		z_values = np.zeros((len(net1),len(net2)))

		for i in range(0,len(net1)):
			for j in range(0,len(net2)):

				z_values[i,j] = roi_cor(data,net1[i],net2[j])

				print "found roi " + str((i, j)) + ". its value is " + str(z_values[i, j])

		return z_values.ravel()


def ci_within (data,dics):
	"""
	#Input: 
		#triple nesting lists
		#image data
	#Output:
		# a list of tuples(CIs); within nework
	"""
	return [network_cor(data,rois,rois, True) for rois in dics]


def ci_bewteen (data,dics):
	"""
	#Input: 
		#triple nesting lists
		#image data
	#Output:
		#a list of tuples(CIs); between network
	"""

	#TODO

	ci_bet = []
	for i in range(0,len(dics)):
		for j in range(0,len(dics)):
			ci_bet.append(network_cor(data,dics[i],dics[j], False))
	return ci_bet #CI for ("bDMN-FP","bDMN-CER","bDMN-CO","bFP-CER","bFP-CO","bCER-CO")


def dictolist (dic, mm_to_vox, in_brain_mask):
	networks=dic.keys() #['Default', 'Fronto-Parietal', 'Cerebellar', 'Cingulo-Opercular'] with caution
	list_net=[]
	for i in networks:
		ROIs = dic[i].keys() #['LSF', 'RMPF', 'LMPF', 'RS', 'RSF', 'RIP', 'LiT', 'LIP', 'LpH', 'RpH', 'pCin', 'RiT', 'CT']
		list_roi = []
		for j in ROIs:
			list_roi.append(roi_extraction.get_voxels(mm_to_vox, dic[i][j], in_brain_mask))
		list_net.append(list_roi)
	return list_net

dic = roi_extraction.dic

mm_to_vox_con = npl.inv(img_con.affine)
mm_to_vox_scz = npl.inv(img_scz.affine)

in_brain_mask_con = np.mean(data_con, axis=-1) > 5000
in_brain_mask_scz = np.mean(data_scz, axis=-1) > 5000
#we choose 5000 values by inspecting the histogram of data values

trilist_con = dictolist(dic, mm_to_vox_con, in_brain_mask_con)
z_values_per_network_con = ci_within(data_con,trilist_con)

trilist_scz = dictolist(dic, mm_to_vox_scz, in_brain_mask_scz)
z_values_per_network_scz = ci_within(data_scz,trilist_scz)