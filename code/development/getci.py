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
#input: 
	# roi1 and roi2 are two list of tuples indicating the voxel 
	# indexes of the ROI1 and ROI2 respectively
	# data
#output: 
	# returns the mean Fisher's z value of all the correlations among voxels in ROI1 and ROI2

	cor_z = np.zeros((len(roi1),len(roi2)))

	store = np.zeros(cor_z.shape) - float('inf')

	for i in range(0,len(roi1)):
		for j in range(0,len(roi2)):

			if 0 <= j and j < len(roi1) and 0 <= i and i < len(roi2) and store[j, i] !=  -float('inf'):
				cor_z[i, j] = store[j, i]
				continue

			data1 = data[roi1[i]]
			data2 = data[roi2[j]]
			cor=np.corrcoef(data1,data2)[1,0]
			if cor >= 1:
				cor=0.99999
			cor_z[i,j] = 1/2*(math.log((1+cor)/(1-cor)))  # Q: how to deal with cor=1 

			store[i, j] = cor_z[i, j]
			if 0 <= j and j < len(roi1) and 0 <= i and i < len(roi2):
				store[j, i] = cor_z[i, j]

	return np.mean(cor_z)

def network_cor(data,net1,net2):
#Input:
	#net1 and net2 are two lists of lists: (1) list of ROIs (2)list of tuples of one ROI
#Output: 
	#95% Confidence Interval of the z-values between networks, a tuple 
	z_values = np.zeros((len(net1),len(net2)))

	store = np.zeros(z_values.shape) - float('inf')

	for i in range(0,len(net1)):
		for j in range(0,len(net2)):

			if 0 <= j and j < len(net1) and 0 <= i and i < len(net2) and store[j, i] !=  -float('inf'):
				z_values[i, j] = store[j, i]
				continue

			z_values[i,j] = roi_cor(data,net1[i],net2[j])

			store[i, j] = z_values[i, j]
			if 0 <= j and j < len(net1) and 0 <= i and i < len(net2):
				store[j, i] = z_values[i, j]

			print "found roi " + str((i, j)) + ". its value is " + str(z_values[i, j])

	# CI = stats.norm.interval(0.95, loc=np.mean(z_values), scale=np.std(z_values))
	return z_values


def ci_within (data,dics):
#Input: 
	#triple nesting lists
	#image data
#Output:
	# a list of tuples(CIs); within nework
	"""
	ci_wit = []
	for net in dics:
		ci_wit.append(network_cor(data,net,net))
	return ci_wit #CI for ("wDMN","wFP","wCER","wCO")
	"""
	return [network_cor(data,rois,rois) for rois in dics]


def ci_bewteen (data,dics):
#Input: 
	#triple nesting lists
	#image data
#Output:
	#a list of tuples(CIs); between network

	#TODO

	ci_bet = []
	for i in range(0,len(dics)):
		for j in range(0,len(dics)):
			ci_bet.append(network_cor(data,dics[i],dics[j]))
	return ci_bet #CI for ("bDMN-FP","bDMN-CER","bDMN-CO","bFP-CER","bFP-CO","bCER-CO")


def dictolist (dic, mm_to_vox, in_brain_mask):
	networks=dic.keys() #['Default', 'Fronto-Parietal', 'Cerebellar', 'Cingulo-Opercular']
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

trilist_con = dictolist(dic, mm_to_vox_con, in_brain_mask_con)
z_values_per_network_con = ci_within(data_con,trilist_con)

trilist_scz = dictolist(dic, mm_to_vox_scz, in_brain_mask_scz)
z_values_per_network_scz = ci_within(data_scz,trilist_scz)



#ci_between(data,trilist)