import numpy as np
import json
import logging


class Compressor:
    """
    Basic class for compressors.
    Compressor is a compressed representation of fastText model
    """
    def __init__(self, storage):
        """
        storage is a dict-like object. 
        See Storage class for details
        """
        self.storage = storage
        try:
            int(self.storage['config']['dim'])
            int(self.storage['config']['minn'])
            int(self.storage['config']['maxn'])
        except:
            self.storage['config']['dim'] = '-1'
            self.storage['config']['maxn'] = '-1'
            self.storage['config']['minn'] = '-1'

    def fit(self, ft_model, **kwargs):
        raise NotImplementedError()

    def info(self):
        raise NotImplementedError()

    def get_ngram_vector(self, ngram, full_word_ngram=False):
        raise NotImplementedError()

    def get_word_vector(self, word, minn=3, maxn=6, dim=300, verbose=False):
        """
        Gathering vector for word using prediction method
        """
        word_ = '<' + word + '>'
        ngrams = []
        for n_ in range(minn, maxn + 1):
            for subw_id in range(0,
                                 len(word_) - n_ +
                                 1):  # ignoring start at '<' or '>'
                if len(word_[subw_id:subw_id + n_]) != n_:
                    break
                if n_ == 1 and subw_id in [0, len(word_) - 1]:
                    continue
                if verbose:
                    logging.debug('{0}:{1}:{2}'.format(
                        subw_id, n_, word_[subw_id:subw_id + n_]))
                ngrams.append(word_[subw_id:subw_id + n_])

        ngrams = [self.get_ngram_vector(w, False) for w in ngrams]
        ngrams.append(self.get_ngram_vector(word, True))
        ngrams = [n for n in ngrams if n is not None]
        if len(ngrams) == 0:
            return np.zeros(dim)
        return np.mean(ngrams, 0)

    def __getitem__(self, word):
        return self.get_word_vector(word,
                                    minn=int(self.storage['config']['minn']),
                                    maxn=int(self.storage['config']['maxn']),
                                    dim=int(self.storage['config']['dim']))
