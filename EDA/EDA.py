"""sub011, task001_run_001"""
# library
import nibabel as nib
import numpy as np 
import diagnostics as diag
import matplotlib.pyplot as plt
import math

#functions
def events2neural(task_fname, tr, n_trs):
    """ Return predicted neural time course from event file `task_fname`

    Parameters
    ----------
    task_fname : str
        Filename of event file
    tr : float
        TR in seconds
    n_trs : int
        Number of TRs in functional run

    Returns
    -------
    time_course : array shape (n_trs,)
        Predicted neural time course, one value per TR
    """
    task = np.loadtxt(task_fname)
    # Check that the file is plausibly a task file
    if task.ndim != 2 or task.shape[1] != 3:
        raise ValueError("Is {0} really a task file?", task_fname)
    # Convert onset, duration seconds to TRs
    task[:, :2] = task[:, :2] / tr
    # Neural time course from onset, duration, amplitude for each event
    time_course = np.zeros(n_trs)
    for onset, duration, amplitude in task:
        time_course[onset:math.ceil(onset + duration)] = amplitude
    return time_course

def vol_std(data):
    """ Return standard deviation across voxels for 4D array `data`

    Parameters
    ----------
    data : 4D array
        4D array from FMRI run with last axis indexing volumes.  Call the shape
        of this array (M, N, P, T) where T is the number of volumes.

    Returns
    -------
    std_values : array shape (T,)
        One dimensonal array where ``std_values[i]`` gives the standard
        deviation of all voxels contained in ``data[..., i]``.
    """

    std_values=[]
    for i in range(0,data.shape[-1]):
        vol_1d = np.ravel(data[..., i])
        std_values.append(np.std(vol_1d))
    return std_values



def iqr_outliers(arr_1d, iqr_scale=1.5):
    """ Return indices of outliers identified by interquartile range

    Parameters
    ----------
    arr_1d : 1D array
        One-dimensional numpy array, from which we will identify outlier
        values.
    iqr_scale : float, optional
        Scaling for IQR to set low and high thresholds.  Low threshold is given
        by 25th centile value minus ``iqr_scale * IQR``, and high threshold id
        given by 75 centile value plus ``iqr_scale * IQR``.

    Returns
    -------
    outlier_indices : array
        Array containing indices in `arr_1d` that contain outlier values.
    lo_hi_thresh : tuple
        Tuple containing 2 values (low threshold, high thresold) as described
        above.
    """
    # Hint : np.lookfor('centile')
    # Hint : np.lookfor('nonzero')

    IQR = np.percentile(arr_1d,75) - np.percentile(arr_1d,25)
    low = np.percentile(arr_1d,25)-iqr_scale*IQR
    high = np.percentile(arr_1d,75)+iqr_scale*IQR
    outlier_indices=np.where((arr_1d<low)|(arr_1d>high))[0]
    lo_hi_thresh=(low,high)
    return (outlier_indices,lo_hi_thresh)


def vol_rms_diff(arr_4d):
    """ Return root mean square of differences between sequential volumes

    Parameters
    ----------
    data : 4D array
        4D array from FMRI run with last axis indexing volumes.  Call the shape
        of this array (M, N, P, T) where T is the number of volumes.

    Returns
    -------
    rms_values : array shape (T-1,)
        One dimensonal array where ``rms_values[i]`` gives the square root of
        the mean (across voxels) of the squared difference between volume i and
        volume i + 1.
    """

    rmsd_vals=[]
    for i in range(0,arr_4d.shape[-1]-1):
        diff_vol = arr_4d[..., i + 1] - arr_4d[..., i]
        rmsd = np.sqrt(np.mean(diff_vol ** 2))
        rmsd_vals.append(rmsd)
    return rmsd_vals

def extend_diff_outliers(diff_indices):
    """ Extend difference-based outlier indices `diff_indices` by pairing

    Parameters
    ----------
    diff_indices : array
        Array of indices of differences that have been detected as outliers.  A
        difference index of ``i`` refers to the difference between volume ``i``
        and volume ``i + 1``.

    Returns
    -------
    extended_indices : array
        Array where each index ``j`` in `diff_indices has been replaced by two
        indices, ``j`` and ``j+1``, unless ``j+1`` is present in
        ``diff_indices``.  For example, if the input was ``[3, 7, 8, 12, 20]``,
        ``[3, 4, 7, 8, 9, 12, 13, 20, 21]``.
    """

    extended_indices=[]
    for i in diff_indices:
        extended_indices.extend([i,i+1])
    return np.unique(extended_indices)

#loading data
img = nib.load('bold.nii.gz')
data = img.get_data() 
ds1=data.shape
#drop the first five
data = data[..., 5:]
ds2=data.shape
print("1.The original data shape is %r. After dropping the first five, now the data has the shape %r") %(str(ds1),str(ds2))
#standard deviations of all voxels along the TRs.
std = vol_std(data)
fobj = open('vol_std_values.txt', 'wt')
for i in std:
	fobj.write(str(i) + '\n')
fobj.close()
print("2. The standard deviations of all voxels along the TRs are saved in to 'vol_std_values.txt'")
#find the std outliers
outlier = iqr_outliers(std)[0]
fobj = open('vol_std_outliers.txt', 'wt')
for i in outlier:
	fobj.write(str(i) + '\n')
