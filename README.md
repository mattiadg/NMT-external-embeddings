# NMT with External Embeddings
This project has the purpose of evaluating the possiblity of using embeddings trained outside the parallel data to improve NMT.
The problem comes from the limited size of the vocabulary, which is usually tackled by using subword-level representations, but this approach has the downside of increasing the sentence lengths.

Experiments
----------
In the experiments conducted so far, we found that it is possible to use only externally-trained embeddings in the source side and get meaningful translations, but the results are weaker than the word-level baseline for a small training set (IWSLT2016).
This is the experimental setting:
* IWSLT 2016 En-Fr
* ***Baseline*** Word level NMT (Nematus)
* Our system:
  * ***External Embeddings***: Glove Gigacrawl
  * Bi-directional mapping of external word embeddings

Results: 3 bleu scores under the baseline on the dev set

Next Steps
----------
- [ ] Implement combination of internal and external exmbeddings. The input words should go both to the normal network and to the mapper
- [ ] Experiment with this setting
- [ ] Make the code more readable
