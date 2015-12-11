"""
EDA:

This module detects the exteded RMS outliers and generates the plot for those outliers.
Results of the analysis are to understand the noise in fMRI data and justify the need 
for additional preprocessing steps.
We detect the outliers on "sub011, task001_run_001"
"""

import project_config
import nibabel as nib
import os
import numpy as np 
import outliers_utils
import matplotlib.pyplot as plt
from general_utils import form_cond_filepath

data_dir_path = os.path.join(os.path.dirname(__file__), '..', 'data')
output_dir = os.path.join(os.path.dirname(__file__), '..', 'results')
BOLD_file_1 = os.path.join(data_dir_path, 'sub011/BOLD/task001_run001/bold.nii.gz')
cond_filename = form_cond_filepath('011', '001', '002', data_dir_path)

#loading data
img = nib.load(BOLD_file_1)
data = img.get_data() 
ds1 = data.shape
#drop the first five
data = data[..., 5:]

#standard deviations of all voxels along the TRs.
std = outliers_utils.vol_std(data)

#find the std outliers
outlier = outliers_utils.iqr_outliers(std)[0]

#plot the std outliers
std_outlier=[]
low = outliers_utils.iqr_outliers(std)[1][0]
high = outliers_utils.iqr_outliers(std)[1][1]
for i in outlier:
	std_outlier.append(std[i])
x=np.arange(data.shape[-1])

plt.figure()

std1, = plt.plot(x,std,'b',label="std values")
std2, = plt.plot(outlier,std_outlier,'ro',label="outliers")
lowbound = plt.axhline(y=low,color='r',ls='dashed',label='lower IRQ')
highbound = plt.axhline(y=high,color='g',ls='dashed',label='higher IRQ')
plt.legend(handles=[std1, std2, lowbound,highbound],loc=4)
plt.ylabel('standard deviation')
plt.xlabel('volumns')
plt.title('Std outliers Detection for Sub011, Task001')
plt.savefig(os.path.join(output_dir,'sub011_task011_std_outliers.png'), format='png',dpi=500)

#RMS diffrence
rms = outliers_utils.vol_rms_diff(data)
rms_outlier = outliers_utils.iqr_outliers(rms)[0]
rms_outlier_value = []
for i in rms_outlier:
 	rms_outlier_value.append(rms[i])

#extended RMS outliers
ext_outlier = outliers_utils.extend_diff_outliers(rms_outlier)
rms.append(0)
ext_outlier_value = []
for i in ext_outlier:
	ext_outlier_value.append(rms[i])
low_ext = outliers_utils.iqr_outliers(rms)[1][0]
high_ext = outliers_utils.iqr_outliers(rms)[1][1]
xxx = np.arange(len(rms))

plt.figure()

plt.axis([0,140,5,15])
ext1, = plt.plot(xxx,rms,'b',label="rms values")
ext2, = plt.plot(ext_outlier,ext_outlier_value,'ro',label="extended outliers")
lowbound_ext = plt.axhline(y=low_ext,color='r',ls='dashed',label='lower IRQ')
highbound_ext = plt.axhline(y=high_ext,color='g',ls='dashed',label='higher IRQ')
plt.legend(handles=[ext1, ext2, lowbound_ext,highbound_ext],loc=1)
plt.ylabel('RMS difference')
plt.xlabel('volumns')
plt.title('Extended RMS difference outliers for Sub011, Task001')
plt.savefig(os.path.join(output_dir,'sub011_task011_extended_RMS_outliers.png'))
