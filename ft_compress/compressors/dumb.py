from ft_compress.interfaces.compressor import Compressor
import numpy as np
import logging 

class DumbCompressor(Compressor):
    DTYPE = np.float32
    DTYPE_SIZE = 4
    
    def fit(self, ft_model, take_every=1):
        dtype = np.float32        
        self.dtype = dtype
        self.ngrams = {}
        self.storage['config']['dim'] = ft_model.get_dimension()
        logging.debug('loading words')

            
        for w_id, w in enumerate(ft_model.words):
            if w_id%take_every != 0:
                continue
            ngrams, ids = ft_model.get_subwords(w)
            for n,i in zip(ngrams, ids):
                self.ngrams[n] = i
        logging.debug('filling matrix')       
        maxn = 0  
        for new_id,n in enumerate(self.ngrams):
            old_id = self.ngrams[n]
            self.storage['ngrams'][n] = self.vector_to_bytes(ft_model.get_input_vector(old_id))
            if not (n.startswith('<') and n.endswith('>')): 
                maxn = max(maxn, len(n))
        self.storage['config']['n'] = str(maxn)
        logging.debug('ready')
        self.storage['info']['vec len'] = str(self.DTYPE_SIZE*len(ft_model.get_input_vector(old_id)))
        self.storage['info']['ngram len'] = str(sum([len(n) for n in self.ngrams]))
        self.storage['info']['ngram count'] = str(len(self.ngrams))
        del self.ngrams
    
    def get_ngram_vector(self, ngram):
        try:
            return self.bytes_to_vec(self.storage['ngrams'][ngram])
        except:
            return None
        
    def info(self):
        size = 0
        size = int(self.storage['info']['ngram len'])
        size += int(self.storage['info']['ngram count'])*int(self.storage['info']['vec len'])
        size/=1024
        size/=1024
        return 'Number of ngrams: {0}. Approximate size: {1} MB'.format(self.storage['info']['ngram count'], size)
    
        
    def vector_to_bytes(self, v):
        return v.astype(self.dtype).tostring() 
        
    def bytes_to_vec(self, b):
        return np.fromstring(b, self.dtype)

if __name__=='__main__':
    from ft_compress.storages.dict_based import DictStorage
    import sys 
    import logging
    log_format = '[%(asctime)s] [%(levelname)s] - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=log_format)
    log = logging.getLogger(__name__)

    # writing to stdout
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(log_format)
    log.addHandler(handler)
    logging.debug('hello')
    from fasttext import load_model
    model = load_model('/home/legin/fasttext/wiki.en.bin')
    d = DictStorage()
    c = DumbCompressor(d)
    c.fit(model, 200000)

    