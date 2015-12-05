import project_config
from pca_utils import project_onto_first_pcs
from general_utils import prepare_standard_data, prepare_mask
import matplotlib.pyplot as plt
import numpy as np

def plot_first_pcs_projection(in_brain_vols_2d, in_brain_mask):
  projections = project_onto_first_pcs(in_brain_vols_2d, 8)
  
  fig = plt.figure()
  
  for i in range(1, 9):
    ax = fig.add_subplot("42" + str(i))
    ax.set_title("z=45, pc=%d, mni" % (i - 1))
    b_vols = np.zeros(in_brain_mask.shape)
    b_vols[in_brain_mask] = projections[:,i - 1]
    ax.imshow(b_vols[...,45], interpolation="nearest", cmap="gray")

  plt.show()

if __name__ == "__main__":

  standard_source_prefix = "/Volumes/G-DRIVE mobile USB/fmri_con/"

  subject_num = "011"
  task_num = "001"

  data_4d = prepare_standard_data(subject_num, task_num, standard_source_prefix)

  mean_vols = np.mean(data_4d, axis=-1)
  plt.hist(np.ravel(mean_vols), bins=100)
  plt.show()

  # Chose cutoff = 5500 from the histogram
  cutoff = 5500

  in_brain_mask, in_brain_vols = prepare_mask(data_4d, cutoff)
  plot_first_pcs_projection(in_brain_vols, in_brain_mask)

  # The first two PCs represent anatomical features. At the third PC, we start to
  # see patterns similar to those found in the literature. 
  # http://owenlab.uwo.ca/pdf/2005-Owen-HBM-N-Back%20Working%20Memory%20Paradigm.pdf