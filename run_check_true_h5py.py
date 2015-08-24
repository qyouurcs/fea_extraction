#!/usr/bin/python

import h5py
import sys
import pdb
import glob
import os

if __name__ == '__main__':
    # check the consistency between different h5py file. 
    if len(sys.argv) < 2:
        print 'Usage: {0} <h5py.dir>'.format(sys.argv[0])
        sys.exit()
    src_dir = sys.argv[1]
    h5pys = glob.glob( os.path.join(src_dir, 'True*'))

    for fn in h5pys:
        fn = h5py.File(sys.argv[1],'r')

        pdb.set_trace()
        print fn.keys()


