"""
Wrappers for identifying first Principal Components and for projections onto the
chosen components as well as retrieving residuls. 
"""

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import project_config
import numpy as np
from sklearn.decomposition import PCA

def first_pcs_removed(data_2d, n_pcs_removed):
  pca = PCA(n_components=n_pcs_removed)
  fitted = pca.fit(data_2d).transform(data_2d)
  reconstruct = pca.inverse_transform(fitted)
  residuals = data_2d - reconstruct
  return residuals

def project_onto_first_pcs(data_2d, n_pcs):
  pca = PCA(n_components=n_pcs)
  fitted = pca.fit(data_2d).transform(data_2d)
  return fitted

