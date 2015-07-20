#!/usr/bin/python

import os
import sys
import h5py
import pdb


if __name__ == '__main__':

    if len(sys.argv) < 5:
        print 'Usage: {0} <SBU_caption> <SBU_url> <dist_h5py_dir><vocab_dict.txt>'.format(sys.argv[0])
        sys.exit()

    sbu_cap = sys.argv[1]
    sbu_url = sys.argv[2]
    dist_dir = sys.argv[3]
    vocab = sys.argv[4]

    sbu_img2dict = {}
    with open(sbu_url,'r') as fid_url:
        with open(sub_cap,'r') as fid_cap:
            for url,cap in zip(fid_url, fid_cap):
                url = url.strip()
                cap = cap.strip()
                sbu_img2dict[url] = cap

