import numpy as np 
import json

class Compressor:    
        
    def __init__(self, storage):
        self.storage = storage
        self.storage['config']['dim'] = '-1'
        self.storage['config']['n'] = '-1'
        

    def fit(self, ft_model, **kwargs):
        raise NotImplementedError()

    
    def info(self):
        raise NotImplementedError()
        
    def get_ngram_vector(self, ngram):
        raise NotImplementedError()
        
    def get_word_vector(self, word, n=4, dim=300):
        word_ = '<'+word+'>'
        ngrams = [self.get_ngram_vector(word_[i:i+n]) for i in range(0, len(word_)-n)]
        ngrams = [n for n in ngrams if n is not None]
        if len(ngrams)==0:
            return np.zeros(dim)            
        return np.mean(ngrams)
    
    def __getitem__(self, word):
        return self.get_word_vector(word, n = int(self.storage['config']['n']), dim = int(self.storage['config']['dim']) )