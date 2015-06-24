import sys
import pdb
import os
import argparse
import numpy as np
from scipy.misc import imread, imresize
import cPickle as pickle
import h5py

def predict(in_data, net, layer='fc7'):
    """
    Get the features for a batch of data using network

    Inputs:
    in_data: data batch
    """
    out = net.forward(**{net.inputs[0]: in_data})
    features = net.blobs[layer].data
    return features


def batch_predict(filenames, net):
    """
    Get the features for all images from filenames using a network

    Inputs:
    filenames: a list of names of image files

    Returns:
    an array of feature vectors for the images in that file
    """
    layer = args.layer
    N, C, H, W = net.blobs[net.inputs[0]].data.shape
    F = net.blobs[net.outputs[0]].data.shape[1]
    Nf = len(filenames)
    batch_idx = 0
    pdb.set_trace()
    for i in range(0, Nf, N):
        in_data = np.zeros((N, C, H, W), dtype=np.float32)

        batch_range = range(i, min(i+N, Nf))
        batch_fns = [filenames[j] for j in batch_range]
        Nb = len(batch_range)

        batch_images = np.zeros((Nb, 3, H, W))
        for j,fname in enumerate(batch_fns):
            im = imread(fname)
            if len(im.shape) == 2:
                im = np.tile(im[:,:,np.newaxis], (1,1,3))
            # RGB -> BGR
            im = im[:,:,(2,1,0)]
            # mean subtraction
            im = im - np.array([103.939, 116.779, 123.68])
            # resize
            im = imresize(im, (H, W))
            # get channel in correct dimension
            im = np.transpose(im, (2, 0, 1))
            batch_images[j,:,:,:] = im
            print fname

        # insert into correct place
        in_data[0:len(batch_range), :, :, :] = batch_images

        feas = predict(in_data, net,layer)
        # predict features
        save_fn = os.path.join(args.out, 'batch_{0}.h5'.format(batch_idx))
        f = h5py.File(save_fn,'w')
        f.create_dataset('fea', data = feas)
        f.create_dataset('fns', data = batch_fns)
        f.create_dataset('batch_idx', data = batch_idx)
        f.close()
        batch_idx += 1
        print 'Done with batch {0}'.format(save_fn)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--caffe',
                        help='path to caffe installation')
    parser.add_argument('--model_def',
                        help='path to model definition prototxt')
    parser.add_argument('--model',
                        help='path to model parameters')
    parser.add_argument('--layer',default='fc7', help='batch_size')
    parser.add_argument('--dir',
                        help='path to a directory contsining a list of images')
    parser.add_argument('--gpu',
                        action='store_true',
                        help='whether to use gpu training')
    parser.add_argument('--out',
                        help='name of the directory to store the features')
    
    args = parser.parse_args()
    
    if args.caffe is None or args.model is None or args.model_def is None or args.out is None:
        parser.print_help()
        sys.exit()
    
    
    caffepath = args.caffe + '/python'
    sys.path.append(caffepath)
    
    import caffe

    if args.gpu:
        caffe.set_mode_gpu()
    else:
        caffe.set_mode_cpu()
    
    net = caffe.Net(args.model_def, args.model, caffe.TEST)
    
    filenames = []
    
    for root, dirs, fns in os.walk(args.dir):
        for fn in fns:
            filenames.append(os.path.join(root, fn))
    
    batch_predict(filenames, net)
    
