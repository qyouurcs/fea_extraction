#!/usr/bin/env bash

if [ $# -lt 4 ]; then
    echo "Usage: $0 <deploy.prototxt> <modelfile> <image_list> <ProcessID> <ProcessNum> <save_dir> [layer=fc7]"
    exit
fi

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

deploy=$1
model=$2
img_list=$3
process=$4
process_num=$5
save_dir=$6

layer='fc7'

if [ $# -gt 6 ]; then
    layer=$7
fi

if [ ! -d $save_dir ]; then
  mkdir $save_dir
fi

str_hostname=`hostname`
echo $str_hostname

echo $deploy 
echo $model
echo $img_list 
echo $process 
echo $process_num 
echo $gid 
echo $save_dir 
echo $layer
python run_batch_fea_extract.py $deploy $model $img_list $gid $process $process_num $save_dir $layer
