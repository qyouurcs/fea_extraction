#!/usr/bin/python

import caffe
import numpy as np
import os
import sys
import pdb

# Set the right path to your model file, pretrained model,
# and the image you would like to classify.
#MODEL_FILE = 'imagenet_deploy.prototxt'
#PRETRAINED = './caffe_reference_imagenet_model'
#IMAGE_FILE = '/home/qyou/Downloads/lena.png'

#MODEL_FILE = 'vso_deploy.prototxt'
#PRETRAINED = 'vso_flickr_train_iter_100000'
#IMAGE_FILE = '/home/qyou/Downloads/lena.png'

#MODEL_FILE = 'imagenet_deploy.prototxt'
#PRETRAINED = 'caffe_flickr_train_iter_90000'
#IMAGE_FILE = '/home/qyou/Downloads/lena.png'


if len(sys.argv) < 4:
    print 'Usage: ./run_batch...py <MODEL_FILE> <PRETRAINED> <IMAGE_FILE_LIST> [batch_size=256] [device_id = 0 or 1]'
    sys.exit()
else:
    MODEL_FILE = sys.argv[1]
    PRETRAINED = sys.argv[2]

    IMAGE_FILE_LIST = sys.argv[3]
caffe_root = '/home/qyou/src/caffe-release/caffe-0.999'    
batch_size = 256

device_id = 0
if len(sys.argv) > 4:
    batch_size = int(sys.argv[4])
if len(sys.argv) > 5:
    device_id = int(sys.argv[5])

#MODEL_FILE = 'lower_vso_deploy.prototxt'
#PRETRAINED = 'lower_vso_fseq_train_iter_70000'
#IMAGE_FILE = '/home/qyou/Downloads/lena.png'

net = caffe.Classifier(MODEL_FILE, PRETRAINED, mean_file=os.path.join(caffe_root , 'python/caffe/imagenet/ilsvrc_2012_mean.npy'),channel_swap=(2,1,0),input_scale=255)
net.set_phase_test()
net.set_mode_gpu()
net.set_device(device_id)

#prediction = net.predict(IMAGE_FILE)

fid = open(IMAGE_FILE_LIST,'r')

pred_label = -1
input_images = []
full_fns = []
for aline in fid:
    aline = aline.strip()
    parts = aline.split()
    full_fn = parts[0]
    #predict this image using the pretrained model.

    try:
        input_image = caffe.io.load_image(full_fn)
    except:
        # just ignore this one
        continue
    if len(input_images) < batch_size:
        input_images.append(input_image)
        full_fns.append(full_fn)
        continue
    try:
        prediction = net.predict(input_images)
    except:
        # there is an exception, which may be due to the image format problem.
        # Just ignore it.
        continue
    max_idx = np.argmax(prediction, axis=1)
    for i in range(len(input_images)):
        sys.stdout.write(full_fns[i] +  ' ' + str(max_idx[i]))
        for j in range(prediction.shape[1]):
            sys.stdout.write(' ' + str(prediction[i][j]))
        sys.stdout.write('\n')
        
    input_images = []
    full_fns = []
    input_images.append(input_image)
    full_fns.append(full_fn)

prediction = net.predict(input_images)
max_idx = np.argmax(prediction, axis=1)
for i in range(len(input_images)):
    sys.stdout.write(full_fns[i] +  ' ' + str(max_idx[i]))
    for j in range(prediction.shape[1]):
        sys.stdout.write(' ' + str(prediction[i][j]))
    sys.stdout.write('\n')
 
