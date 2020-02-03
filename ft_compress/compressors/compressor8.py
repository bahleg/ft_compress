from ft_compress.interfaces.compressor import Compressor
from ft_compress.utils.ft_hash import ft_hash
import numpy as np
import logging 
import tqdm 


class Compressor8Bit(Compressor):
    """
    Simple quantization-based compressor: saves representation with one-byte 
    per vector component
    """
    
    def fit(self, ft_model, save_word_ngrams=True,  take_every=1):
        """
        :param take_every: if >1, we will take only each nth ngram and word
        :param save_word_ngrams: if False, we will not save ngram-words which are trained  distinctly as tokens
        """
        bucket_size = ft_model.f.getArgs().bucket
        self.storage['config']['minn'] = str(ft_model.f.getArgs().minn)  
        self.storage['config']['maxn'] = str(ft_model.f.getArgs().maxn)  
        cnt = 0
        word_num = len(ft_model.words)
        logging.debug('estimating params')
        dim = ft_model.get_dimension()
        min_ = np.ones(dim) * 99999999.0
        max_ = np.ones(dim) * (-99999999.0)
        for i in  tqdm.tqdm(range(0, bucket_size+word_num), total=(bucket_size+word_num)):
            if i<word_num and not save_word_ngrams:
                continue
            if (i < word_num and i%take_every == 0) or (i>=word_num and (i+word_num)%take_every == 0):
                v = ft_model.get_input_vector(i)
                
                min_ = np.minimum(min_, v)
                max_= np.maximum(max_, v)
                

                
            
        self.storage['config']['min'] = min_.astype(np.float32).tostring()
        self.storage['config']['max'] = max_.astype(np.float32).tostring()

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
        self.storage['info']['vec len'] = str(ft_model.get_dimension())        
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
        min_ = np.fromstring(self.storage['config']['min'], np.float32)
        max_ = np.fromstring(self.storage['config']['max'], np.float32)
        
        v = np.round(255*(v-min_)/(max_-min_)).astype(np.uint8)
        
        
        return v.tostring()
        
    def bytes_to_vec(self, b):
        min_ = np.fromstring(self.storage['config']['min'], np.float32)
        max_ = np.fromstring(self.storage['config']['max'], np.float32)
        
        return (np.fromstring(b, np.uint8)/255)*(max_-min_)+min_

