#!/bin/bash

ANACONDA="/hltsrv1/software/anaconda"

THEANO="/hltsrv1/software/Theano/Theano.0.8.2-dev/"
#THEANO="/hltsrv1/software"

CUDA_ROOT="/usr/local/cuda-7.5"

LIBGPU="/hltsrv1/software/libgpu"

GRAPHVIZ="/hltsrv1/software/graphviz"

export PATH="$GRAPHVIZ/bin/:$ANACONDA/bin:$CUDA_ROOT/bin:$PATH"

export PYTHONPATH="$THEANO:$PYTHONPATH"

export LIBRARY_PATH="$CUDA_ROOT/lib64:$LIBGPU/lib:$LIBRARY_PATH"

export LD_LIBRARY_PATH="$CUDA_ROOT/lib64:$LIBGPU/lib:$LD_LIBRARY_PATH"

export CPATH="$LIBGPU/include:$CPATH"

export CPPPATH="$LIBGPU/include:$CPPPATH"
export PYTHONUNBUFFERED=true
