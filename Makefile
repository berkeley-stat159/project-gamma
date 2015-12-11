.PHONY: all clean coverage test data analysis paper

all: clean

clean:
	find . -name "*.so" -o -name "*.pyc" -o -name "*.pyx.md5" | xargs rm -f

coverage:
	nosetests code/utils/tests data/tests --with-coverage --cover-package=code/utils/ --cover-package=data/

test:
	nosetests code/utils data

validate:
	python data/data.py

analysis:
	python code/linear_model.py
	python code/correlations_with_baselines.py
	python code/network_analysis.py
	python code/extended_rms_outliers.py
	python code/kmeans_analysis.py

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

	wget -P ./data http://openfmri.s3.amazonaws.com/tarballs/ds115_sub015-019.tgz
	tar -xvzf ./data/ds115_sub015-019.tgz

	wget -P ./data http://openfmri.s3.amazonaws.com/tarballs/ds115_sub006-009.tgz
	tar -xvzf ./data/ds115_sub006-009.tgz

	wget -P ./data http://openfmri.s3.amazonaws.com/tarballs/ds115_sub020-024.tgz
	tar -xvzf ./data/ds115_sub020-024.tgz

	wget -P ./data http://openfmri.s3.amazonaws.com/tarballs/ds115_sub030-034.tgz
	tar -xvzf ./data/ds115_sub030-034.tgz

	wget -P ./data http://openfmri.s3.amazonaws.com/tarballs/ds115_sub035-039.tgz
	tar -xvzf ./data/ds115_sub035-039.tgz

	wget -O ./data/sub012_task001_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub012/model/model001/task001_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/sub012_task002_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub012/model/model001/task002_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/sub012_task003_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub012/model/model001/task003_run001.feat/filtered_func_data_mni.nii.gz

	wget -O ./data/sub015_task001_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub015/model/model001/task001_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/sub015_task002_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub015/model/model001/task002_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/sub015_task003_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub015/model/model001/task003_run001.feat/filtered_func_data_mni.nii.gz

	wget -O ./data/sub035_task001_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub035/model/model001/task001_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/sub035_task002_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub035/model/model001/task002_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/sub035_task003_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub035/model/model001/task003_run001.feat/filtered_func_data_mni.nii.gz

	wget -O ./data/sub036_task001_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub036/model/model001/task001_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/sub036_task002_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub036/model/model001/task002_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/sub036_task003_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub036/model/model001/task003_run001.feat/filtered_func_data_mni.nii.gz

	wget -O ./data/sub037_task001_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub037/model/model001/task001_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/sub037_task002_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub037/model/model001/task002_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/sub037_task003_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub037/model/model001/task003_run001.feat/filtered_func_data_mni.nii.gz

	wget -O ./data/sub010_task001_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub010/model/model001/task001_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/sub010_task002_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub010/model/model001/task002_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/sub010_task003_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub010/model/model001/task003_run001.feat/filtered_func_data_mni.nii.gz

	wget -O ./data/sub013_task001_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub013/model/model001/task001_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/sub013_task002_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub013/model/model001/task002_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/sub013_task003_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub013/model/model001/task003_run001.feat/filtered_func_data_mni.nii.gz

	wget -O ./data/sub014_task001_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub014/model/model001/task001_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/sub014_task002_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub014/model/model001/task002_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/sub014_task003_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub014/model/model001/task003_run001.feat/filtered_func_data_mni.nii.gz

	wget -O ./data/sub021_task001_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub021/model/model001/task001_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/sub021_task002_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub021/model/model001/task002_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/sub021_task003_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub021/model/model001/task003_run001.feat/filtered_func_data_mni.nii.gz

	wget -O ./data/sub022_task001_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub022/model/model001/task001_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/sub022_task002_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub022/model/model001/task002_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/sub022_task003_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub022/model/model001/task003_run001.feat/filtered_func_data_mni.nii.gz

	wget -O ./data/sub038_task001_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub038/model/model001/task001_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/sub038_task002_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub038/model/model001/task002_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/sub038_task003_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub038/model/model001/task003_run001.feat/filtered_func_data_mni.nii.gz

	wget -O ./data/sub007_task001_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub007/model/model001/task001_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/sub007_task002_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub007/model/model001/task002_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/sub007_task003_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub007/model/model001/task003_run001.feat/filtered_func_data_mni.nii.gz

	wget -O ./data/sub009_task001_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub009/model/model001/task001_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/sub009_task002_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub009/model/model001/task002_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/sub009_task003_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub009/model/model001/task003_run001.feat/filtered_func_data_mni.nii.gz

	wget -O ./data/sub017_task001_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub017/model/model001/task001_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/sub017_task002_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub017/model/model001/task002_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/sub017_task003_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub017/model/model001/task003_run001.feat/filtered_func_data_mni.nii.gz

	wget -O ./data/sub031_task001_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub031/model/model001/task001_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/sub031_task002_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub031/model/model001/task002_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/sub031_task003_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub031/model/model001/task003_run001.feat/filtered_func_data_mni.nii.gz

	wget -O ./data/sub006_task001_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub006/model/model001/task001_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/sub006_task002_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub006/model/model001/task002_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/sub006_task003_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub006/model/model001/task003_run001.feat/filtered_func_data_mni.nii.gz

	wget -O ./data/sub008_task001_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub008/model/model001/task001_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/sub008_task002_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub008/model/model001/task002_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/sub008_task003_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub008/model/model001/task003_run001.feat/filtered_func_data_mni.nii.gz

	wget -O ./data/sub018_task001_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub018/model/model001/task001_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/sub018_task002_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub018/model/model001/task002_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/sub018_task003_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub018/model/model001/task003_run001.feat/filtered_func_data_mni.nii.gz

	wget -O ./data/sub024_task001_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub024/model/model001/task001_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/sub024_task002_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub024/model/model001/task002_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/sub024_task003_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub024/model/model001/task003_run001.feat/filtered_func_data_mni.nii.gz