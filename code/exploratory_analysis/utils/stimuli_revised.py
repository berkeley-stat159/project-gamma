import numpy as np
import math

def events2neural(task_fname, time_unit, n_trs, TR = 2.5):
    """ 
    Return predicted neural time course from event file `task_fname`,
    scaled to the appropriate TIME_UNIT

    Parameters
    ----------
    task_fname : str
        Filename of event file
    tr : float
        TR in seconds
    n_trs : int
        Number of TRs in functional run
    TR: time span a nii array measurement corresponds to

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
    task[:, :2] = task[:, :2] / time_unit
    task[:,1] = np.round(task[:,1])
    # Neural time course from onset, duration, amplitude for each event
    time_course = np.zeros(int(n_trs*TR/time_unit))
    for onset, duration, amplitude in task:
        time_course[int(onset):int(onset + duration)] = amplitude
    return time_course


def events2neural_rounded(task_fname, tr, n_trs):
    """ Return predicted neural time course from event file `task_fname`

    This method is different from events2neural in that it has a fixed time
    unit of 1 second and force round-up of durations less than 1 second

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
        time_course[int(onset):int(math.ceil(onset + duration))] = amplitude
    return time_course