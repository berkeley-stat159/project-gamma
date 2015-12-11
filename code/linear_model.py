"""
Script for linear modeling of fMRI data to identify noise regressors and to investigate activation clusters.
"""

import project_config
import numpy as np
import numpy.linalg as npl
import matplotlib.pyplot as plt
import nibabel as nib
import os
import pandas as pd
from utils import general_utils
from multiple_comparison import multiple_comp
from general_utils import form_cond_filepath, prepare_standard_data, prepare_mask
from stimuli_revised import events2neural_std
from conv import conv_target_non_target, conv_std
from gaussian_filter import spatial_smooth
from matplotlib import colors
from hypothesis import compute_t_values

import pdb

def plot_first_four_pcs(U, Y, depth, output_filename):
  
  Y_demeaned = Y - np.mean(Y, axis=1).reshape([-1, 1])
  projections = U.T.dot(Y_demeaned)
  projection_vols = np.zeros(data.shape)
  projection_vols[in_brain_mask, :] = projections.T

  fig = plt.figure()

  for map_index, pc_index in ((221, 0),(222, 1),(223, 2),(224, 3)):

    ax = fig.add_subplot(map_index)
    ax.set_title("sub%s,z=%d,nth_pc=%s" % (subject_num, depth, pc_index))
    ax.imshow(projection_vols[:,:,depth,pc_index], interpolation="nearest", cmap="gray")

  plt.tight_layout()
  plt.savefig(os.path.join(output_filename, "sub011_task001_first_four_pcs.png"), format='png', dpi=500)      

def plot_target_betas_n_back(t_vols_n_back_beta_0, b_vols_smooth_n_back, in_brain_mask, brain_structure, nice_cmap, n_back):

  beta_index = 0

  plt.figure()

  b_vols_smooth_n_back[~in_brain_mask] = np.nan
  t_vols_n_back_beta_0[~in_brain_mask] = np.nan

  min_val = np.nanmin(b_vols_smooth_n_back[...,(40,50,60),beta_index])
  max_val = np.nanmax(b_vols_smooth_n_back[...,(40,50,60),beta_index])

  for map_index, depth in (((3,2,1), 40),((3,2,3), 50),((3,2,5), 60)):
    plt.subplot(*map_index)
    plt.title("z=%d,%s" % (depth, n_back + "-back target,beta values"))
    plt.imshow(brain_structure[...,depth], alpha=0.5)
    plt.imshow(b_vols_smooth_n_back[...,depth,beta_index], cmap=nice_cmap, alpha=0.5, vmin=min_val, vmax=max_val)
    plt.colorbar()
    plt.tight_layout()

  t_min_val = np.nanmin(t_vols_n_back_beta_0[...,(40,50,60)])
  t_max_val = np.nanmax(t_vols_n_back_beta_0[...,(40,50,60)])

  for map_index, depth in (((3,2,2), 40),((3,2,4), 50),((3,2,6), 60)):
    plt.subplot(*map_index)
    plt.title("z=%d,%s" % (depth, n_back + "-back target,t values"))
    plt.imshow(brain_structure[...,depth], alpha=0.5)
    plt.imshow(t_vols_n_back_beta_0[...,depth], cmap=nice_cmap, alpha=0.5, vmin=t_min_val, vmax=t_max_val)
    plt.colorbar()
    plt.tight_layout()

  plt.savefig(os.path.join(output_filename, "sub011_target_betas_%s_back.png" % (n_back)), format='png', dpi=500)  

