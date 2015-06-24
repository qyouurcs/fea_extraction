#!/usr/bin/env bash

#if [ $# -lt 4 ]; then
#    echo "Usage: $0 <deploy.prototxt> <modelfile> <image_list> <ProcessID> <ProcessNum> <save_dir> [layer=fc7]"
#    exit
#fi

gid=$((${_CONDOR_SLOT:4} - 1 ))

#gid=0

caffe_python="/mnt/ilcompf2d0/project/qyou/src/caffe/python/"
local_python="/mnt/ilcompf2d0/project/qyou/libs/python_packages/lib/python2.7/site-packages/"

caffe_dep="/mnt/ilcompf2d0/project/qyou/libs/caffe_dep"
python_packages_dep="/mnt/ilcompf2d0/project/qyou/libs/python_packages_dep/"
local_lib="/mnt/ilcompf2d0/project/qyou/libs/"

# this is really stupid. however, just use it currently.


if [ -z $LD_LIBRARY_PATH ]; then
    export LD_LIBRARY_PATH=$caffe_dep:$python_packages_dep:$local_lib
else
    LD_LIBRARY_PATH=$caffe_dep:$python_packages_dep:$local_lib:$LD_LIBRARY_PATH
fi


if [ -z $PYTHONPATH ]; then
    export PYTHONPATH=$local_python:$caffe_python
else
    PYTHONPATH=$caffe_python:$local_python:$PYTHONPATH
fi

echo $PYTHONPATH
python run_batch_fea.py  --caffe ../caffe --model_def VGG_ILSVRC_16_layers_deploy.prototxt --model ./models/VGG_ILSVRC_16_layers.caffemodel --dir ./tmp --out . --gpu
