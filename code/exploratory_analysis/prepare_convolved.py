import project_config
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
from scipy.stats import gamma
from stimuli_revised import events2neural
from conv import conv_main

"""
Replace these variables before running the script
"""
cond_filename = "../../../ds115_sub010-014/sub013/model/model001/onsets/task001_run001/cond002.txt"
n_trs = 132


TR = project_config.TR
convolved = conv_main(n_trs, cond_filename, TR)

#save convolved data in txt file:
np.savetxt('results/conv_data.txt', convolved)



# tr_times = np.arange(0, time_length, time_unit)
# hrf_at_trs = hrf(tr_times)
# len(hrf_at_trs)
# plt.plot(tr_times, hrf_at_trs)
# plt.xlabel('time')
# plt.ylabel('HRF sampled every 2.5 seconds')

# n_vols = 132
# neural_prediction = events2neural('cond_nb_tar.txt',
#                                   0.1, n_vols)
# all_tr_times = np.arange(n_vols*TR/time_unit)*.1
# plt.plot(all_tr_times, neural_prediction)
# plt.savefig("on_off_sig.png")
# plt.close()


# convolved = np.convolve(neural_prediction, hrf_at_trs)
# N = len(neural_prediction)
# M = len(hrf_at_trs)  # M == 12
# len(convolved) == N + M - 1

# #the plot is too weird here. I think we need to revise the hrf functions
# n_to_remove = len(hrf_at_trs) - 1
# convolved = convolved[:-n_to_remove]
# x  = np.arange(132)
#  plt.plot(x, see)
# plt.plot(all_tr_times, convolved)
# plt.title("Convolved Data")
# plt.savefig("convolved.png")


