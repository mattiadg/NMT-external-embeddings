from polyglot.mapping.embeddings import Embedding
from polyglot.mapping import CaseExpander, DigitExpander
from numpy.random import rand
import numpy

def get_embeddings_model(path, typef):
    if typef == 'polyglot':
        embs = Embedding.load(path)
    elif typef == 'glove':
        embs = GloveEmbedding(Embedding.from_glove(path))

    embs.apply_expansion(CaseExpander)
    embs.apply_expansion(DigitExpander)

    return embs

class GloveEmbedding(object):

    def __init__(self, emb):
        self.Embedding = emb
        self.unk = numpy.mean(self.Embedding.vectors, 0)
        self.eos = self.unk + numpy.std(self.Embedding.vectors, 0)

    def __getitem__(self, k):
        if k in self.Embedding:
            return self.Embedding[k]
        elif k == '</S>':
            return self.eos
        else:
            return self.unk

    def __contains__(self, k):
        if k in self.Embedding or k == '</S>' or k == '<UNK>':
            return True
        else:
            return False

    def __len__(self):
        return len(self.Embedding) + 2

    @property
    def shape(self):
        return self.Embedding.shape[0] + 2, self.Embedding.shape[1]

    def get(self, k, default=None):
        if k == '<UNK>':
            return self.unk
        elif k == '</S>':
            return self.eos
        else:
            return self.Embedding.get(k, default)

    def apply_expansion(self, expansion):
        self.Embedding.apply_expansion(expansion)



