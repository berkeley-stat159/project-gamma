from __future__ import print_function, division

import hashlib
import os


d = {os.path.join(os.path.dirname(__file__), "actc.txt"): '1f7101556e2f491a71155e1aed6f823c',
     os.path.join(os.path.dirname(__file__), 'mni_icbm152_csf_tal_nlin_asym_09c_2mm.nii'): 'fb5d52b1162dcf111e2a9b3825c030ae',
     os.path.join(os.path.dirname(__file__), 'sub011_task001_run001_func_data_mni.nii'): '50abdd2cc179fb8cca27977ff4ba0e8e',
     os.path.join(os.path.dirname(__file__), 'sub011_task002_run001_func_data_mni.nii'): '6aedb4dc502fc45f786f089b1ab77dd8',
     os.path.join(os.path.dirname(__file__), 'sub011_task003_run001_func_data_mni.nii'): '21ec3f73afe425126ccd74fb3385fbff',
     os.path.join(os.path.dirname(__file__), 'net_roi.txt'): '6c9f140748de388d842cf9ab9ccadc71'}


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
