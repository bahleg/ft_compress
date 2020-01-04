from interfaces.compressor import Compressor
import numpy as np
import logging 

class Compressor8bit(Compressor):
    def __init__(self, ft_model, maxsize=None):   
        self.ngrams = {}            
        logging.debug('Loading words')
        self.min_ = 99999
        self.max_ = -99999
        for w in ft_model.words:
            if maxsize is not None and len(self.ngrams)>=maxsize:
                logging.warning('Too many ngrams, breaking')
                break
            ngrams, ids = ft_model.get_subwords(w)
            for n,i in zip(ngrams, ids):
                self.ngrams[n] = i
                if maxsize is not None and len(self.ngrams)>=maxsize:
                    logging.warning('Too many ngrams, breaking')
                    break
        logging.debug('Estimating parameters')
        for id in self.ngrams.values():
            old_id = self.ngrams[n]
            v = ft_model.get_input_vector(old_id)
            
            self.min_ = min(self.min_, v.min())
            self.max_ = max(self.max_, v.max())
        
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
        size+=len(self.ngrams)*self.byte_size
        size/=1024
        size/=1024
        return 'Number of ngrams: {0}. Approximate size: {1} MB'.format(len(self.ngrams), size)
    
        
    def vector_to_bytes(self, v):
        v = np.round(255*(v-self.min_)/(self.max_-self.min_)).astype(np.uint8)
        return v.tostring() 
        
    def bytes_to_vec(self, b):
        return (np.fromstring(b, np.uint8)/255)*(self.max_-self.min_)+self.min_
