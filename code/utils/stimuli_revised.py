"""
Different versions of the events2neural function. All are
needed to deal with different condition file formats and 
specific needs of callers, such as handling the possibility
of an empty but legal error condition file and retrieving
the convolved time course at different resolution.
"""


from __future__ import division
import numpy as np
import math

def events2neural_target_non_target(task_fname, error_fname, n_trs, tr_divs, TR = 2.5):
    task = np.loadtxt(task_fname)
    # Check that the file is plausibly a task file
    if task.ndim != 2 or task.shape[1] != 3:
        raise ValueError("Is {0} really a task file?", task_fname)

    # parse target intensity and non-target intensity
    target_intensity, nontarget_intensity = max(set(task[:,2])), min(set(task[:,2]))
    target_task = task[task[:,2] == target_intensity]
    target_task[:,2] = 1.0
    nontarget_task = task[task[:,2] == nontarget_intensity]
    nontarget_task[:,2] = 1.0

    # if there are any errors, treat them as targets
    task_errors = np.loadtxt(error_fname)

    task_errors = task_errors.reshape((-1, 3))
    task_errors[:,2] = 1.0

    res = []
    for cond_data in (target_task, nontarget_task, task_errors):
        onsets_seconds = cond_data[:, 0]
        duration_seconds = cond_data[:, 1]
        amplitudes = cond_data[:, 2]
        onsets_in_scans = onsets_seconds / TR
        high_res_times = np.arange(0, n_trs, 1 / tr_divs) * TR
        high_res_neural = np.zeros(high_res_times.shape)
        high_res_onset_indices = onsets_in_scans * tr_divs
        high_res_durations = duration_seconds / TR * tr_divs
        for hr_onset, hr_duration, amplitude in zip(high_res_onset_indices, high_res_durations, amplitudes):
            if hr_duration == 0: continue
            hr_onset = int(round(hr_onset))
            hr_duration = int(round(hr_duration))
            high_res_neural[hr_onset:hr_onset + hr_duration] = amplitude
        res.append(high_res_neural)

    target_neural, nontarget_neural, error_neural = res

    return target_neural, nontarget_neural, error_neural


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

def events2neural_std(task_fname, tr, n_trs):
    return events2neural_rounded(task_fname, tr, n_trs)

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