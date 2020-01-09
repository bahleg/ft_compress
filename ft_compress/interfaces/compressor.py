import numpy as np 

class Compressor:    
        
    def __init__(self, storage):
        self.storage = storage

    def fit(self, ft_model):
        raise NotImplementedError()

    
    def info(self):
        raise NotImplementedError()
        
    def get_ngram_vector(self, ngram)
        raise NotImplementedError()
        
    def get_word_vector(self, word, n=4, dim=300):
        word_ = '<'+word+'>'
        ngrams = [get_ngram_vector(w[i:i+n]) for i in range(0, len(word_)-n)]
        ngrams = [n for n in ngrams if n is not None]
        if len(ngrams)==0:
            return np.zeros(dim)            
        return np.mean(ngrams)
        