def plot_nontarget_betas_n_back(t_vols_n_back_beta_1, b_vols_smooth_n_back, in_brain_mask, brain_structure, nice_cmap, n_back):

  beta_index = 1

  b_vols_smooth_n_back[~in_brain_mask] = np.nan
  t_vols_n_back_beta_1[~in_brain_mask] = np.nan
  min_val = np.nanmin(b_vols_smooth_n_back[...,(40,50,60),beta_index])
  max_val = np.nanmax(b_vols_smooth_n_back[...,(40,50,60),beta_index])

  plt.figure()

  for map_index, depth in (((3,2,1), 40),((3,2,3), 50),((3,2,5), 60)):
    plt.subplot(*map_index)
    plt.title("z=%d,%s" % (depth, n_back + "-back nontarget,beta values"))
    plt.imshow(brain_structure[...,depth], alpha=0.5)
    plt.imshow(b_vols_smooth_n_back[...,depth,beta_index], cmap=nice_cmap, alpha=0.5, vmin=min_val, vmax=max_val)
    plt.colorbar()
    plt.tight_layout()

  t_min_val = np.nanmin(t_vols_n_back_beta_1[...,(40,50,60)])
  t_max_val = np.nanmax(t_vols_n_back_beta_1[...,(40,50,60)])

  for map_index, depth in (((3,2,2), 40),((3,2,4), 50),((3,2,6), 60)):
    plt.subplot(*map_index)
    plt.title("z=%d,%s" % (depth, n_back + "-back nontarget,t values"))
    plt.imshow(brain_structure[...,depth], alpha=0.5)
    plt.imshow(t_vols_n_back_beta_1[...,depth], cmap=nice_cmap, alpha=0.5, vmin=t_min_val, vmax=t_max_val)
    plt.colorbar()
    plt.tight_layout()

  plt.savefig(os.path.join(output_filename, "sub011_nontarget_betas_%s_back.png" % (n_back)), format='png', dpi=500)  

def plot_noise_regressor_betas(b_vols_smooth, t_vols_beta_6_to_9, brain_structure, in_brain_mask, nice_cmap):

  plt.figure()

  min_val = np.nanmin(b_vols_smooth[...,40,(6,7,9)])
  max_val = np.nanmax(b_vols_smooth[...,40,(6,7,9)])

  plt.subplot(3,2,1)
  plt.title("z=%d,%s" % (40, "linear drift,betas"))
  b_vols_smooth[~in_brain_mask] = np.nan
  plt.imshow(brain_structure[...,40], alpha=0.5)
  plt.imshow(b_vols_smooth[...,40,6], cmap=nice_cmap, alpha=0.5, vmin=min_val, vmax=max_val)
  plt.colorbar()
  plt.tight_layout()

  plt.subplot(3,2,3)
  plt.title("z=%d,%s" % (40, "quadratic drift,betas"))
  b_vols_smooth[~in_brain_mask] = np.nan
  plt.imshow(brain_structure[...,40], alpha=0.5)
  plt.imshow(b_vols_smooth[...,40,7], cmap=nice_cmap, alpha=0.5, vmin=min_val, vmax=max_val)
  plt.colorbar()
  plt.tight_layout()

  plt.subplot(3,2,5)
  plt.title("z=%d,%s" % (40, "second PC,betas"))
  b_vols_smooth[~in_brain_mask] = np.nan
  plt.imshow(brain_structure[...,40], alpha=0.5)
  plt.imshow(b_vols_smooth[...,40,9], cmap=nice_cmap, alpha=0.5, vmin=min_val, vmax=max_val)
  plt.colorbar()
  plt.tight_layout()

  t_vols_beta_6_to_9[0][~in_brain_mask] = np.nan
  t_vols_beta_6_to_9[1][~in_brain_mask] = np.nan
  t_vols_beta_6_to_9[3][~in_brain_mask] = np.nan

  t_min_val = np.nanmin([t_vols_beta_6_to_9[0][...,40], t_vols_beta_6_to_9[1][...,40], t_vols_beta_6_to_9[3][...,40]])
  t_max_val = np.nanmax([t_vols_beta_6_to_9[0][...,40], t_vols_beta_6_to_9[1][...,40], t_vols_beta_6_to_9[3][...,40]])

  plt.subplot(3,2,2)
  plt.title("z=%d,%s" % (40, "linear drift,t values"))
  plt.imshow(brain_structure[...,40], alpha=0.5)
  plt.imshow(t_vols_beta_6_to_9[0][...,40], cmap=nice_cmap, alpha=0.5, vmin=t_min_val, vmax=t_max_val)
  plt.colorbar()
  plt.tight_layout()

  plt.subplot(3,2,4)
  plt.title("z=%d,%s" % (40, "quadratic drift,t values"))
  plt.imshow(brain_structure[...,40], alpha=0.5)
  plt.imshow(t_vols_beta_6_to_9[1][...,40], cmap=nice_cmap, alpha=0.5, vmin=t_min_val, vmax=t_max_val)
  plt.colorbar()
  plt.tight_layout()

  plt.subplot(3,2,6)
  plt.title("z=%d,%s" % (40, "second PC,t values"))
  plt.imshow(brain_structure[...,40], alpha=0.5)
  plt.imshow(t_vols_beta_6_to_9[3][...,40], cmap=nice_cmap, alpha=0.5, vmin=t_min_val, vmax=t_max_val)
  plt.colorbar()
  plt.tight_layout()

  plt.savefig(os.path.join(output_filename, "sub001_noise_regressors_betas_map.png"), format='png', dpi=500)  


