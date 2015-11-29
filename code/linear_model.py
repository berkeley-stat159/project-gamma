import project_config
import numpy as np
import numpy.linalg as npl
import matplotlib.pyplot as plt
import nibabel as nib
from general_utils import form_cond_filepath, prepare_data_single, prepare_mask
from stimuli_revised import events2neural_std
from conv import conv_target_non_target, conv_std
from gaussian_filter import spatial_smooth
from matplotlib import colors
from hypothesis import perform_t_tests

import pdb

def single_subject_linear_model(standard_source_prefix, cond_filepath_prefix, subject_num, task_num):

  data = prepare_data_single(subject_num, task_num, True, standard_source_prefix)

  n_trs = data.shape[-1] + 5

  cond_filename_003 = form_cond_filepath(subject_num, task_num, "003", cond_filepath_prefix)
  cond_filename_005 = form_cond_filepath(subject_num, task_num, "005", cond_filepath_prefix)
  cond_filename_001 = form_cond_filepath(subject_num, task_num, "001", cond_filepath_prefix)
  cond_filename_004 = form_cond_filepath(subject_num, task_num, "004", cond_filepath_prefix)

  # TODO: put cond007 back to 003
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

  B = npl.pinv(X).dot(Y)

  rs_squared = []
  for i in range(Y.shape[-1]):
    r_squared = 1 - np.sum((Y[:,i] - X.dot(B[:,i]))**2) * 1.0 / np.sum((Y[:,i] - np.mean(Y[:,i])) ** 2)
    rs_squared.append(r_squared)

  print "mean R squared across all voxels is " + str(np.mean(rs_squared))

  b_vols = np.zeros((data.shape[0:-1] + (n_betas,)))
  b_vols[in_brain_mask, :] = B.T

  t_test_target_beta = 0
  p_values = perform_t_tests(X, B, Y, t_test_target_beta)
  p_vols_beta_0 = np.zeros((data.shape[0:-1]))
  p_vols_beta_0[in_brain_mask] = p_values

  t_test_target_beta = 1
  p_values = perform_t_tests(X, B, Y, t_test_target_beta)
  p_vols_beta_1 = np.zeros((data.shape[0:-1]))
  p_vols_beta_1[in_brain_mask] = p_values


  return b_vols, in_brain_mask, U, Y, data, p_vols_beta_0, p_vols_beta_1

def plot_p_values(p_vols_smooth, in_brain_mask, brain_structure, nice_cmap_values, depth, title):
  plot(p_vols_smooth.reshape(p_vols_smooth.shape + (1,)), in_brain_mask, brain_structure, nice_cmap_values, 0, depth, title)

def plot(b_vols_smooth, in_brain_mask, brain_structure, nice_cmap_values, beta_index, depth, title):
  b_vols_smooth[~in_brain_mask] = np.nan
  nice_cmap = colors.ListedColormap(nice_cmap_values, 'actc')
  plt.imshow(brain_structure[...,depth], alpha=0.5)
  plt.imshow(b_vols_smooth[...,depth,beta_index], cmap=nice_cmap, alpha=0.5)
  plt.title(title)
  plt.colorbar()
  plt.show()


