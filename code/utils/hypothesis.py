import project_config
import numpy as np
import numpy.linalg as npl
from scipy.stats import t as t_distribution

def df(X):
  return X.shape[0] - npl.matrix_rank(X)

def rse(X,Y, betas_hat):
  df_X = df(X)
  return np.sum((Y - X.dot(betas_hat)) ** 2, axis=0) * 1.0 / df_X, df_X

def perform_t_tests(X, betas_hat, Y, target_beta):
  """
  Perform two-sided t test w.r.t a beta against the null hypothesis that it is
  zero for a voxel time course. Obtain p values for t value using its cdf.
  """
  s_sq, df = rse(X, Y, betas_hat)
  cov_matrix = npl.inv(X.T.dot(X))[0,0]
  sd_beta = np.sqrt(s_sq * cov_matrix)

  t_values = betas_hat[target_beta, :] / sd_beta
  p_values = 1 - np.array([t_distribution.cdf(i, df) for i in t_values])

  return p_values * 2