def single_subject_linear_model(standard_source_prefix, cond_filepath_prefix, subject_num, task_num, output_filename):

  data = prepare_standard_data(subject_num, task_num, standard_source_prefix)

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

  in_brain_mask, _ = prepare_mask(data, 5000)

  pad_thickness = 2.0
  sigma = 2.0

  b_vols = spatial_smooth(data, in_brain_mask, pad_thickness, sigma, False)
  in_brain_tcs = b_vols[in_brain_mask]

  Y = in_brain_tcs.T
  Y_demeaned = Y - np.mean(Y, axis=1).reshape([-1, 1])
  unscaled_cov = Y_demeaned.dot(Y_demeaned.T)
  U, S, V = npl.svd(unscaled_cov)

  n_betas = 11

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
  X[:, 9] = U[:,1]
  # 10th column is the intercept


  # plot design matrix
  plt.figure()
  plt.imshow(X, aspect=0.1)
  plt.savefig(os.path.join(output_filename, "sub%s_task%s_design_matrix.png" % (subject_num, task_num)), format='png', dpi=500)      

  B = npl.pinv(X).dot(Y)

  # test normality of residuals
  residuals = Y.T - X.dot(B).T
  alpha_test, bonferroni_test, hochberg_test, benjamini_test = [val * 1.0 / Y.shape[-1] for val in multiple_comp(residuals)]
  normality_test_results = {"Alpha Test":alpha_test, "Bonferroni Procedure":bonferroni_test,"Hochberg Procedure":hochberg_test,"Benjamini-Hochberg Procedure":benjamini_test}

  normality_test_pd = pd.DataFrame(normality_test_results, index=["Failure Rate"])

  normality_test_pd.to_csv(os.path.join(output_filename, "sub%s_linear_model_normality_tests_failure_rates.csv" % subject_num))


  rs_squared = []
  for i in range(Y.shape[-1]):
    r_squared = 1 - np.sum((Y[:,i] - X.dot(B[:,i]))**2) * 1.0 / np.sum((Y[:,i] - np.mean(Y[:,i])) ** 2)
    rs_squared.append(r_squared)

  np.savetxt(os.path.join(output_filename, "glm_mean_R_squared_" + ("0_back" if task_num == "001" else "2_back") + ".txt"), np.array([np.mean(rs_squared)]))

  b_vols = np.zeros((data.shape[0:-1] + (n_betas,)))
  b_vols[in_brain_mask, :] = B.T


  # compute t values for target and nontarget betas

  t_test_target_beta = 0
  t_values = compute_t_values(X, B, Y, t_test_target_beta)
  t_vols_beta_0 = np.zeros((data.shape[0:-1]))
  t_vols_beta_0[in_brain_mask] = t_values

  t_test_target_beta = 1
  t_values = compute_t_values(X, B, Y, t_test_target_beta)
  t_vols_beta_1 = np.zeros((data.shape[0:-1]))
  t_vols_beta_1[in_brain_mask] = t_values

  # compute t values for noise regressor betas

  t_values = compute_t_values(X, B, Y, 6)
  t_vols_beta_6 = np.zeros((data.shape[0:-1]))
  t_vols_beta_6[in_brain_mask] = t_values

  t_values = compute_t_values(X, B, Y, 7)
  t_vols_beta_7 = np.zeros((data.shape[0:-1]))
  t_vols_beta_7[in_brain_mask] = t_values

  t_values = compute_t_values(X, B, Y, 8)
  t_vols_beta_8 = np.zeros((data.shape[0:-1]))
  t_vols_beta_8[in_brain_mask] = t_values

  t_values = compute_t_values(X, B, Y, 9)
  t_vols_beta_9 = np.zeros((data.shape[0:-1]))
  t_vols_beta_9[in_brain_mask] = t_values

  t_vols_beta_6_to_9 = [t_vols_beta_6, t_vols_beta_7, t_vols_beta_8, t_vols_beta_9]

  return b_vols, in_brain_mask, U, Y, data, t_vols_beta_0, t_vols_beta_1, t_vols_beta_6_to_9  

