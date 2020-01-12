import numpy as np 
import json
import logging

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
        
    def get_word_vector(self, word, n=5, dim=300):
        word_ = '<'+word.lower()+'>'
        ngrams = []
        for n_ in range(1, n):
            if n_>=len(word_):
                break            
            for subw_id in range(1, len(word_)-n_): #ignring start at '<' or '>'
                logging.debug('{0}:{1}:{2}'.format(subw_id, n_, word_[subw_id:subw_id +  n_]))
                ngrams.append(word_[subw_id:subw_id +  n_])
        if word_ not in ngrams:
            ngrams.append(word_)        
        ngrams = [self.get_ngram_vector(w) for w in ngrams]          
        ngrams = [n for n in ngrams if n is not None]    
        if len(ngrams)==0:
            return np.zeros(dim)            
        return np.mean(ngrams,0)
    
    def __getitem__(self, word):
        return self.get_word_vector(word, n = int(self.storage['config']['n']), dim = int(self.storage['config']['dim']) )