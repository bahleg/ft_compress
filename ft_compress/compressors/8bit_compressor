from interfaces.compressor import Compressor
import numpy as np
import logging 

class DumbCompressor(Compressor):
    def __init__(self, ft_model, maxsize=None, dtype=np.float32):   
        self.ngrams = {}    
        self.dtype = dtype
        
        logging.debug('loading words')
        for w in ft_model.words:
            if maxsize is not None and len(self.ngrams)>maxsize:
                logging.warning('Too many ngrams, breaking')
                break
            ngrams, ids = ft_model.get_subwords(w)
            for n,i in zip(ngrams, ids):
                self.ngrams[n] = i
        logging.debug('filling matrix')        
        for new_id,n in enumerate(self.ngrams):
            old_id = self.ngrams[n]
            self.ngrams[n] = self.vector_to_bytes(ft_model.get_input_vector(old_id))
        logging.debug('ready')
        
        self.byte_size = len(self.ngrams[n])                    
          
    @property
    def config(self):
        return {}
        
    def info(self):
        size = 0
        size += sum([len(n) for n in self.ngrams])
        size+=self.byte_size*len(self.ngrams)
        size/=1024
        size/=1024
        return 'Number of ngrams: {0}. Approximate size: {1} MB'.format(len(self.ngrams), size)
    
        
    def vector_to_bytes(self, v):
        return v.astype(self.dtype).tostring() 
        
    def bytes_to_vec(self, b):
        return np.fromstring(b, self.dtype)