if __name__ == "__main__":

  # single subject, 0-back

  data_dir_path = os.path.join(os.path.dirname(__file__), "..", "data")

  standard_source_prefix = data_dir_path
  cond_filepath_prefix = data_dir_path
  brain_structure_path = os.path.join(data_dir_path, "mni_icbm152_csf_tal_nlin_asym_09c_2mm.nii")
  nice_cmap_values_path = os.path.join(data_dir_path, "actc.txt")
  output_filename = os.path.join(os.path.dirname(__file__), "..", "results")

  subject_num = "011"
  task_num = "001"
  TR = project_config.TR

  plt.rcParams['image.cmap'] = 'gray'
  plt.rcParams['image.interpolation'] = 'nearest'

  brain_structure = nib.load(brain_structure_path).get_data()
  nice_cmap_values = np.loadtxt(nice_cmap_values_path)
  
  b_vols_smooth_0_back, in_brain_mask, U, Y, data, t_vols_0_back_beta_0, t_vols_0_back_beta_1, t_vols_beta_6_to_9 = single_subject_linear_model(standard_source_prefix, cond_filepath_prefix, subject_num, task_num, output_filename)

  nice_cmap = colors.ListedColormap(nice_cmap_values, 'actc')

  plot_noise_regressor_betas(b_vols_smooth_0_back, t_vols_beta_6_to_9, brain_structure, in_brain_mask, nice_cmap)

  plot_target_betas_n_back(t_vols_0_back_beta_0, b_vols_smooth_0_back, in_brain_mask, brain_structure, nice_cmap, "0")

  plot_nontarget_betas_n_back(t_vols_0_back_beta_1, b_vols_smooth_0_back, in_brain_mask, brain_structure, nice_cmap, "0")
  
  # projection of first four 
  plot_first_four_pcs(U, Y, 40, output_filename)

  # single subject, 0-back vs. 2-back

  task_num = "003"

  b_vols_smooth_2_back, in_brain_mask, U, Y, data, t_vols_2_back_beta_0, t_vols_2_back_beta_1, _ = single_subject_linear_model(standard_source_prefix, cond_filepath_prefix, subject_num, task_num, output_filename)

  plot_target_betas_n_back(t_vols_2_back_beta_0, b_vols_smooth_2_back, in_brain_mask, brain_structure, nice_cmap, "2")

  plot_nontarget_betas_n_back(t_vols_2_back_beta_1, b_vols_smooth_2_back, in_brain_mask, brain_structure, nice_cmap, "2")