if __name__ == "__main__":

  # single subject, 0-back

  standard_source_prefix = "/Volumes/G-DRIVE mobile USB/fmri_con/"
  cond_filepath_prefix = "/Volumes/G-DRIVE mobile USB/fmri_non_mni/"
  brain_structure_path = "/Users/fenglin/Downloads/mni_icbm152_csf_tal_nlin_asym_09c_2mm.nii"
  nice_cmap_values_path = "actc.txt"

  subject_num = "011"
  task_num = "001"
  TR = project_config.TR

  plt.rcParams['image.cmap'] = 'gray'
  plt.rcParams['image.interpolation'] = 'nearest'

  brain_structure = nib.load(brain_structure_path).get_data()
  nice_cmap_values = np.loadtxt(nice_cmap_values_path)
  
  b_vols_smooth_0_back, in_brain_mask, U, Y, data, p_vols_0_back_beta_0, p_vols_0_back_beta_1 = single_subject_linear_model(standard_source_prefix, cond_filepath_prefix, subject_num, task_num)

  # visualize p values for target regressor
  plot_p_values(p_vols_0_back_beta_0, in_brain_mask, brain_structure, nice_cmap_values, 40, "z=40,target-beta p values,0-back")
  plot_p_values(p_vols_0_back_beta_0, in_brain_mask, brain_structure, nice_cmap_values, 50, "z=50,target-beta p values,0-back")
  plot_p_values(p_vols_0_back_beta_0, in_brain_mask, brain_structure, nice_cmap_values, 60, "z=60,target-beta p values,0-back")

  plot_p_values(p_vols_0_back_beta_1, in_brain_mask, brain_structure, nice_cmap_values, 40, "z=40,nontarget-beta p values,0-back")
  plot_p_values(p_vols_0_back_beta_1, in_brain_mask, brain_structure, nice_cmap_values, 50, "z=50,nontarget-beta p values,0-back")
  plot_p_values(p_vols_0_back_beta_1, in_brain_mask, brain_structure, nice_cmap_values, 60, "z=60,nontarget-beta p values,0-back")



  # show target betas
  plot(b_vols_smooth_0_back, in_brain_mask, brain_structure, nice_cmap_values, 0, 40, "z=40,target beta,0-back")
  plot(b_vols_smooth_0_back, in_brain_mask, brain_structure, nice_cmap_values, 0, 50, "z=50,target beta,0-back")
  plot(b_vols_smooth_0_back, in_brain_mask, brain_structure, nice_cmap_values, 0, 60, "z=60,target beta,0-back")

  plot(b_vols_smooth_0_back, in_brain_mask, brain_structure, nice_cmap_values, 1, 40, "z=40,non-target beta,0-back")
  plot(b_vols_smooth_0_back, in_brain_mask, brain_structure, nice_cmap_values, 1, 50, "z=50,non-target beta,0-back")
  plot(b_vols_smooth_0_back, in_brain_mask, brain_structure, nice_cmap_values, 1, 60, "z=60,non-target beta,0-back")

  # projection of first component
  plt.plot(U[:, 0])
  # plt.show()
  Y_demeaned = Y - np.mean(Y, axis=1).reshape([-1, 1])
  projections = U.T.dot(Y_demeaned)
  projection_vols = np.zeros(data.shape)
  projection_vols[in_brain_mask, :] = projections.T
  plt.imshow(projection_vols[:, :, 40, 0])
  # plt.show()

  # second component
  # this component starts to look like functional features
  plt.plot(U[:, 1])
  # plt.show()
  plt.imshow(projection_vols[:, :, 40, 1])
  # plt.show()

  # single subject, 0-back vs. 2-back

  task_num = "003"

  b_vols_smooth_2_back, in_brain_mask, U, Y, data, p_vols_2_back_beta_0, p_vols_2_back_beta_1 = single_subject_linear_model(standard_source_prefix, cond_filepath_prefix, subject_num, task_num)

  # visualize p values for target regressor
  plot_p_values(p_vols_2_back_beta_0, in_brain_mask, brain_structure, nice_cmap_values, 40, "z=40,target-beta p values,2-back")
  plot_p_values(p_vols_2_back_beta_0, in_brain_mask, brain_structure, nice_cmap_values, 50, "z=50,target-beta p values,2-back")
  plot_p_values(p_vols_2_back_beta_0, in_brain_mask, brain_structure, nice_cmap_values, 60, "z=60,target-beta p values,2-back")

  plot_p_values(p_vols_2_back_beta_1, in_brain_mask, brain_structure, nice_cmap_values, 40, "z=40,nontarget-beta p values,2-back")
  plot_p_values(p_vols_2_back_beta_1, in_brain_mask, brain_structure, nice_cmap_values, 50, "z=50,nontarget-beta p values,2-back")
  plot_p_values(p_vols_2_back_beta_1, in_brain_mask, brain_structure, nice_cmap_values, 60, "z=60,nontarget-beta p values,2-back")

  # show 2-back target betas
  plot(b_vols_smooth_2_back, in_brain_mask, brain_structure, nice_cmap_values, 0, 40, "z=40,target beta,2-back")
  plot(b_vols_smooth_2_back, in_brain_mask, brain_structure, nice_cmap_values, 0, 50, "z=50,target beta,2-back")
  plot(b_vols_smooth_2_back, in_brain_mask, brain_structure, nice_cmap_values, 0, 60, "z=60,target beta,2-back")

  plot(b_vols_smooth_2_back, in_brain_mask, brain_structure, nice_cmap_values, 1, 40, "z=40,non-target beta,2-back")
  plot(b_vols_smooth_2_back, in_brain_mask, brain_structure, nice_cmap_values, 1, 50, "z=50,non-target beta,2-back")
  plot(b_vols_smooth_2_back, in_brain_mask, brain_structure, nice_cmap_values, 1, 60, "z=60,non-target beta,2-back")


  # show 2-back target betas - 0-back target betas
  plot(b_vols_smooth_2_back - b_vols_smooth_0_back, in_brain_mask, brain_structure, nice_cmap_values, 0, 40, "2-back target betas - 0-back target betas")
