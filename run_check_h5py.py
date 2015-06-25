#!/usr/bin/python

import h5py
import sys
import pdb

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'Usage: {0} <h5py.h5>'.format(sys.argv[0])
        sys.exit()
    fn = h5py.File(sys.argv[1],'r')

    pdb.set_trace()
    print fn.keys()


