"""
This script analyzes correlation between BOLD meansurements and a baseline 
value. The baseline value is extracted from convolution between neural 
prediction values and a gamma hrf function (see conv.py).

We employ two methods to find activation regions. A comparison is made.

"""

import project_config
import numpy as np
import nibabel as nib
import general_utils
import matplotlib.pyplot as plt
from conv import conv_main

"""
Replace these variables before running the script
"""
bold_data_filename = '../../../ds115_sub010-014/sub013/BOLD/task001_run001/bold.nii.gz'
cond_filename = "../../../ds115_sub010-014/sub013/model/model001/onsets/task001_run001/cond002.txt"


img = nib.load(bold_data_filename)
data = img.get_data()
data = data[..., 4:]

TR = project_config.TR

tr_times = np.arange(0, 30, TR)
convolved = conv_main(data.shape[-1], cond_filename, TR)

corrs = np.zeros((data.shape[:-1]))
for i in general_utils.vol_index_iter(data.shape[:-1]):
  corrs[i] = np.corrcoef(data[i], convolved)[1,0]

plt.imshow(corrs[...,25])
plt.show()