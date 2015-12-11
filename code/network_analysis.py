"""
Script for inter-netowrk and intra-network connectivity analysis.
"""

from __future__ import division
import project_config
from conv import conv_target_non_target, conv_std
from stimuli_revised import events2neural_std
from gaussian_filter import spatial_smooth
from general_utils import prepare_standard_img, prepare_mask, prepare_standard_data, form_cond_filepath
from os.path import join
from connectivity_utils import c_between, c_within, permute
import numpy as np
import os
import math
import nibabel as nib
import numpy.linalg as npl
import roi_extraction
from ggplot import *
import pandas as pd
import random

import pdb

def create_f (task, dic, namelist, find_nw):
    con_group = "con"
    scz_group = 'scz'

    sub_dic_con = dic[task][con_group]
    sub_dic_scz = dic[task][scz_group]
    corrs = np.array([])
    network = np.array([])
    for name in namelist:
      corrs = np.append(corrs, np.ravel(sub_dic_con[name]))
      network =np.append(network, [find_nw[name] + ",con"]*len(np.ravel(sub_dic_con[name])))
      corrs = np.append(corrs, np.ravel(sub_dic_scz[name]))
      network =np.append(network, [find_nw[name] + ",scz"]*len(np.ravel(sub_dic_scz[name])))
    data_f = pd.DataFrame(corrs)
    data_f['networks']=network
    data_f.columns = ['corrs','networks']
    return data_f

def generate_connectivity_results(connectivity_results, output_filename):
  
  find_nw = {}
  find_nw['Default-Cerebellar']='bDMN-CER'
  find_nw['Cerebellar-Cingulo-Opercular']='bCO-CER'
  find_nw['Default-Cingulo-Opercular']='bDMN-CO'
  find_nw['Default']='wDMN'
  find_nw['Fronto-Parietal-Cerebellar']='bFP-CER'
  find_nw['Cingulo-Opercular']='wCO'
  find_nw['Default-Fronto-Parietal']='bDMN-FP'
  find_nw['Fronto-Parietal']='wFP'
  find_nw['Cerebellar']='wCER'
  find_nw['Fronto-Parietal-Cingulo-Opercular']='bFP-CO'
  
  between_namelist = ['Default-Cerebellar','Cerebellar-Cingulo-Opercular','Default-Cingulo-Opercular'
  ,'Fronto-Parietal-Cerebellar','Default-Fronto-Parietal','Fronto-Parietal-Cingulo-Opercular']

  within_namelist = ['Default','Fronto-Parietal','Cerebellar','Cingulo-Opercular']
  
  f_within = create_f ('003', connectivity_results, within_namelist, find_nw)
  
  plt1 = ggplot(f_within, aes(x='corrs', y='networks')) +\
      geom_boxplot()+\
      ggtitle("Within-Network Correlations in CON and SCZ Group")+\
      xlab("Correlation")+\
      ylab("Networks")+\
      scale_x_continuous(limits=(-1.0, 1.0))

  ggsave(plt1, os.path.join(output_filename, "within_network_connectivity_plot.png"))

  between_namelist = ['Default-Cerebellar','Cerebellar-Cingulo-Opercular','Default-Cingulo-Opercular'
  ,'Fronto-Parietal-Cerebellar','Default-Fronto-Parietal','Fronto-Parietal-Cingulo-Opercular']
  
  f_between = create_f('003', connectivity_results, between_namelist, find_nw)
  
  plt2 = ggplot(f_between, aes(x='corrs', y='networks')) +\
      geom_boxplot()+\
      ggtitle("Between-Network Correlations in CON and SCZ Group")+\
      xlab("Correlation")+\
      ylab("Networks")+\
      scale_x_continuous(limits=(-1.0, 1.0))

  ggsave(plt2, os.path.join(output_filename, "inter_network_connectivity_plot.png"))