fobj.close()
print("3.There are %d std outliers, with indices %r. They are saved into 'vol_std_outliers.txt'") %(len(outlier),outlier)

#plot the std outliers
std_outlier=[]
low = iqr_outliers(std)[1][0]
high = iqr_outliers(std)[1][1]
for i in outlier:
	std_outlier.append(std[i])
x=np.arange(data.shape[-1])
std1, = plt.plot(x,std,'b',label="std values")
std2, = plt.plot(outlier,std_outlier,'ro',label="outliers")
lowbound = plt.axhline(y=low,color='r',ls='dashed',label='lower IRQ')
highbound = plt.axhline(y=high,color='g',ls='dashed',label='higher IRQ')
plt.legend(handles=[std1, std2, lowbound,highbound],loc=4)
plt.ylabel('standard deviation')
plt.xlabel('volumns')
plt.title('Outliers Detection')
plt.savefig('vol_std.png')
plt.show()
print("The std outliers is plotted and saved as 'vol_std.png'")
#RMS diffrence
rms = vol_rms_diff(data)
rms_outlier = iqr_outliers(rms)[0]
rms_outlier_value = []
for i in rms_outlier:
	rms_outlier_value.append(rms[i])
low_rms = iqr_outliers(rms)[1][0]
high_rms = iqr_outliers(rms)[1][1]
xx = np.arange(len(rms))
plt.axis([0,140,0,25])
rms1, = plt.plot(xx,rms,'b',label="rms values")
rms2, = plt.plot(rms_outlier,rms_outlier_value,'ro',label="rms outliers")
lowbound_rms = plt.axhline(y=low_rms,color='r',ls='dashed',label='lower IRQ')
highbound_rms = plt.axhline(y=high_rms,color='g',ls='dashed',label='higher IRQ')
plt.legend(handles=[rms1, rms2, lowbound_rms,highbound_rms],loc=1)
plt.ylabel('RMS difference')
plt.xlabel('indices')
plt.title('RMS difference outliers')
plt.savefig('vol_rms_outliers.png')
plt.show()
print("4.There are %d RMS outliers with indices %r.") %(len(rms_outlier),rms_outlier)
print("5.The RMS difference outliers is plotted and saved as 'vol_rms_outliers.png'")
#extended RMS outliers
ext_outlier = extend_diff_outliers(rms_outlier)
rms.append(0)
ext_outlier_value = []
for i in ext_outlier:
	ext_outlier_value.append(rms[i])
low_ext = iqr_outliers(rms)[1][0]
high_ext = iqr_outliers(rms)[1][1]
xxx = np.arange(len(rms))
plt.axis([0,140,0,25])
ext1, = plt.plot(xxx,rms,'b',label="rms values")
ext2, = plt.plot(ext_outlier,ext_outlier_value,'ro',label="extended outliers")
lowbound_ext = plt.axhline(y=low_ext,color='r',ls='dashed',label='lower IRQ')
highbound_ext = plt.axhline(y=high_ext,color='g',ls='dashed',label='higher IRQ')
plt.legend(handles=[ext1, ext2, lowbound_ext,highbound_ext],loc=1)
plt.ylabel('RMS difference')
plt.xlabel('volumns')
plt.title('Extended RMS difference outliers')
plt.savefig('extended_vol_rms_outliers.png')
plt.show()
fobj = open('extended_vol_rms_outliers.txt', 'wt')
for i in ext_outlier:
	fobj.write(str(i) + '\n')
fobj.close()
print("6.There are %d RMS exteded outliers with indices %r.They are saved into 'extended_vol_rms_outliers.txt'") %(len(ext_outlier),ext_outlier)
print("The RMS difference outliers is plotted and saved as'extended_vol_rms_outliers.png'")
#drop the outliers
rms = diag.vol_rms_diff(data)
rms_outlier = diag.iqr_outliers(rms)[0]
ext_outlier = diag.extend_diff_outliers(rms_outlier)
mask = np.ones(data.shape[-1])
mask[ext_outlier] = 0
mask = np.array(mask, dtype=bool)
data_rem=data[..., mask]
print("7.After dropping the extended RMS outliers, now the data has the shape %r.") %str(data_rem.shape)
 
#basic statistics
np.amin(data) #0
np.amax(data) #1550
np.mean(data) #137.08845107920848

#get the correlation matrix
TR = 2.5
n_trs = img.shape[-1]
time_course = events2neural('cond002.txt', 2.5, n_trs) 
plt.plot(time_course)
plt.title("time_course")
plt.savefig("time_course.png")
plt.show()
print("8.The time_course is plotted and saved as 'time_course.png'")
time_course=time_course[5:]
correlations = np.zeros(data.shape[:-1])
for i in range(data.shape[0]):
    for j in range(data.shape[1]):
        for k in range(data.shape[2]):
            vox_values = data[i, j, k]
            correlations[i, j, k] = np.corrcoef(time_course, vox_values)[1, 0]
plt.imshow(correlations[:, :, 18], cmap='gray')
plt.colorbar()
plt.savefig("correlation_middle.png")
plt.title("Middle slice of correlations")
plt.show()
print("9.The middle slice of the third axis from the correlations array is plotted and saved as 'correlation_middle.png'")




