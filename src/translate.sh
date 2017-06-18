#!/bin/sh

# set-up environmental variables

# path to nematus ( https://www.github.com/rsennrich/nematus )
nematus=/hltsrv1/software/Nematus/nematus-15.11.2016.save-gradient

source $nematus/config_env.sh

# path to moses decoder: https://github.com/moses-smt/mosesdecoder
mosesdecoder=/hltsrv1/software/moses/moses-20150228_kenlm_cmph_xmlrpc_irstlm_master

work_dir=$1
dev=$2
ref=$3
device=$4
uidx=$5

model="$work_dir/model.npz.dev.npz"
prefix="$work_dir/model.npz"

# decode
THEANO_FLAGS="mode=FAST_RUN,floatX=float32,device=$device,on_unused_input=warn,force_device=True,lib.cnmem=0.0,dnn.enabled=False" OMP_NUM_THREADS=1 python $nematus/nematus/translate.py \
     -m $model \
     -i $dev \
     -o $dev.$uidx.output \
     -a $dev.$uidx.output.align \
     -k 12 -n -p 6 \
     --use-external-embeddings --embeddings

$nematus/postprocess-dev.sh < $dev.$uidx.output > $dev.$uidx.output.postprocessed


perl $mosesdecoder/scripts/generic/multi-bleu.perl $ref < $dev.$uidx.output.postprocessed

#exit

#BLEU=`$mosesdecoder/scripts/generic/multi-bleu.perl $ref < $dev.$uidx.output.postprocessed  | cut -f 3 -d ' ' | cut -f 1 -d ','`
