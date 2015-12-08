import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(__file__), 'utils'))

import pdb

TR = 2.5
#we choose cutoff value values by inspecting the histogram of data values of the standard mni brain
MNI_CUTOFF = 5000
MIN_STD_SHAPE = (91, 109, 91)