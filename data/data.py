from __future__ import print_function, division

import hashlib
import os

cur_filepath = os.path.dirname(__file__)

d = {os.path.join(cur_filepath, "actc.txt"): '1f7101556e2f491a71155e1aed6f823c',
     os.path.join(cur_filepath, 'mni_icbm152_csf_tal_nlin_asym_09c_2mm.nii'): 'fb5d52b1162dcf111e2a9b3825c030ae',
     os.path.join(cur_filepath, 'net_roi.txt'): '6c9f140748de388d842cf9ab9ccadc71',
     os.path.join(cur_filepath, 'preprocessed/sub006_task001_run001_func_data_mni.nii.gz'): '441387111f5515496659d84cd33c11e5',
     os.path.join(cur_filepath, 'preprocessed/sub006_task002_run001_func_data_mni.nii.gz'): 'c6052b42bb8ce4b7bd2ac666273d6029',
     os.path.join(cur_filepath, 'preprocessed/sub006_task003_run001_func_data_mni.nii.gz'): 'ffe7c5a9cfee6345721359e094f7853c',
     os.path.join(cur_filepath, 'preprocessed/sub007_task001_run001_func_data_mni.nii.gz'): 'cec2925b81ec5dd6c0b6d4ce1ffdc109',
     os.path.join(cur_filepath, 'preprocessed/sub007_task002_run001_func_data_mni.nii.gz'): '1dc9bce616bbf3dc8561e70ea61f7831',
     os.path.join(cur_filepath, 'preprocessed/sub007_task003_run001_func_data_mni.nii.gz'): 'ee5e23c6444c97ea4a3d74b9f9543b0d',
     os.path.join(cur_filepath, 'preprocessed/sub008_task001_run001_func_data_mni.nii.gz'): '2968eae5657e9687f5cc0a74b7482ce5',
     os.path.join(cur_filepath, 'preprocessed/sub008_task002_run001_func_data_mni.nii.gz'): 'ac54e557aad65cc4eef8d15c21babfa5',
     os.path.join(cur_filepath, 'preprocessed/sub008_task003_run001_func_data_mni.nii.gz'): '1676f6188aa182134785bc5f6a336336',
     os.path.join(cur_filepath, 'preprocessed/sub009_task001_run001_func_data_mni.nii.gz'): '3ec468715a1d6fb6e32b44dae212e120',
     os.path.join(cur_filepath, 'preprocessed/sub009_task002_run001_func_data_mni.nii.gz'): 'f4e5ccccfcadf05238c13ccd9da7bcf6',
     os.path.join(cur_filepath, 'preprocessed/sub009_task003_run001_func_data_mni.nii.gz'): '3f2ff2fc9ba74b2aa083594905763d78',
     os.path.join(cur_filepath, 'preprocessed/sub010_task001_run001_func_data_mni.nii.gz'): '2c846fb6c10d17fab874202d928d3d40',
     os.path.join(cur_filepath, 'preprocessed/sub010_task002_run001_func_data_mni.nii.gz'): '69f3d3278279b3816fc50474bcceee77',
     os.path.join(cur_filepath, 'preprocessed/sub010_task003_run001_func_data_mni.nii.gz'): '89674c433a30db53b8818e61450402e9',
     os.path.join(cur_filepath, 'preprocessed/sub011_task001_run001_func_data_mni.nii.gz'): '50abdd2cc179fb8cca27977ff4ba0e8e',
     os.path.join(cur_filepath, 'preprocessed/sub011_task002_run001_func_data_mni.nii.gz'): '6aedb4dc502fc45f786f089b1ab77dd8',
     os.path.join(cur_filepath, 'preprocessed/sub011_task003_run001_func_data_mni.nii.gz'): '21ec3f73afe425126ccd74fb3385fbff',
     os.path.join(cur_filepath, 'preprocessed/sub012_task001_run001_func_data_mni.nii.gz'): '456b4faf30c18638b4b1e7fb5d47f228',
     os.path.join(cur_filepath, 'preprocessed/sub012_task002_run001_func_data_mni.nii.gz'): 'bd4c4be29552efa3c4976e81c71c2aef',
     os.path.join(cur_filepath, 'preprocessed/sub012_task003_run001_func_data_mni.nii.gz'): 'b5bd9f6e0ccb445870cb15f2e0a4fc90',
     os.path.join(cur_filepath, 'preprocessed/sub013_task001_run001_func_data_mni.nii.gz'): '9a606783bec9983f46e441844123a910',
     os.path.join(cur_filepath, 'preprocessed/sub013_task002_run001_func_data_mni.nii.gz'): 'a6805fb95d69988c3b420cc1d39cacd3',
     os.path.join(cur_filepath, 'preprocessed/sub013_task003_run001_func_data_mni.nii.gz'): '57f8d74ce6899a96ade6c1323731b34e',
     os.path.join(cur_filepath, 'preprocessed/sub014_task001_run001_func_data_mni.nii.gz'): 'ef1b9eed555f0a9104dd7851c1f0c99d',
     os.path.join(cur_filepath, 'preprocessed/sub014_task002_run001_func_data_mni.nii.gz'): 'bda6f6e42a88f8120837e7a6f0ae2853',
     os.path.join(cur_filepath, 'preprocessed/sub014_task003_run001_func_data_mni.nii.gz'): 'd8773953d1eb249fdea6a37f3c22b4f7',
     os.path.join(cur_filepath, 'preprocessed/sub015_task001_run001_func_data_mni.nii.gz'): '3b16886920c4c1f14d89bcb0d0c8d579',
     os.path.join(cur_filepath, 'preprocessed/sub015_task002_run001_func_data_mni.nii.gz'): 'd72007f4b99375a485124c39b03b9112',
     os.path.join(cur_filepath, 'preprocessed/sub015_task003_run001_func_data_mni.nii.gz'): 'dd9c9c994a418ab3bc0d1a3c2e24d399',
     os.path.join(cur_filepath, 'preprocessed/sub017_task001_run001_func_data_mni.nii.gz'): 'dfbd5d7d1b5b623d2e038c88b93ff1ec',
     os.path.join(cur_filepath, 'preprocessed/sub017_task002_run001_func_data_mni.nii.gz'): 'ff87ea03543f64623e442dc20f2b8d9c',
     os.path.join(cur_filepath, 'preprocessed/sub017_task003_run001_func_data_mni.nii.gz'): 'db9ffed2bdcffae578b85e7a5fac0518',
     os.path.join(cur_filepath, 'preprocessed/sub018_task001_run001_func_data_mni.nii.gz'): 'b95b47e7e2deb54ebe195ca4ea2aac77',
     os.path.join(cur_filepath, 'preprocessed/sub018_task002_run001_func_data_mni.nii.gz'): '5f7a3e2477359e797734646b0f999448',
     os.path.join(cur_filepath, 'preprocessed/sub018_task003_run001_func_data_mni.nii.gz'): 'b0c9e24359252eca4a25f18e6576315a',
     os.path.join(cur_filepath, 'preprocessed/sub021_task001_run001_func_data_mni.nii.gz'): 'dbd8d23c625cc5b6a4d40b7ffa74cead',
     os.path.join(cur_filepath, 'preprocessed/sub021_task002_run001_func_data_mni.nii.gz'): '1a8fc6ebd164b0fd5bb6d9c5eeacc7c9',
     os.path.join(cur_filepath, 'preprocessed/sub021_task003_run001_func_data_mni.nii.gz'): '3cadc166681ac17475987d745278e70f',
     os.path.join(cur_filepath, 'preprocessed/sub022_task001_run001_func_data_mni.nii.gz'): '222b5a9fce2b5fa3dc8bf638a64645ee',
     os.path.join(cur_filepath, 'preprocessed/sub022_task002_run001_func_data_mni.nii.gz'): 'd721035ff7f2790e66e2193a3b92441c',
     os.path.join(cur_filepath, 'preprocessed/sub022_task003_run001_func_data_mni.nii.gz'): '40ab5f2da3bbc627aec46fdfad464ce2',
     os.path.join(cur_filepath, 'preprocessed/sub024_task001_run001_func_data_mni.nii.gz'): 'a8538f72c61afb00ebc512cc4c5787a8',
     os.path.join(cur_filepath, 'preprocessed/sub024_task002_run001_func_data_mni.nii.gz'): 'a78db60610f2aa7bfa30e7d9bc6a6bc0',
     os.path.join(cur_filepath, 'preprocessed/sub024_task003_run001_func_data_mni.nii.gz'): '57f0b956bea95c347ac1d42e433aea5c',
     os.path.join(cur_filepath, 'preprocessed/sub031_task001_run001_func_data_mni.nii.gz'): '5a86aaea7941018fd6de7ef12b043dcc',
     os.path.join(cur_filepath, 'preprocessed/sub031_task002_run001_func_data_mni.nii.gz'): 'bca69af16e250ca2d4cf90c54b212cba',
     os.path.join(cur_filepath, 'preprocessed/sub031_task003_run001_func_data_mni.nii.gz'): '4ef57cf672f8186aebfb3f4e335e8c16',
     os.path.join(cur_filepath, 'preprocessed/sub035_task001_run001_func_data_mni.nii.gz'): '2a0b87fe162b561ccbef7834473f5704',
     os.path.join(cur_filepath, 'preprocessed/sub035_task002_run001_func_data_mni.nii.gz'): '5cedca07b6c47feb2e94c08ee70f42c1',
     os.path.join(cur_filepath, 'preprocessed/sub035_task003_run001_func_data_mni.nii.gz'): '1267c2adadf99c51880c20127678a935',
     os.path.join(cur_filepath, 'preprocessed/sub036_task001_run001_func_data_mni.nii.gz'): '9b60d067be17fa3414958bb49c5f6cf1',
     os.path.join(cur_filepath, 'preprocessed/sub036_task002_run001_func_data_mni.nii.gz'): 'd4594fe2413bc3dc21d2f56e9a9eef88',
     os.path.join(cur_filepath, 'preprocessed/sub036_task003_run001_func_data_mni.nii.gz'): 'e322517593fa3002d5137d072c297337',
     os.path.join(cur_filepath, 'preprocessed/sub037_task001_run001_func_data_mni.nii.gz'): 'f3dd8b992ae3d6bbfdd1d6a1b11e998c',
     os.path.join(cur_filepath, 'preprocessed/sub037_task002_run001_func_data_mni.nii.gz'): 'c700278821bc57196caee5ab34adde62',
     os.path.join(cur_filepath, 'preprocessed/sub037_task003_run001_func_data_mni.nii.gz'): 'cb46603f0ec136390abeef0471024bb1',
     os.path.join(cur_filepath, 'preprocessed/sub038_task001_run001_func_data_mni.nii.gz'): '5e5b4bdf001dc07cd1a2cff443e2541a',
     os.path.join(cur_filepath, 'preprocessed/sub038_task002_run001_func_data_mni.nii.gz'): 'e0855bcb0dc770d4d2e85bff4b733f07',
     os.path.join(cur_filepath, 'preprocessed/sub038_task003_run001_func_data_mni.nii.gz'): 'f609aa31e1d630f97f5af801a9824074'}


def generate_file_md5(filename, blocksize=2**20):
    m = hashlib.md5()
    with open(filename, "rb") as f:
        while True:
            buf = f.read(blocksize)
            if not buf:
                break
            m.update(buf)
    return m.hexdigest()


def check_hashes(d):
    all_good = True
    for k, v in d.items():
        digest = generate_file_md5(k)
        if v == digest:
            print("The file {0} has the correct hash.".format(k))
        else:
            print("ERROR: The file {0} has the WRONG hash!".format(k))
            all_good = False
    return all_good


if __name__ == "__main__":
    check_hashes(d)
