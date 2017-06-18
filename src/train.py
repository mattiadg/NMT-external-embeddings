#!/usr/bin/env python
'''
    File name: train.py
    Description: this is a wrapper script to preprocess and train a NMT system (it uses Nematus toolkit)
    Author: Rajen Chatterjee
    Email: chatterjee@fbk.eu
    Date created: 17th July, 2016
    Python Version: 2.7
'''

import sys
from subprocess import Popen
from nematus.nmt import train
import ast

import config

conf = config.Configuration(sys.argv[1])
device = sys.argv[2]
script_dir = sys.argv[3]

def get_data_path():
    path = dict()
    if(ast.literal_eval(conf.apply_bpe)):
        path["train_src"] = conf.work_dir + "/train.bpe." + conf.src
        path["train_trg"] = conf.work_dir + "/train.bpe." + conf.trg
        path["dev_src"] = conf.work_dir + "/dev.bpe." + conf.src
        path["dict_src"] = conf.work_dir + "/train.bpe." + conf.src + ".json"
        path["dict_trg"] = conf.work_dir + "/train.bpe." + conf.trg + ".json"
    else:
        path["train_src"] = conf.work_dir + "/train." + conf.src
        path["train_trg"] = conf.work_dir + "/train." + conf.trg
        path["dev_src"] = conf.work_dir + "/dev." + conf.src
        path["dict_src"] = conf.work_dir + "/train." + conf.src + ".json"
        path["dict_trg"] = conf.work_dir + "/train." + conf.trg + ".json"
    path["dev_trg"] = conf.work_dir + "/dev." + conf.trg

    return path


def get_external_validation_script(path):
    external_validation_script = []
    uidx = '0'
    external_validation_script.append(script_dir + "/validate.sh")
    external_validation_script.append(conf.work_dir)
    external_validation_script.append(path["dev_src"])
    external_validation_script.append(path["dev_trg"])
    external_validation_script.append(device)
    external_validation_script.append(uidx)
    print ' '.join(external_validation_script)
    return external_validation_script

def run_subword():
    cmd = []
    cmd.append(script_dir + "/preprocess.sh")
    cmd.append(conf.data_dir)
    cmd.append(conf.src)
    cmd.append(conf.trg)
    cmd.append(conf.work_dir)
    cmd.append(conf.bpe_operation_src)
    cmd.append(conf.bpe_operation_trg)
    cmd.append(conf.apply_bpe)
    cmd.append(script_dir)
    preprocess = Popen(cmd)
    exit_val = preprocess.wait()
    return exit_val

def run_nmt(path):
    external_validation_script = get_external_validation_script(path)

    validerr = train(saveto=conf.work_dir + "/model.npz",
                    external_validation_script=external_validation_script,
                    datasets=[path["train_src"], path["train_trg"]],
                    valid_datasets=[path["dev_src"], path["dev_trg"]],
                    dictionaries=[path["dict_src"], path["dict_trg"]],
                    n_words_src=ast.literal_eval(conf.n_words_src),
                    n_words=ast.literal_eval(conf.n_words),
                    maxlen=ast.literal_eval(conf.maxlen),
                    dim=ast.literal_eval(conf.dim),
                    dim_word=ast.literal_eval(conf.dim_word),
                    factors=ast.literal_eval(conf.factors),
                    dim_per_factor=ast.literal_eval(conf.dim_per_factor),
                    batch_size=ast.literal_eval(conf.batch_size),
                    valid_batch_size=ast.literal_eval(conf.valid_batch_size),
                    reload_=ast.literal_eval(conf.reload_),
                    overwrite=ast.literal_eval(conf.overwrite),
                    optimizer=conf.optimizer,
                    lrate=ast.literal_eval(conf.lrate),
                    dispFreq=ast.literal_eval(conf.dispFreq),
                    validFreq=ast.literal_eval(conf.validFreq),
                    saveFreq=ast.literal_eval(conf.saveFreq),
                    sampleFreq=ast.literal_eval(conf.sampleFreq),
                    use_dropout=ast.literal_eval(conf.use_dropout),
                    dropout_embedding=ast.literal_eval(conf.dropout_embedding),
                    dropout_hidden=ast.literal_eval(conf.dropout_hidden),
                    dropout_source=ast.literal_eval(conf.dropout_source),
                    dropout_target=ast.literal_eval(conf.dropout_target),
                    shuffle_each_epoch=ast.literal_eval(conf.shuffle_each_epoch),
                    max_epochs=ast.literal_eval(conf.max_epochs),
                    finish_after=ast.literal_eval(conf.finish_after),
                    finetune=ast.literal_eval(conf.finetune),
                    finetune_only_last=ast.literal_eval(conf.finetune),
                    sort_by_length=ast.literal_eval(conf.sort_by_length),
                    use_domain_interpolation=ast.literal_eval(conf.use_domain_interpolation),
                    domain_interpolation_min=ast.literal_eval(conf.domain_interpolation_min),
                    domain_interpolation_inc=ast.literal_eval(conf.domain_interpolation_inc),
                    domain_interpolation_indomain_datasets=ast.literal_eval(conf.domain_interpolation_indomain_datasets),
                    maxibatch_size=ast.literal_eval(conf.maxibatch_size),
                    decay_c=ast.literal_eval(conf.decay_c),
                    map_decay_c=ast.literal_eval(conf.decay_c),
                    alpha_c=ast.literal_eval(conf.alpha_c),
                    clip_c=ast.literal_eval(conf.clip_c),
                    patience=ast.literal_eval(conf.patience),
                    encoder=conf.encoder,
                    decoder=conf.decoder,
                    embs=conf.external_embeddings,
                    emb_type=conf.emb_type)
    return validerr

if __name__ == '__main__':
    #copy_config(sys.argv[1], conf.work_dir)
    #save_config.save(conf, conf.work_dir + "/conf_param.cfg")
    exit_val = run_subword()
    path = get_data_path()
    validerr = run_nmt(path)
