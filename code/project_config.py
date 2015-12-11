"""
Convenient way to expose filepaths to scripts. Also, important
constants are centralized here to avoid multiple copies.
"""

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils', 'tests'))

TR = 2.5
#we choose cutoff value values by inspecting the histogram of data values of the standard mni brain
MNI_CUTOFF = 5000
MIN_STD_SHAPE = (91, 109, 91)