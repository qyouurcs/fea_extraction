#!/usr/bin/python

import caffe
import numpy as np
import os
import sys
import pdb

if len(sys.argv) < 7:
    print 'Usage: {0} <MODEL_FILE> <PRETRAINED> <IMAGE_FILE_LIST> <device_id> <process_id> <process_num> <save_dir> [layer=fc7]'.format(sys.argv[0])
    sys.exit()
else:
    MODEL_FILE = sys.argv[1]
    PRETRAINED = sys.argv[2]
    IMAGE_FILE_LIST = sys.argv[3]
    device_id = int(sys.argv[4])
    process_id = int(sys.argv[5])
    process_num = int(sys.argv[6])
    save_dir = sys.argv[7]
layer = 'fc7'
if len(sys.argv) > 8:
    layer = sys.argv[8]


caffe_root = '/mnt/ilcompf2d0/project/qyou/src/caffe'
caffe.set_mode_gpu()
caffe.set_device(device_id)
# must done the above before making a caffe.Net.

net = caffe.Classifier(MODEL_FILE, PRETRAINED, mean=np.load(os.path.join(caffe_root , 'python/caffe/imagenet/ilsvrc_2012_mean.npy')).mean(1).mean(1),channel_swap=(2,1,0),input_scale=255)

fid = open(IMAGE_FILE_LIST,'r')

fail_fid = open('fail_imgs_{0}.txt'.format(process_id),'w')

save_fn = os.path.join(save_dir, '{0}-{1}.txt'.format(process_id, process_num))
idx = 0

save_fid = open(save_fn,'w')
for aline in fid:
    idx += 1
    aline = aline.strip()
    input_images = []
    parts = aline.split()
    full_fn = parts[0]
    if (idx % process_num) != process_id:
        continue
    #predict this image using the pretrained model.
    try:
        input_image = caffe.io.load_image(full_fn)
        input_images.append(input_image)
    except:
        fail_fid.write(full_fn + '\n')
        fail_fid.flush()
        continue

    prediction = net.predict(input_images, oversample=False)
    fc7 = net.blobs[layer].data[0]
    fc7 = np.reshape(fc7, (1,fc7.size))
    #max_idx = np.argmax(fc7, axis=1)
    #sys.stdout.write(full_fn +  ' ' + str(max_idx[0]))
    save_fid.write(full_fn) 
    for j in range(fc7.shape[1]):
        save_fid.write(' ' + str(fc7[0][j]))
    save_fid.write('\n')

fail_fid.close()
save_fid.close()
