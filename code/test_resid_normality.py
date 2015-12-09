import numpy as np 
from scipy import stats
residuals = np.load("/Users/Xinyue_star/Desktop/Final_Proj/project-gamma/data/lm_residuals.npy")
p_nor = []
for i in range(residuals.shape[0]):
    p_nor.append(stats.shapiro(residuals[i,:])[1])
len(p_nor)
#for p<0.05, the voxel is not normal distributed
p_nor_005 = [i for i in p_nor if i < 0.05]
len(p_nor_005)
print("12.Before removing the outliers, there are %d voxels out of %d are not normally distributed." % (len(p_nor_005),len(p_nor)))

"""
Bonferroni procedure:
reject the null if p < alpha/n where n is the sample size
"""
p_bonf = [i for i in p_nor if i < 0.05/data.shape[-1]]
print("15.With Bonferroni correction, there are %d voxels out of %d are not normally distributed." % (len(p_bonf),len(p_nor)))

"""
Hochberg's set up:
1. Order the p-values P(1),P(2),...,P(n) and their associated hypothesis H(1),...,H(n)
2. Reject all hypotheses H(k) having P(k) <= alpha/(n+1-k) where k=1,...,n
"""

p_nors = np.sort(p_nor)
alpha = 0.05
n=len(p_nors)
tf=[]
for i in range(0,len(p_nors)):
    thres = alpha/(n+1-(i+1))
    tf.append(p_nors[i]<=thres)
print("17.With Hochberg's procedure, there are %d voxels out of %d are not normally distributed." %(sum(tf),len(p_nors)))


""""
Benjamini-Hochberg procedure:
1. Order the p-values P(1),P(2),...,P(n) and their associated hypothesis H(1),...,H(n)
2. Reject all hypotheses H(k) having P(k) <= (k/n)*alpha where k=1,...,n
"""
tf=[]
for i in range(0,len(p_nors)):
    thres = (i/n)*alpha
    tf.append(p_nors[i]<=thres)
print("18.With Benjamini-Hochberg's procedure, there are %d voxels out of %d are not normally distributed." %(sum(tf),len(p_nors)))












