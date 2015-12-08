.PHONY: all clean coverage test data analysis paper

all: clean

clean:
	find . -name "*.so" -o -name "*.pyc" -o -name "*.pyx.md5" | xargs rm -f

coverage:
	nosetests code/utils data --with-coverage --cover-package=data  --cover-package=utils

test:
	nosetests code/utils data

verbose:
	nosetests -v code/utils data

data:
	wget -P ./data http://www.jarrodmillman.com/rcsds/_downloads/actc.txt
	wget -P ./data http://nipy.bic.berkeley.edu/rcsds/mni_icbm152_nlin_asym_09c_2mm/mni_icbm152_csf_tal_nlin_asym_09c_2mm.nii
	wget -O ./data/sub011_task001_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub011/model/model001/task001_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/sub011_task002_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub011/model/model001/task002_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/sub011_task003_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub011/model/model001/task003_run001.feat/filtered_func_data_mni.nii.gz
	wget -P ./data http://openfmri.s3.amazonaws.com/tarballs/ds115_sub010-014.tgz
	tar -xvzf ./data/ds115_sub010-014.tgz

validate:
	python data/data.py

analysis:
	python code/linear_model.py
	python code/correlations_with_baselines.py
	python code/network_analysis.py
	python code/extended_rms_outliers.py
	python code/kmeans_analysis.py

