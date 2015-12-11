"""
Helpers for computing t values w.r.t a beta against the null hypothesis that
it is zero for a voxel time course.
"""

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
import project_config
import numpy as np
import numpy.linalg as npl
from scipy.stats import t as t_distribution

def df(X):
  return X.shape[0] - npl.matrix_rank(X)

def rse(X,Y, betas_hat):
  df_X = df(X)
  return np.sum((Y - X.dot(betas_hat)) ** 2, axis=0) * 1.0 / df_X, df_X

def compute_t_values(X, betas_hat, Y, target_beta):
  """
  Compute t values w.r.t a beta against the null hypothesis that it is
  zero for a voxel time course.
  
  Parameters
  ----------
  X : design matrix
  betas_hat : estimated betas from linear model fit
  target_beta : the specific beta in the design matrix to compute t values on

  Returns
  -------
  t_values : t values for hypothesis testing of the predictor variables as 
  outline in the notes below:
  http://dept.stat.lsa.umich.edu/~kshedden/Courses/Stat401/Notes/401-multreg.pdf

  """

  s_sq, df = rse(X, Y, betas_hat)
  cov_matrix = npl.inv(X.T.dot(X))[0,0]
  sd_beta = np.sqrt(s_sq * cov_matrix)

  t_values = betas_hat[target_beta, :] / sd_beta

  return t_values
