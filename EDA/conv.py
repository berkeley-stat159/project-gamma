import numpy as np
import matplotlib.pyplot as plt 
import scipy.stats
from scipy.stats import gamma
from stimuli_revised import events2neural

TR = 2.5
#duration = 0.769951
time_length = 30
time_unit = 0.1
##define a hrf for convolution
def hrf(times,time_unit):
    # Gamma pdf for the peak
    peak_values = gamma.pdf(times, 6)
    # Gamma pdf for the undershoot
    undershoot_values = gamma.pdf(times, 12)
    # Combine them
    values = peak_values - 0.35 * undershoot_values
    # Scale max to 0.6
    return values / np.max(values) * 0.6 *time_unit

tr_times = np.arange(0, time_length, time_unit)
hrf_at_trs = hrf(tr_times,time_unit)
len(hrf_at_trs)
plt.plot(tr_times, hrf_at_trs)
plt.xlabel('time')
plt.ylabel('HRF sampled every 2.5 seconds')


# def hrf_prep(time_unit,time_length):
# 	tr_times = np.arange(0, time_length, time_unit)
# 	hrf_at_trs = hrf(tr_times)
# 	return tr_times,hrf_at_trs


n_vols = 169
neural_prediction = events2neural('cond_nb_tar.txt',
                                  0.1, n_vols)
all_tr_times = np.arange(169*TR/time_unit)*.1
plt.plot(all_tr_times, neural_prediction)
plt.savefig("on_off_sig.png")
plt.close()


convolved = np.convolve(neural_prediction, hrf_at_trs)
N = len(neural_prediction)
M = len(hrf_at_trs)  # M == 12
len(convolved) == N + M - 1

#the plot is too weird here. I think we need to revise the hrf functions
n_to_remove = len(hrf_at_trs) - 1
convolved = convolved[:-n_to_remove]
plt.plot(all_tr_times, neural_prediction)
plt.plot(all_tr_times, convolved)
plt.title("Convolved Data")
plt.savefig("convolved.png")


