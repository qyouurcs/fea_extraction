#!/usr/bin/python
import os
import h5py
import sys
import pdb
import glob

if __name__ == '__main__':
    # check the consistency between different h5py file. 
    if len(sys.argv) < 2:
        print 'Usage: {0} <h5py.dir>'.format(sys.argv[0])
        sys.exit()
    src_dir = sys.argv[1]
    h5pys = glob.glob( os.path.join(src_dir, 'True*'))

    fns_a = None

    for fn in h5pys:
        print 'loading', fn
        fid = h5py.File(fn, 'r')
        fns = fid['fns'][:]
        if fns_a is None:
            fns_a = fns
        else:
            for a,b in zip(fns_a, fns):
                pdb.set_trace()
                if a != b:
                    print a
                    print b
                    sys.exit()
    print 'Done, they are all the same'

    
