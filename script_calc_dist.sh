#!/usr/bin/bash

if [ $# -lt 3 ];then
    echo "Usage: $0 <num_threads> <h5py_dir_1million> <h5py_dir_target>"
    exit
fi

num_t=$1
train_fea=$2
target_fea=$3

for i in $(seq 0 $((num_t-1)))
do
    python script_calc_dist.py $train_fea $target_fea $i $num_t&
    sleep 0.5
done
