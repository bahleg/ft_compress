from ft_compress.interfaces.compressor import Compressor
from ft_compress.utils.ft_hash import ft_hash
import numpy as np
import logging 
import tqdm 



class DumbCompressor(Compressor):
    """
    The most simple compressor that just saves all the words for the fastText model
    """
    DTYPE = np.float32
    DTYPE_SIZE = 4
    
    def fit(self, ft_model, save_word_ngrams=True, take_every=1):
        """
        :param take_every: if >1, we will take only each nth ngram and word
        :param save_word_ngrams: if False, we will not save ngram-words which are trained  distinctly as tokens
        """
        bucket_size = ft_model.f.getArgs().bucket
        self.storage['config']['minn'] = str(ft_model.f.getArgs().minn)  
        self.storage['config']['maxn'] = str(ft_model.f.getArgs().maxn)  
        cnt = 0
        word_num = len(ft_model.words)
        self.storage['config']['dim'] = ft_model.get_dimension()
        logging.debug('loading ngrams')
        for i in  tqdm.tqdm(range(0, bucket_size, take_every), total=bucket_size//take_every):
            self.storage['ngrams'][str(i)] = self.vector_to_bytes(ft_model.get_input_vector(i+word_num))
            cnt+=1
        if save_word_ngrams:
            logging.debug('loading words')
            for w in tqdm.tqdm(ft_model.words):
                ngrams, ids = ft_model.get_subwords(w)
                for i,n  in zip(ids, ngrams):
                    if i<word_num and i%take_every == 0:
                        self.storage['word_ngrams'][n] = self.vector_to_bytes(ft_model.get_input_vector(i))
                        cnt+=1
            
        

        logging.debug('ready')
        self.storage['info']['vec len'] = str(self.DTYPE_SIZE*ft_model.get_dimension())        
        self.storage['info']['ngram count'] = str(cnt)
        self.storage['info']['bucket size'] = str(bucket_size)

    
    def get_ngram_vector(self, ngram, full_word=False):
        try:
            if full_word:
                return self.bytes_to_vec(self.storage['word_ngrams'][ngram])
            else:
                h = ft_hash(ngram)
                h = h % int(self.storage['info']['bucket size'])
                h = str(h)
                return self.bytes_to_vec(self.storage['ngrams'][h])
        except KeyError:
            return None 
        
    def info(self):
        size = 0        
        size += int(self.storage['info']['ngram count'])*int(self.storage['info']['vec len'])
        size/=1024
        size/=1024
        return 'Number of ngrams: {0}. Approximate size: {1} MB'.format(self.storage['info']['ngram count'], size)
    
        
    def vector_to_bytes(self, v):
        return v.astype(self.DTYPE).tostring() 
        
    def bytes_to_vec(self, b):
        return np.fromstring(b, self.DTYPE)
