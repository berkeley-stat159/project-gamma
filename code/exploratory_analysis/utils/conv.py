import project_config
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gamma
from stimuli_revised import events2neural

TIME_UNIT = 0.1
HRF_TIME_LENGTH = 30

def hrf(times):
    # Gamma pdf for the peak
    peak_values = gamma.pdf(times, 6)
    # Gamma pdf for the undershoot
    undershoot_values = gamma.pdf(times, 12)
    # Combine them
    values = peak_values - 0.35 * undershoot_values
    # Scale max to 0.06
    return values / np.max(values) * 0.06

def hrf_prep(time_length):
	tr_times = np.arange(0, time_length, TIME_UNIT)
	hrf_at_trs = hrf(tr_times)
	return hrf_at_trs

def rescaled (convolved,TR,n_trs):
  tmp = np.reshape(convolved,(n_trs,int(TR/TIME_UNIT)))
  ret = np.median(tmp,axis=1)
  return ret

def conv_main(n_trs, filename, TR):
  """ 
  Read on-off neural prediction from condition file in FILENAME, convolve the 
  neural prediction with a predefined hrf function.

  Since convolved neural prediction has a unit of 0.1 second while TR has a
  unit of 2.5 seconds, our strategy picks the median of the span of 
  neural prediction values that correspond to a TR.

  Parameters
  ----------
  n_trs : number of TRs in functional run (i.e. length of a time course in nii array)
  filename : condition file that stores information regarding on and off time of tasks in a run
  TR: time span a nii array measurement corresponds to

  Returns
  -------
  convolved : return an array of convolved neural prediction

  """
  hrf_at_trs = hrf_prep(HRF_TIME_LENGTH)
  neural_prediction = events2neural(filename, 0.1, n_trs)
  all_tr_times = np.arange(n_trs * TR / TIME_UNIT) * TIME_UNIT
  convolved = np.convolve(neural_prediction, hrf_at_trs)
  n_to_remove = len(hrf_at_trs) - 1
  convolved = convolved[:-n_to_remove]
  ret = rescaled(convolved,TR,n_trs)
  return ret