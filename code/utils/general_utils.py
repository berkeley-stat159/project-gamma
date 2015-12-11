"""
Convenient methods for preparing fMRI data as well as
condition files.
"""

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import project_config
import nibabel as nib
import numpy as np
from itertools import product
from os.path import join

def vol_index_iter(shape):
  return product(range(shape[0]), range(shape[1]), range(shape[2]))

def plane_index_iter(shape):
  return product(range(shape[0]), range(shape[1]))

def prepare_standard_data(subject_num, task_num, source_prefix):
  img = prepare_standard_img(subject_num, task_num, source_prefix)
  return img.get_data()[..., 5:]

def prepare_standard_img(subject_num, task_num, source_prefix):
  return nib.load(join(source_prefix, "sub%s_task%s_run001_func_data_mni.nii.gz" % (subject_num, task_num)))

def form_cond_filepath(subject_num, task_num, cond_num, cond_filepath_prefix):
  return join(cond_filepath_prefix, "sub%s" % (subject_num), "model/model001/onsets", "task%s_run001" % (task_num), "cond%s.txt" % (cond_num))

def prepare_mask(data_4d, cutoff):
  in_brain_mask = np.mean(data_4d, axis=-1) > cutoff
  return in_brain_mask, data_4d[in_brain_mask]