def expand_dic(dic, mm_to_vox, roi_extractor):
	expanded_dic = {}
	for i in dic.keys():
		expanded_dic[i] = {}
		for roi_name in dic[i].keys():
			expanded_dic[i][roi_name] = roi_extractor.get_voxels(mm_to_vox, dic[i][roi_name])
	return expanded_dic

def preprocessing_pipeline(subject_num, task_num, standard_source_prefix, cond_filepath_prefix):

  img = prepare_standard_img(subject_num, task_num, standard_source_prefix)
  data = img.get_data()[..., 5:]

  n_trs = data.shape[-1] + 5

  cond_filename_003 = form_cond_filepath(subject_num, task_num, "003", cond_filepath_prefix)
  cond_filename_005 = form_cond_filepath(subject_num, task_num, "005", cond_filepath_prefix)
  cond_filename_001 = form_cond_filepath(subject_num, task_num, "001", cond_filepath_prefix)
  cond_filename_004 = form_cond_filepath(subject_num, task_num, "004", cond_filepath_prefix)
  cond_filename_007 = form_cond_filepath(subject_num, task_num, "007", cond_filepath_prefix)

  target_convolved, nontarget_convolved, error_convolved = conv_target_non_target(n_trs, cond_filename_003, cond_filename_007, TR, tr_divs = 100.0)
  target_convolved, nontarget_convolved, error_convolved = target_convolved[5:], nontarget_convolved[5:], error_convolved[5:]

  block_regressor = events2neural_std(cond_filename_005, TR, n_trs)[5:]

  block_start_cues = conv_std(n_trs, cond_filename_001, TR)[5:]
  block_end_cues = conv_std(n_trs, cond_filename_004, TR)[5:]

  linear_drift = np.linspace(-1, 1, n_trs)
  qudratic_drift = linear_drift ** 2
  qudratic_drift -= np.mean(qudratic_drift)

  linear_drift = linear_drift[5:]
  qudratic_drift = qudratic_drift[5:]

  in_brain_mask, _ = prepare_mask(data, CUTOFF)

  pad_thickness = 2.0
  sigma = 2.0

  b_vols = spatial_smooth(data, in_brain_mask, pad_thickness, sigma, False)
  in_brain_tcs = b_vols[in_brain_mask]

  Y = in_brain_tcs.T
  Y_demeaned = Y - np.mean(Y, axis=1).reshape([-1, 1])
  unscaled_cov = Y_demeaned.dot(Y_demeaned.T)
  U, S, V = npl.svd(unscaled_cov)

  n_betas = 10

  X = np.ones((n_trs - 5, n_betas))
  X[:, 0] = target_convolved
  X[:, 1] = nontarget_convolved
  X[:, 2] = error_convolved
  X[:, 3] = block_regressor
  X[:, 4] = block_start_cues
  X[:, 5] = block_end_cues
  X[:, 6] = linear_drift
  X[:, 7] = qudratic_drift
  X[:, 8] = U[:,0]
  # 9th column is the intercept

  B = npl.pinv(X).dot(Y)

  residuals = in_brain_tcs - X.dot(B).T

  B[(3,4,5,6,7,8,9),:] = 0

  # project Y onto the functional betas
  functional_Y = X.dot(B).T

  b_vols = np.zeros((data.shape))
  b_vols[in_brain_mask, :] = functional_Y + residuals

  return b_vols, img, in_brain_mask

def subject_c_values(img, data, dist_from_center, dic, in_brain_mask):
	mm_to_vox = npl.inv(img.affine)

	roi_extractor = roi_extraction.SphereExtractor(in_brain_mask, dist_from_center)

	expanded_dic = expand_dic(dic, mm_to_vox, roi_extractor)

	mean_c_values = c_within(data, expanded_dic)
	mean_c_values.update(c_between(data, expanded_dic))
	return mean_c_values

