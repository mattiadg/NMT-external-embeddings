for i in 1 2 3
do
bash train.sh ~/NLP/tools/NMT/nematus-master/toy_example/config.cfg gpu0 ~/NLP/tools/NMT/nematus-master/toy_example/ &>log.train-1000Sents-500upd.AAA-$i
done

for i in 1 2 3
do
bash train.sh ~/NLP/tools/NMT/nematus-master/toy_example/config.cfg gpu0 ~/NLP/tools/NMT/nematus-master/toy_example/ &>log.train-1000Sents-500upd.BBB-$i
done

for i in 1 2 3
do
bash train.sh ~/NLP/tools/NMT/nematus-master/toy_example/config.cfg gpu0 ~/NLP/tools/NMT/nematus-master/toy_example/ &>log.train-1000Sents-500upd.CCC-$i
done
