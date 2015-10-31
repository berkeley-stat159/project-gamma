from on_off import find_time_course
import kmeans
import numpy as np
from scipy.stats import gamma
import nibabel as nib
import general_helpers
import matplotlib.pyplot as plt

img = nib.load('bold.nii.gz')
data = img.get_data()
data = data[..., 4:]


# TODO: replace this with the agreed hrf implementation
def hrf(times):
  """ Return values for HRF at given times """
  # Gamma pdf for the peak
  peak_values = gamma.pdf(times, 6)
  # Gamma pdf for the undershoot
  undershoot_values = gamma.pdf(times, 12)
  # Combine them
  values = peak_values - 0.35 * undershoot_values
  # Scale max to 0.6
  return values / np.max(values) * 0.6

TR = 2.5
tr_times = np.arange(0, 30, TR)
hrf_at_trs = hrf(tr_times)
neural_prediction = on_off.find_time_course("cond002.txt", 2.5, data.shape[-1])
convolved = np.convolve(neural_prediction, hrf_at_trs)
n_to_remove = len(hrf_at_trs) - 1
convolved = convolved[:-n_to_remove]
corrs = np.zeros((data.shape[:-1]))
for i in general_helpers.vol_index_iter(data.shape[:-1]):
  corrs[i] = np.corrcoef(data[i], convolved)[1,0]

# to visualize, e.g. plt.imshow(corrs[...,25]); plt.show()