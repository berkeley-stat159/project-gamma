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

np.savetxt('results/conv_data.txt', convolved)