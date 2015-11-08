import project_config
import os
import numpy as np
import scipy as sp
import nibabel as nib
import numpy.linalg as npl
import matplotlib.pyplot as plt

from diagnostics import *

"""
Replace these variables before running the script
"""
analysis_dir = '../ds115_sub001-005/sub001/BOLD/task001_run001/'
BOLD_file_1 = 'bold.nii.gz'



os.chdir(analysis_dir)
img = nib.load(BOLD_file_1)
data = img.get_data(BOLD_file_1)
data = data[...,5:] #drop first 5 volumes

sd = vol_std(data) #voxel standard deviations along all TRs
np.savetxt('results/voxel_sd_raw.txt', sd)

outliers = iqr_outliers(sd)[0] #finding outlier indices on sd
np.savetxt('results/voxel_sd_outliers.txt', outliers)

#plot the std outliers
sd_outlier=[]
low_thresh = iqr_outliers(sd)[1][0]
high_thresh = iqr_outliers(sd)[1][1]
for i in outliers:
    sd_outlier.append(sd[i])
x_vox = np.arange(data.shape[-1])
sd_a, = plt.plot(x_vox, sd, 'b', label="sd values")
sd_b, = plt.plot(outliers, sd_outlier,'ro', label="outliers")
low_thresh_line = plt.axhline(y = low_thresh, color='r', ls='dashed', label='25th percentile')
high_thresh_line = plt.axhline(y = high_thresh, color='g', ls='dashed', label='75th percentile')
plt.legend(handles=[sd_a, sd_b, low_thresh_line, high_thresh_line], loc=4)
plt.ylabel('Standard Deviations')
plt.xlabel('Voxels / Volumes')
plt.title('Outlier Detection Plot')
plt.savefig('results/vox_sd.png')
plt.show()

#RMS diffrence
rms = vol_rms_diff(data)
rms_outlier_info = iqr_outliers(rms)[0]
rms_outliers = []
for i in rms_outlier_info:
    rms_outliers.append(rms[i])
rms_low_thresh = iqr_outliers(rms)[1][0]
rms_high_thresh = iqr_outliers(rms)[1][1]
rms_vox = np.arange(len(rms))
plt.axis([0,140,0,25])
rms_a, = plt.plot(rms_vox, rms, 'b', label = "RMS Values")
rms_b, = plt.plot(rms_outlier_info, rms_outliers, 'ro', label="Outliers on RMS")
rms_low_thresh_line = plt.axhline(y = rms_low_thresh, color='r', ls='dashed', label='25th percentile')
rms_high_thresh_line = plt.axhline(y = rms_high_thresh, color='g', ls='dashed', label='75th percentile')
plt.legend(handles=[rms_a, rms_b, rms_low_thresh_line, rms_high_thresh_line], loc=1)
plt.ylabel('Differences in RMS')
plt.xlabel('Voxel Indices')
plt.title('Outliers in RMS Magnitudes')
plt.savefig('results/vol_rms_outliers.png')
plt.show()

#extended RMS outliers
extend_outliers = extend_diff_outliers(rms_outlier_info)
np.append(rms,0)
rms_outlier_ext = []
for i in extend_outliers:
    rms_outlier_ext.append(rms[i])
rms_ext_low = iqr_outliers(rms_outlier_ext)[1][0]
rms_ext_high = iqr_outliers(rms_outlier_ext)[1][1]
rms_ext_vox = np.arange(len(rms_outlier_ext))
plt.axis([0,140,0,25])
rms_ext_a, = plt.plot(rms_ext_vox, rms_outlier_ext, 'b', label = "RMS Values")
rms_ext_b, = plt.plot(extend_outliers, rms_outlier_ext, 'ro', label = "Potential RMS Outliers")
rms_ext_low_line = plt.axhline(y=rms_ext_low,color='r',ls='dashed', label='25th Percentile')
rms_ext_high_line = plt.axhline(y=rms_ext_high,color='g',ls='dashed', label='75th Percentile')
plt.legend(handles=[rms_ext_b, rms_ext_b, rms_ext_low_line, rms_ext_high_line],loc=1)
plt.ylabel('Differences in RMS')
plt.xlabel('Voxels/Volumes')
plt.title('RMS Outliers Extended')
plt.savefig('results/extended_vol_rms_outliers.png')
plt.show()

#drop outliers
rms = vol_rms_diff(data)
rms_outliers = iqr_outliers(rms)[0]
rms_extend_outliers = extend_diff_outliers(rms_outliers)
outlier_masking = np.ones(data.shape[-1])
outlier_masking[rms_extend_outliers] = 0
outlier_masking = np.array(outlier_masking, dtype=bool)
data_clean = data[..., outlier_masking]
