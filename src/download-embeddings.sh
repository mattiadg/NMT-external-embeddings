if [ ! -f data//glove.42B.300d.txt ]; then
    wget http://nlp.stanford.edu/data/glove.42B.300d.zip
    pushd ../data
        unzip ../src/glove.42B.300d.zip/ glove.42B.300d.txt
    popd
fi
