import numpy as np

#I treat the second colunm in cond002 as time directly
#maybe checked later

def events2neural(task_fname, time_unit, n_trs):
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
    task[:, :2] = task[:, :2] / time_unit
    #print task
    task[:,1] = np.round(task[:,1])
    # Neural time course from onset, duration, amplitude for each event
    time_course = np.zeros(n_trs*2.5/time_unit)
    for onset, duration, amplitude in task:
        # print onset
        # print duration
        # print amplitude
        time_course[onset:onset + duration] = amplitude
    return time_course