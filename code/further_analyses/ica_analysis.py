"""
A set of functions for extracting and visualizing results from applying independent components analysis (ICA) on the
preprocessed neuroimaging data.
"""

import os
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt

def prep_data(data_path='/Users/nimahejazi/Dropbox/159_projData/preprocessed/',subj_num):
  BOLD_file_1 = os.path.join(data_path,'sub'+subj_num+'_BOLD','task001_run001/filtered_func_data_mni'+'.'+'nii.gz')
  BOLD_file_2 = os.path.join(data_path,'sub'+subj_num+'_BOLD','task002_run001/filtered_func_data_mni'+'.'+'nii.gz')
  BOLD_file_3 = os.path.join(data_path,'sub'+subj_num+'_BOLD','task003_run001/filtered_func_data_mni'+'.'+'nii.gz')

  img_1 = nib.load(BOLD_file_1)
  data_1 = img_1.get_data()
  data_1 = data_1[..., 5:]

  img_2 = nib.load(BOLD_file_2)
  data_2 = img_2.get_data()
  data_2 = data_2[..., 5:]

  img_3 = nib.load(BOLD_file_3)
  data_3 = img_3.get_data()
  data_3 = data_3[..., 5:]

### Preprocess ################################################################
from nilearn.input_data import NiftiMasker

# Remove the background with mask_strategy='epi' to compute the mask from the EPI images

def clean_data():
  masker = NiftiMasker(smoothing_fwhm=8, memory='nilearn_cache', memory_level=1,
                       mask_strategy='epi', standardize=False)
  data_masked_1 = masker.fit_transform(BOLD_file_1)
  data_masked_2 = masker.fit_transform(BOLD_file_2)
  data_masked_3 = masker.fit_transform(BOLD_file_3)
  
### Apply ICA #################################################################
from sklearn.decomposition import FastICA

def ica_apply(n_components=20):
  ica = FastICA(n_components = n_components, random_state = 42)
  components_masked_1 = ica.fit_transform(data_masked_1).T
  components_masked_2 = ica.fit_transform(data_masked_2).T
  components_masked_3 = ica.fit_transform(data_masked_3).T

  # Normalize estimated components, for thresholding to make sense
  components_masked_1 -= components_masked_1.mean(axis=0)
  components_masked_1 /= components_masked_1.std(axis=0)
  components_masked_2 -= components_masked_2.mean(axis=0)
  components_masked_2 /= components_masked_2.std(axis=0)
  components_masked_3 -= components_masked_3.mean(axis=0)
  components_masked_3 /= components_masked_3.std(axis=0)
  
  # Threshold
  components_masked_1[components_masked_1 < .8] = 0
  components_masked_2[components_masked_2 < .8] = 0
  components_masked_3[components_masked_3 < .8] = 0

  # Now invert the masking operation, going back to a full 3D representation
  component_img_1 = masker.inverse_transform(components_masked_1)
  component_img_2 = masker.inverse_transform(components_masked_2)
  component_img_3 = masker.inverse_transform(components_masked_3)

### Visualize the results #####################################################
# Show some interesting components
from nilearn import image
from nilearn.plotting import plot_stat_map

def ica_vis(subj_num):
  # Use the mean as a background
  mean_img_1 = image.mean_img(BOLD_file_1)
  mean_img_2 = image.mean_img(BOLD_file_2)
  mean_img_3 = image.mean_img(BOLD_file_3)

  plot_stat_map(image.index_img(component_img_1, 5), mean_img_1, output_file=os.path.join(data_path,'sub'+subj_num+'_BOLD','task001_run001'+'ica_1'+'.jpg'))
  plot_stat_map(image.index_img(component_img_1, 12), mean_img_1, output_file=os.path.join(data_path,'sub'+subj_num+'_BOLD','task001_run001'+'ica_2'+'.jpg'))

  plot_stat_map(image.index_img(component_img_2, 5), mean_img_2, output_file=os.path.join(data_path,'sub'+subj_num+'_BOLD','task002_run001'+'ica_1'+'.jpg'))
  plot_stat_map(image.index_img(component_img_2, 12), mean_img_2, output_file=os.path.join(data_path,'sub'+subj_num+'_BOLD','task002_run001'+'ica_2'+'.jpg'))

plot_stat_map(image.index_img(component_img_3, 5), mean_img_3, output_file=os.path.join(data_path,'sub'+subj_num+'_BO\
LD','task003_run001'+'ica_1'+'.jpg'))
  plot_stat_map(image.index_img(component_img_3, 12), mean_img_3, output_file=os.path.join(data_path,'sub'+subj_num+'_BOLD','task003_run001'+'ica_2'+'.jpg'))



import project_config
from sklearn.decomposition import PCA

def first_pcs_removed(data_2d, n_pcs_removed):
  pca = PCA(n_components=n_pcs_removed)
  fitted = pca.fit(data_2d).transform(data_2d)
  reconstruct = pca.inverse_transform(fitted)
  residuals = data_2d - reconstruct
  return residuals

def project_onto_first_pcs(data_2d,n_pcs):
  pca = PCA(n_components=n_pcs)
  fitted = pca.fit(data_2d).transform(data_2d)
  return fitted
