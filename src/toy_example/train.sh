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
#. /hltsrv1/software/nematus-master/config_env.sh

script_dir=/home/farajian/NLP/tools/NMT/nematus-15.11.2016/
config=$1
device=$2
work_dir=$3

out=$work_dir/log.out
err=$work_dir/log.err
THEANO_FLAGS="exception_verbosity=high,mode=FAST_RUN,floatX=float32,device=$device,on_unused_input=warn,force_device=True,lib.cnmem=0.0,dnn.enabled=False" OMP_NUM_THREADS=1 python $script_dir/train.py $config $device $script_dir #> $out 2> $err
