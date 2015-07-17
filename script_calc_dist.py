#!/usr/bin/python
import os
import h5py
import sys
import numpy as np
import scipy.spatial.distance as dist
import pdb

def distance(batch_fn, dummy_matrix, dummy_fns, save_dir, process_id, top=50, save_fns = False):

    '''This funciton calculate the distance between the current batch with all the batches in the fea dir.
    '''
    batch = h5py.File(full_fn, 'r')
    batch_fea = np.squeeze(batch['fea'][:])
    d = dist.cdist(batch_fea, dummy_matrix)
    dist_inc = np.argsort(d)
    
    dist_fn = os.path.splitext(os.path.basename(batch_fn))[0] + '_dist.txt'
    dist_fn = os.path.join(save_dir, dist_fn)
    f = open(dist_fn, 'w')
    for i in xrange(dist_inc.shape[0]):
        dist_str = ' '.join([ str(ds) for ds in dist_inc[i,0:top]])
        f.write(dist_str + '\n')
    f.close()

    dist_inc = None
    save_fn = os.path.basename(batch_fn)
    save_fn = os.path.join(save_dir, str(save_fns) + '_' + str(process_id) + '_' + save_fn)
    f = h5py.File(save_fn, 'w')
    f.create_dataset('dist', data = d)
    if save_fns: # all the same process share the same copy of the fns.
        f.create_dataset('fns', data = dummy_fns)
    f.close()
    batch.close()
    print >> sys.stderr, 'Process ', process_id, 'done with', batch_fn

def total_images(h5py_dir):
    total_imgs = 0
    for root, subdir, fns in os.walk(h5py_dir):
        for fn in fns:
            full_fn = os.path.join(root, fn)
            batch = h5py.File(full_fn, 'r')
            total_imgs += batch['fea'][:].shape[0]
            batch.close()
    return total_imgs

if __name__ == '__main__':

    if len(sys.argv) < 5:
        print 'Usage: {0} <h5py_dir_1million> <h5py_dir_target> <process_id> <total_processes> [fea_len=1024]'.format(sys.argv[0])
        sys.exit()

    h5py_dir = sys.argv[1]
    h5py_dir_dst = sys.argv[2]

    process_id = int(sys.argv[3])
    process_num = int(sys.argv[4])
    fea_len = 1024
    if len(sys.argv) >= 6:
        fea_len = int(sys.argv[5])
    
    if h5py_dir_dst[-1] =='/':
        h5py_dir_dst = h5py_dir_dst[0:-1]
    save_dir = h5py_dir_dst + '_dist'
    if not os.path.isdir(save_dir):
        os.mkdir(save_dir)

    total_imgs = total_images(h5py_dir)
    dummy_fea = np.zeros((total_imgs,fea_len), dtype='float32')
    dummy_fns = []
    # now load all these features, this needed to be done for every process. 
    list_fns = []
    fea_idx = 0
    for root, sub_dir, fns in os.walk(h5py_dir):
        for fn in fns:
            full_fn = os.path.join(root, fn)
            list_fns.append(full_fn)
            batch = h5py.File(full_fn, 'r')
            fea = np.squeeze(batch['fea'][:])
            dummy_fea[fea_idx:fea_idx + fea.shape[0],:] = fea
            fns = batch['fns'][:]
            for i in xrange(fns.shape[0]):
                dummy_fns.append(fns[i])
            batch.close()
            fea_idx += fea.shape[0]
    save_fns = True
    for root, sub_dir, fns in os.walk(h5py_dir_dst):
        for fn in fns:
            ifn = os.path.splitext(fn)[0]
            idx = int(ifn.split('_')[-1])
            if not idx % process_num:
                # it's my job to do it. 
                full_fn = os.path.join(root, fn)
                distance(full_fn, dummy_fea, dummy_fns, save_dir, process_id, save_fns=save_fns)
                save_fns = False
