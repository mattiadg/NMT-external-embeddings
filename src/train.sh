#!/bin/bash 

# set some parameters for qsub

# -N name of the job
#$ -N NMT

# -q name of the queue to use
#$ -q gpgpu.q

# -l mf=amount of memory requested (this is a MANDATORY parameter), use carefully.
#$ -l mf=500G,gpu=1

#$ -S /bin/sh


# set-up environmental variables
script_dir=/hltsrv0/digangi/nematus-15.11.2016.embeddings
. $script_dir/config_env.sh

config=$1
device=gpu$SGE_GPU
work_dir=$2

out=$work_dir/log.out
err=$work_dir/log.err
THEANO_FLAGS="mode=FAST_RUN,floatX=float32,device=$device,on_unused_input=warn,force_device=True,lib.cnmem=0.0,dnn.enabled=False" OMP_NUM_THREADS=1 python $script_dir/train.py $config $device $script_dir > $out 2> $err
