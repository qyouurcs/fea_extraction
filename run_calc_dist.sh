#!/usr/bin/env bash

if [ $# -lt 4 ]; then
    echo "Usage: $0 <h5py_dir_1mlillion> <h5py_dir_target> <process_id> <total_processes> [fea_len=1024]"
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

h5py_dir=$1
h5py_dir_dst=$2
process_id=$3
total_process=$4
fea_len=1024

if [ $# -ge 5 ]; then
    fea_len=$5
fi

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
python script_calc_dist.py $h5py_dir $h5py_dir_dst $process_id $total_process $fea_len
