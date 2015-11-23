from urllib import urlretrieve

for sub in range(20, 103):
  if len(str(sub)) == 1:
    sub_str = "00" + str(sub) 
  elif len(str(sub)) == 2:
    sub_str = "0" + str(sub) 
  else:
    sub_str = str(sub)
  for task_str in ("001", "002", "003"):
    urlretrieve("http://nipy.bic.berkeley.edu/rcsds/ds115/sub%s/model/model001/task%s_run001.feat/filtered_func_data_mni.nii.gz" % (sub_str, task_str), "/Users/fenglin/Desktop/stat159/fmri_processed/sub%s_task%s_run001_func_data_mni.nii.gz" % (sub_str, task_str))