#!/bin/sh

# set-up environmental variables
# /hltsrv1/software/nematus-master/config_env.sh

# path to nematus ( https://www.github.com/rsennrich/nematus )
nematus=/hltsrv0/digangi/nematus-15.11.2016.embeddings
source $nematus/config_env.sh

# path to moses decoder: https://github.com/moses-smt/mosesdecoder
mosesdecoder=/hltsrv1/software/moses/moses-20150228_kenlm_cmph_xmlrpc_irstlm_master

work_dir=$1
dev=$2
ref=$3
device=gpu$SGE_GPU
uidx=$5

model="$work_dir/model.iter$uidx.npz"
prefix="$work_dir/model.npz"

ln -s $work_dir/model.npz.json $work_dir/model.iter$uidx.npz.json
# decode
THEANO_FLAGS="mode=FAST_RUN,floatX=float32,device=$device,on_unused_input=warn,force_device=True,lib.cnmem=0.0,dnn.enabled=False" OMP_NUM_THREADS=1 python $nematus/nematus/translate.py \
     -m $model \
     -i $dev \
     -o $dev.$uidx.output \
     -a $dev.$uidx.output.align \
     -k 12 -n -p 6 --use-external-embeddings

$nematus/postprocess-dev.sh < $dev.$uidx.output > $dev.$uidx.output.postprocessed


#perl $mosesdecoder/scripts/generic/multi-bleu.perl $ref < $dev.$uidx.output.postprocessed >> model.npz_bleu_scores

#exit

BLEU=`$mosesdecoder/scripts/generic/multi-bleu.perl $ref < $dev.$uidx.output.postprocessed  | cut -f 3 -d ' ' | cut -f 1 -d ','`
echo "UIDX=$uidx : BLEU=$BLEU" >> ${prefix}_bleu_scores

if [ -f ${prefix}_best_bleu ]; then
    BEST=`cat ${prefix}_best_bleu || echo 0`
    BETTER=`echo "$BLEU > $BEST" | bc`
else
    BETTER="1"
fi
# save model with highest BLEU
if [ "$BETTER" = "1" ]; then
  echo "new best; saving"
  echo $BLEU > ${prefix}_best_bleu
  cp ${prefix}.dev.npz "$work_dir/model.best_bleu.npz"
fi

