import sys
import pdb
import os
import argparse
import numpy as np
from scipy.misc import imread, imresize
import cPickle as pickle
import h5py
from scandir import scandir, walk


def predict(in_data, net, layer='fc7'):
    """
    Get the features for a batch of data using network

    Inputs:
    in_data: data batch
    """
    out = net.forward(**{net.inputs[0]: in_data})
    features = net.blobs[layer].data
    return features


def batch_predict(filenames, net, layer, batch_idx):
    """
    Get the features for all images from filenames using a network

    Inputs:
    filenames: a list of names of image files

    Returns:
    an array of feature vectors for the images in that file
    """
    N, C, H, W = net.blobs[net.inputs[0]].data.shape
    F = net.blobs[net.outputs[0]].data.shape[1]
    Nf = len(filenames)
    #batch_idx = 0
    for i in range(0, Nf, N):
        in_data = np.zeros((N, C, H, W), dtype=np.float32)

        batch_range = range(i, min(i + N, Nf))
        batch_fns_s = []
        batch_fns = [filenames[j] for j in batch_range]
        Nb = len(batch_range)
        idx = 0

        batch_images = np.zeros((Nb, 3, H, W))
        for j, fname in enumerate(batch_fns):
            try:
                im = imread(fname)
            except:
                print >> sys.stderr, fname
                continue

            if len(im.shape) == 2:
                im = np.tile(im[:, :, np.newaxis], (1, 1, 3))
            # RGB -> BGR
            if len(im.shape) == 4:
                print >> sys.stderr, fname
                im = im[:,:,0:3]
            try:
                # one of the train image is really stupidly wrong. 
                # just ignore it.
                im = im[:, :, (2, 1, 0)]
            except:
                print >> sys.stderr, fname, 'im[:,:,(2,1,0)]'
                continue
            # mean subtraction
            im = im - np.array([103.939, 116.779, 123.68])
            # resize
            im = imresize(im, (H, W))
            # get channel in correct dimension
            im = np.transpose(im, (2, 0, 1))
            batch_images[idx, :, :, :] = im
            batch_fns_s.append(fname)
            idx += 1
            # print fname

        # insert into correct place
        in_data[0:idx, :, :, :] = batch_images[0:idx,:,:,:]

        feas = predict(in_data, net, layer)
        feas = feas[0:idx,:]
        # predict features
        save_fn = os.path.join(args.out, 'batch_{0}.h5'.format(batch_idx))
        f = h5py.File(save_fn, 'w')
        f.create_dataset('fea', data=feas)
        f.create_dataset('fns', data=batch_fns_s)
        f.create_dataset('batch_idx', data=batch_idx)
        f.close()
        #batch_idx += 1
        print 'Done with batch {0}'.format(save_fn)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--caffe',
                        help='path to caffe installation')
    parser.add_argument('--model_def',
                        help='path to model definition prototxt')
    parser.add_argument('--model',
                        help='path to model parameters')
    parser.add_argument('--layer', default='fc7', help='layer_name')
    parser.add_argument('--dir',
                        help='path to a directory contsining a list of images')
    parser.add_argument('--gpu',
                        help='whether to use gpu training')
    parser.add_argument('--out',
                        help='name of the directory to store the features')
    parser.add_argument('--batch_size', default=256, help='the size of each batch')

    args = parser.parse_args()
    if not os.path.isdir(args.out):
        os.makedirs(args.out)

    if args.caffe is None or args.model is None or args.model_def is None or args.out is None:
        parser.print_help()
        sys.exit()

    caffepath = args.caffe + '/python'
    layer = args.layer
    sys.path.append(caffepath)

    import caffe
    device_id = int(args.gpu)
    caffe.set_mode_gpu()
    caffe.set_device(device_id)
    net = caffe.Net(args.model_def, args.model, caffe.TEST)

    load_size = int(args.batch_size)
    batch_idx = 0
    cnt_ = 0
    for root, dirs, fns in walk(args.dir):
        filenames = []
        for fn in fns:
            filenames.append(os.path.join(root, fn))
            cnt_ += 1
            if cnt_ == load_size:
                batch_predict(filenames, net, layer, batch_idx)
                batch_idx += 1
                cnt_ = 0
                filenames = []
    if cnt_ > 0:
        batch_predict(filenames, net, layer, batch_idx)
        batch_idx += 1
    print 'Done with a total of {0} batches'.format(batch_idx)
