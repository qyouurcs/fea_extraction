#!/usr/bin/python
import os
import h5py
import sys
import pdb
import glob

if __name__ == '__main__':
    # check the consistency between different h5py file. 
    if len(sys.argv) < 3:
        print 'Usage: {0} <h5py_fea_dir> <h5py_fea_dir_dist>'.format(sys.argv[0])
        sys.exit()
    src_dir = sys.argv[2]
    h5pys = glob.glob( os.path.join(src_dir, 'True*'))

    fns_a = None

    for fn in h5pys:
        print 'loading targeted fns from', fn
        fid = h5py.File(fn, 'r')
        fns = fid['fns'][:]
        fns_a = fns
        break
    if sys.argv[2][-1] == '/':
        save_base = sys.argv[2][0:-1]
    else:
        save_base = sys.argv[2]

    save_fn = os.path.basename(save_base) + '_mapping_fns.txt' 
    with open(save_fn,'w') as fid:
        for root, subdirs, fns in os.walk(sys.argv[1], 'r'):
            for fn in fns:
                print 'Processing', fn
                full_fn = os.path.join(root, fn)
                h5fid = h5py.File(full_fn,'r')
                fns = h5fid['fns'][:]
                h5fid.close()

                dist_fn = os.path.splitext(fn)[0]
                dist_fn = os.path.join(sys.argv[2], dist_fn + '_dist.txt')
                with open(dist_fn, 'r') as rfid:
                    for src_fn, dist_idx in zip(fns, rfid):
                        dist_idx = dist_idx.strip().split()
                        dist_idx = [ int(idx) for idx in dist_idx ]
                        print >>fid, src_fn, ' '.join(fns_a[dist_idx])
                    
    print 'Done with', save_fn
