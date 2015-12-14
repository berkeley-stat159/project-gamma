"""
Wrapper for normality testing using multiple methods for comparison of results.

Procedures are as follows.

Bonferroni procedure:
reject the null if p < alpha/n where n is the sample size

Hochberg's set up:
1. Order the p-values P(1),P(2),...,P(n) and their associated hypothesis H(1),...,H(n)
2. Reject all hypotheses H(k) having P(k) <= alpha/(n+1-k) where k=1,...,n

Benjamini-Hochberg procedure:
1. Order the p-values P(1),P(2),...,P(n) and their associated hypothesis H(1),...,H(n)
2. Reject all hypotheses H(k) having P(k) <= (k/n)*alpha where k=1,...,n

"""

from scipy import stats
import numpy as np

def multiple_comp (residuals): 
  """
  Parameters
  ----------
  Residuals: 2d array (voxels,timecourse)

  Returns
  -------

  A list of the number of voxels that being tested as not normally distributed, based on 
  alpha-test, Bonferroni procedure, Hochberg procedure and  Benjamini-Hochberg procedure 
  respectively
  """

  # Alpha Test
  p_nor = []
  for i in range(0,residuals.shape[0]):
      p_nor.append(stats.shapiro(residuals[i,:])[1])

  # for p<0.05, the voxel is not normal distributed
  p_nor_005 = [i for i in p_nor if i < 0.05]

  # Bonferroni Procedure
  p_bonf = [i for i in p_nor if i < (0.05 / residuals.shape[0])]

  # Hochberg Procedure
  p_nors = np.sort(p_nor)
  alpha = 0.05
  n=len(p_nors)
  tf=[]
  for i in range(0,n):
      thres = alpha/(n+1-(i+1))
      tf.append(p_nors[i]<=thres)

  # Benjamini-Hochberg procedure
  tf_bh=[]
  for i in range(0,len(p_nors)):
      thres = (i/n)*alpha
      tf_bh.append(p_nors[i]<=thres)

  return [len(p_nor_005),len(p_bonf),sum(tf),sum(tf_bh)]







