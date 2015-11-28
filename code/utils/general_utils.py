import project_config
import nibabel as nib
import numpy as np
from itertools import product
from os.path import join

def vol_index_iter(shape):
  return product(range(shape[0]), range(shape[1]), range(shape[2]))

def index_iter_2d(shape):
  return product(range(shape[0]), range(shape[1]))

def prepare_data_single(subject_num, task_num, is_standard, source_prefix):
  img = prepare_img_single(subject_num, task_num, is_standard, source_prefix)
  return img.get_data()[..., 5:]

def prepare_img_single(subject_num, task_num, is_standard, source_prefix):
  if is_standard:
    img = nib.load(join(source_prefix, "sub%s_task%s_run001_func_data_mni.nii.gz" % (subject_num, task_num)))
  else:
    img = nib.load(join(source_prefix, "ds115_sub001-005/sub%s/BOLD/task%s_run001/bold.nii.gz" % (subject_num, task_num)))
  return img

def form_cond_filepath(subject_num, task_num, cond_num, cond_filepath_prefix):
  return join(cond_filepath_prefix, "sub%s" % (subject_num), "model/model001/onsets", "task%s_run001" % (task_num), "cond%s.txt" % (cond_num))

def prepare_mask(data_4d, cutoff):
  in_brain_mask = np.mean(data_4d, axis=-1) > cutoff
  return in_brain_mask, data_4d[in_brain_mask]

def prepare_data(subject_num, prefix):
  BOLD_file_1 = prefix + 'ds115_sub001-005/sub%s/BOLD/task001_run001/bold.nii.gz' % (subject_num)
  BOLD_file_2 = prefix + 'ds115_sub001-005/sub%s/BOLD/task002_run001/bold.nii.gz' % (subject_num)
  BOLD_file_3 = prefix + 'ds115_sub001-005/sub%s/BOLD/task003_run001/bold.nii.gz' % (subject_num)

  img_1 = nib.load(BOLD_file_1)
  data_1 = img_1.get_data()
  data_1 = data_1[..., 5:]

  img_2 = nib.load(BOLD_file_2)
  data_2 = img_2.get_data()
  data_2 = data_2[..., 5:]

  img_3 = nib.load(BOLD_file_3)
  data_3 = img_3.get_data()
  data_3 = data_3[..., 5:]

  return data_1, data_2, data_3

def prepare_images(subject_num, prefix):
  BOLD_file_1 = prefix + 'ds115_sub001-005/sub%s/BOLD/task001_run001/bold.nii.gz' % (subject_num)
  BOLD_file_2 = prefix + 'ds115_sub001-005/sub%s/BOLD/task002_run001/bold.nii.gz' % (subject_num)
  BOLD_file_3 = prefix + 'ds115_sub001-005/sub%s/BOLD/task003_run001/bold.nii.gz' % (subject_num)

  return nib.load(BOLD_file_1), nib.load(BOLD_file_2), nib.load(BOLD_file_3)

def prepare_cond_filenames(subject_num, prefix):
  cond_file_1 = prefix + 'ds115_sub001-005/sub%s/model/model001/onsets/task001_run001/cond002.txt' % (subject_num)
  cond_file_2 = prefix + 'ds115_sub001-005/sub%s/model/model001/onsets/task002_run001/cond002.txt' % (subject_num)
  cond_file_3 = prefix + 'ds115_sub001-005/sub%s/model/model001/onsets/task003_run001/cond002.txt' % (subject_num)
  return cond_file_1, cond_file_2, cond_file_3