import project_config
from __future__ import division
from scipy import stats
from general_utils import prepare_img_single, prepare_mask
from os.path import join
from pca_utils import first_pcs_removed
import numpy as np
import math
import nibabel as nib
import numpy.linalg as npl
import roi_extraction
import itertools


file_name_con = "/Volumes/G-DRIVE mobile USB/fmri_con/sub011_task001_run001_func_data_mni.nii.gz"
file_name_scz = "/Volumes/G-DRIVE mobile USB/fmri_scz/sub001_task001_run001_func_data_mni.nii.gz"
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

	timecourse1 = [data[roi1[i]] for i in range(0,len(roi1))]
	avg_time1 = np.mean(timecourse1,axis=0)
	timecourse2 = [data[roi2[j]] for j in range(0,len(roi2))]
	avg_time2 = np.mean(timecourse2,axis=0)
	cor = np.corrcoef(avg_time1,avg_time2)[1,0]
	if cor >= 1:
	 	cor=0.99999
	z = 1/2*(math.log((1+cor)/(1-cor)))
	return z

def network_cor(data, net1, net2, is_same):
	"""
	#Input:
		#net1 and net2 are two dictionaries of ROI names to voxels belonging to that ROI
	#Output: 
		a list of z values
	"""

	roi_names_1 = net1.keys()
	roi_names_2 = net2.keys()

	if is_same:
		z_values_list = []
		for i in range(0,len(roi_names_1)):
			for j in range(i + 1,len(roi_names_2)):
				roi_name_1 = roi_names_1[i]
				roi_name_2 = roi_names_2[j]
				val = roi_cor(data,net1[roi_name_1],net2[roi_name_2])
				z_values_list.append(val)

		return z_values_list

	else:
		return [roi_cor(data,voxels_1, voxels_2) for roi_name_1, voxels_1 in net1.items() for roi_name_2, voxels_2 in net2.items()]

def z_within (data,dic):
	"""
	#Input: 
		#triple nesting lists
		#image data
	#Output:
		# a list of tuples(average z-values); within nework
	"""
	return {network_name: network_cor(data,rois,rois, True) for network_name, rois in dic.items()}


def z_bewteen (data,dic):
	"""
	#Input: 
		#triple nesting lists
		#image data
	#Output:
		#a list of tuples(CIs); between network
	"""

	z_bet = {}
	networks = dic.keys()
	for i in range(0,len(networks)):
		for j in range(i+1,len(networks)):
			network_name_1 = networks[i]
			network_name_2 = networks[j]
			z_bet[network_name_1+"-"+network_name_2] = network_cor(data,dic[network_name_1],dic[network_name_2], False)
	return z_bet

def expand_dic(dic, mm_to_vox, roi_extractor):
	expanded_dic = {}
	for i in dic.keys():
		expanded_dic[i] = {}
		for roi_name in dic[i].keys():
			expanded_dic[i][roi_name] = roi_extractor.get_voxels(mm_to_vox, dic[i][roi_name])
	return expanded_dic

def preprocessing_pipeline(subject_num, task_num, standard_source_prefix):

  img = prepare_img_single(subject_num, task_num, True, standard_source_prefix)
  data_4d = img.get_data()[...,5:]

  in_brain_mask, in_brain_vols = prepare_mask(data_4d, CUTOFF)

  residuals = first_pcs_removed(in_brain_vols, 2)

  b_vols = np.zeros(data_4d.shape)
  b_vols[in_brain_mask] = residuals

  return b_vols, img, in_brain_mask

def subject_z_values(img, data, dist_from_center, dic, in_brain_mask):
	mm_to_vox = npl.inv(img.affine)

	roi_extractor = roi_extraction.SphereExtractor(in_brain_mask, dist_from_center)

	expanded_dic = expand_dic(dic, mm_to_vox, roi_extractor)

	mean_z_values = z_within(data, expanded_dic)
	mean_z_values.update(z_bewteen(data, expanded_dic))
	return mean_z_values

def group_z_values(standard_group_source_prefix, dist_from_center, dic, grouping = None):
	task_nums = ("001", "002", "003")
  
	# level 1: task; level 2: group name; level 3: network name; level 3: a list of mean z-values
	z_values_store = {"001":{"con":{}, "scz":{}},
										"002":{"con":{}, "scz":{}},
										"003":{"con":{}, "scz":{}}}

	group_info = grouping if grouping else project_config.group
  
	for group, subject_nums in group_info.items():
		for sn in subject_nums:
			for tn in task_nums:
				data, img, in_brain_mask = preprocessing_pipeline(sn, tn, join(standard_group_source_prefix, group))
				mean_z_values_per_net_pair = subject_z_values(img, data, dist_from_center, dic, in_brain_mask)
				for network_pair_name, z_value in mean_z_values_per_net_pair.items():
					if network_pair_name not in z_values_store[tn]:
						group_name = "con" if group in ("fmri_con", "fmri_con_sib", "fmri_scz_sib") else "scz"
						z_values_store[tn][group_name][network_pair_name] = [z_value]
					else:
						z_values_store[tn][group_name][network_pair_name].append(z_value)
	return z_values_store

dic = roi_extraction.dic
dist_from_center = 4
CUTOFF = project_config.MNI_CUTOFF

mm_to_vox_con = npl.inv(img_con.affine)
mm_to_vox_scz = npl.inv(img_scz.affine)

in_brain_mask_con = np.mean(data_con, axis=-1) > CUTOFF
in_brain_mask_scz = np.mean(data_scz, axis=-1) > CUTOFF

min_roi_roi_dist = roi_extraction.min_roi_roi_distance(dic)
min_roi_roi_dist is 16.49 mm. The choice of ROI diameter in the reference paper is 15mm. This
shows the paper probably chose the ROI diameter based on the min pairwise roi distance to
avoid overlap.

roi_extractor_con = roi_extraction.SphereExtractor(in_brain_mask_con, dist_from_center)
roi_extractor_scz = roi_extraction.SphereExtractor(in_brain_mask_scz, dist_from_center)

expanded_dic_con = expand_dic(dic, mm_to_vox_con, roi_extractor_con)
expanded_dic_scz = expand_dic(dic, mm_to_vox_scz, roi_extractor_scz)

z_values_per_network_con = z_within(data_con, expanded_dic_con)

z_values_per_network_scz = z_within(data_scz, expanded_dic_scz)

z_values_bnet_con = z_bewteen(data_con, expanded_dic_con)
z_values_bnet_scz = z_bewteen(data_scz, expanded_dic_scz)

# z_values result:

# 		wDMN  	  wFP 	  wCER 		wCO
# SCZ     0.3772   0.4749  0.8110    0.5984
# CON     0.6591   0.5506  0.5294    0.6857

# 		bDMN-FP    bDMN-CER   bDMN-CO   bFP-CER   bFP-CO   bCER-CO
# CON 	0.4966	   0.3411     0.3652     0.3778    0.4737   0.3187
# SCZ		0.3461     0.4329     0.2381     0.4344    0.3586   0.3219  

# In the paper, it is said the connectivity of bFP-CER and bCER-CO are reduced for SCZ patients.

standard_group_source_prefix = "/Volumes/G-DRIVE mobile USB/"

small_group_info = {"fmri_con":("011", "012", "015", "020"),
          "fmri_con_sib":("010", "013", "014", "016"),
          "fmri_scz":("007", "009", "017", "027"),
          "fmri_scz_sib":("006", "008", "018", "019")}

z_values_store = group_z_values(standard_group_source_prefix, dist_from_center, dic, grouping=small_group_info)