def group_c_values(standard_group_source_prefix, cond_filepath_prefix, dist_from_center, dic, group_info):
	task_nums = ("001", "002", "003")
  
	# store layout
  #   level 1: task (0-back, 1-back, 2-back)
  #   level 2: group name (CON, SCZ)
  #   level 3: network name
  #   level 4: a list of ROI-ROI correlations
	c_values_store = {"001":{"con":{}, "scz":{}},
										"002":{"con":{}, "scz":{}},
										"003":{"con":{}, "scz":{}}}
  
	for group, subject_nums in group_info.items():
		for sn in subject_nums:
			for tn in task_nums:
				data, img, in_brain_mask = preprocessing_pipeline(sn, tn, standard_group_source_prefix, cond_filepath_prefix)
				mean_c_values_per_net_pair = subject_c_values(img, data, dist_from_center, dic, in_brain_mask)

				for network_pair_name, c_value in mean_c_values_per_net_pair.items():
					group_name = "con" if group in ("fmri_con", "fmri_con_sib") else "scz"
					if network_pair_name not in c_values_store[tn][group_name]:
						c_values_store[tn][group_name][network_pair_name] = [c_value]
					else:
						c_values_store[tn][group_name][network_pair_name].append(c_value)
	return c_values_store

if __name__ == "__main__":

  dic = roi_extraction.dic
  dist_from_center = 4
  CUTOFF = project_config.MNI_CUTOFF
  TR = project_config.TR

  standard_group_source_prefix = os.path.join(os.path.dirname(__file__), "..", "data")
  cond_filepath_prefix = os.path.join(os.path.dirname(__file__), "..", "data")
  output_filename = os.path.join(os.path.dirname(__file__), "..", "results")

  small_group_info = {"fmri_con":("011", "012", "015", "035", "036", "037"),
            "fmri_con_sib":("010", "013", "014", "021", "022", "038"),
            "fmri_scz":("007", "009", "017", "031"),
            "fmri_scz_sib":("006", "008", "018", "024")}

  c_values_store = group_c_values(standard_group_source_prefix, cond_filepath_prefix, dist_from_center, dic, small_group_info)

  generate_connectivity_results(c_values_store, output_filename)

  # change target r-values into list format
  con_dmn_cer = np.ravel(c_values_store["003"]["con"]["Default-Cerebellar"]).tolist()
  scz_dmn_cer = np.ravel(c_values_store["003"]["scz"]["Default-Cerebellar"]).tolist()

  con_cer_co = np.ravel(c_values_store["003"]["con"]["Cerebellar-Cingulo-Opercular"]).tolist()
  scz_cer_co = np.ravel(c_values_store["003"]["scz"]["Cerebellar-Cingulo-Opercular"]).tolist()

  con_dmn_co = np.ravel(c_values_store["003"]["con"]["Default-Cingulo-Opercular"]).tolist()
  scz_dmn_co = np.ravel(c_values_store["003"]["scz"]["Default-Cingulo-Opercular"]).tolist()

  con_fp_cer = np.ravel(c_values_store["003"]["con"]["Fronto-Parietal-Cerebellar"]).tolist()
  scz_fp_cer = np.ravel(c_values_store["003"]["scz"]["Fronto-Parietal-Cerebellar"]).tolist()

  con_dmn_fp = np.ravel(c_values_store["003"]["con"]["Default-Fronto-Parietal"]).tolist()
  scz_dmn_fp = np.ravel(c_values_store["003"]["scz"]["Default-Fronto-Parietal"]).tolist()

  con_fp_co = np.ravel(c_values_store["003"]["con"]["Fronto-Parietal-Cingulo-Opercular"]).tolist()
  scz_fp_co = np.ravel(c_values_store["003"]["scz"]["Fronto-Parietal-Cingulo-Opercular"]).tolist()

  # perform permutation test
  dmn_cer_p_value = permute(scz_dmn_cer,con_dmn_cer)  
  cer_co_p_value = permute(scz_cer_co,con_cer_co)
  dmn_co_p_value = permute(scz_dmn_co,con_dmn_co)
  fp_cer_p_value = permute(scz_fp_cer,con_fp_cer)
  dmn_fp_p_value = permute(scz_dmn_fp,con_dmn_fp)
  fp_co_p_value = permute(scz_fp_co,con_fp_co)

