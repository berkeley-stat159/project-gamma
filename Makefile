.PHONY: all clean coverage test data analysis paper conditionfiles

all: clean

clean:
	find . -name "*.so" -o -name "*.pyc" -o -name "*.pyx.md5" | xargs rm -f

coverage:
	nosetests code/utils/tests data/tests --with-coverage --cover-package=code/utils/ --cover-package=data/

test:
	nosetests code/utils data

paper:
	make clean -C paper
	make -C paper

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

conditionfiles:

	# condition files for the 20 subjects in the data section. The condition files are bundled
	# together with entire data packages on https://openfmri.org/dataset/ds000115.

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

data:

	# color map for plotting nice map

	wget -P ./data http://www.jarrodmillman.com/rcsds/_downloads/actc.txt

	# structural image of the brain

	wget -P ./data http://nipy.bic.berkeley.edu/rcsds/mni_icbm152_nlin_asym_09c_2mm/mni_icbm152_csf_tal_nlin_asym_09c_2mm.nii
	
	# 60 runs of BOLD images for 20 subjects

	wget -O ./data/preprocessed/sub011_task001_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub011/model/model001/task001_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/preprocessed/sub011_task002_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub011/model/model001/task002_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/preprocessed/sub011_task003_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub011/model/model001/task003_run001.feat/filtered_func_data_mni.nii.gz
	
	wget -O ./data/preprocessed/sub012_task001_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub012/model/model001/task001_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/preprocessed/sub012_task002_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub012/model/model001/task002_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/preprocessed/sub012_task003_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub012/model/model001/task003_run001.feat/filtered_func_data_mni.nii.gz

	wget -O ./data/preprocessed/sub015_task001_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub015/model/model001/task001_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/preprocessed/sub015_task002_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub015/model/model001/task002_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/preprocessed/sub015_task003_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub015/model/model001/task003_run001.feat/filtered_func_data_mni.nii.gz

	wget -O ./data/preprocessed/sub035_task001_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub035/model/model001/task001_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/preprocessed/sub035_task002_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub035/model/model001/task002_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/preprocessed/sub035_task003_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub035/model/model001/task003_run001.feat/filtered_func_data_mni.nii.gz

	wget -O ./data/preprocessed/sub036_task001_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub036/model/model001/task001_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/preprocessed/sub036_task002_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub036/model/model001/task002_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/preprocessed/sub036_task003_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub036/model/model001/task003_run001.feat/filtered_func_data_mni.nii.gz

	wget -O ./data/preprocessed/sub037_task001_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub037/model/model001/task001_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/preprocessed/sub037_task002_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub037/model/model001/task002_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/preprocessed/sub037_task003_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub037/model/model001/task003_run001.feat/filtered_func_data_mni.nii.gz

	wget -O ./data/preprocessed/sub010_task001_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub010/model/model001/task001_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/preprocessed/sub010_task002_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub010/model/model001/task002_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/preprocessed/sub010_task003_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub010/model/model001/task003_run001.feat/filtered_func_data_mni.nii.gz

	wget -O ./data/preprocessed/sub013_task001_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub013/model/model001/task001_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/preprocessed/sub013_task002_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub013/model/model001/task002_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/preprocessed/sub013_task003_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub013/model/model001/task003_run001.feat/filtered_func_data_mni.nii.gz

	wget -O ./data/preprocessed/sub014_task001_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub014/model/model001/task001_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/preprocessed/sub014_task002_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub014/model/model001/task002_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/preprocessed/sub014_task003_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub014/model/model001/task003_run001.feat/filtered_func_data_mni.nii.gz

	wget -O ./data/preprocessed/sub021_task001_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub021/model/model001/task001_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/preprocessed/sub021_task002_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub021/model/model001/task002_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/preprocessed/sub021_task003_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub021/model/model001/task003_run001.feat/filtered_func_data_mni.nii.gz

	wget -O ./data/preprocessed/sub022_task001_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub022/model/model001/task001_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/preprocessed/sub022_task002_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub022/model/model001/task002_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/preprocessed/sub022_task003_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub022/model/model001/task003_run001.feat/filtered_func_data_mni.nii.gz

	wget -O ./data/preprocessed/sub038_task001_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub038/model/model001/task001_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/preprocessed/sub038_task002_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub038/model/model001/task002_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/preprocessed/sub038_task003_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub038/model/model001/task003_run001.feat/filtered_func_data_mni.nii.gz

	wget -O ./data/preprocessed/sub007_task001_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub007/model/model001/task001_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/preprocessed/sub007_task002_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub007/model/model001/task002_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/preprocessed/sub007_task003_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub007/model/model001/task003_run001.feat/filtered_func_data_mni.nii.gz

	wget -O ./data/preprocessed/sub009_task001_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub009/model/model001/task001_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/preprocessed/sub009_task002_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub009/model/model001/task002_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/preprocessed/sub009_task003_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub009/model/model001/task003_run001.feat/filtered_func_data_mni.nii.gz

	wget -O ./data/preprocessed/sub017_task001_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub017/model/model001/task001_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/preprocessed/sub017_task002_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub017/model/model001/task002_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/preprocessed/sub017_task003_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub017/model/model001/task003_run001.feat/filtered_func_data_mni.nii.gz

	wget -O ./data/preprocessed/sub031_task001_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub031/model/model001/task001_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/preprocessed/sub031_task002_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub031/model/model001/task002_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/preprocessed/sub031_task003_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub031/model/model001/task003_run001.feat/filtered_func_data_mni.nii.gz

	wget -O ./data/preprocessed/sub006_task001_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub006/model/model001/task001_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/preprocessed/sub006_task002_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub006/model/model001/task002_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/preprocessed/sub006_task003_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub006/model/model001/task003_run001.feat/filtered_func_data_mni.nii.gz

	wget -O ./data/preprocessed/sub008_task001_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub008/model/model001/task001_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/preprocessed/sub008_task002_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub008/model/model001/task002_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/preprocessed/sub008_task003_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub008/model/model001/task003_run001.feat/filtered_func_data_mni.nii.gz

	wget -O ./data/preprocessed/sub018_task001_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub018/model/model001/task001_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/preprocessed/sub018_task002_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub018/model/model001/task002_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/preprocessed/sub018_task003_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub018/model/model001/task003_run001.feat/filtered_func_data_mni.nii.gz

	wget -O ./data/preprocessed/sub024_task001_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub024/model/model001/task001_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/preprocessed/sub024_task002_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub024/model/model001/task002_run001.feat/filtered_func_data_mni.nii.gz
	wget -O ./data/preprocessed/sub024_task003_run001_func_data_mni.nii.gz http://nipy.bic.berkeley.edu/rcsds/ds115/sub024/model/model001/task003_run001.feat/filtered_func_data_mni.nii.gz