from ft_compress.interfaces.compressor import Compressor
import numpy as np
import logging 
import tqdm 
INT_32 = 2**32 
def hash_ft(string):
    h = np.array(2166136261, np.uint32)
    string = string.encode('utf-8')
    for string_i in string: 
        #print (':',np.int8(string_i))
        string_i = np.uint32(np.int8(string_i))
        
        h = h^(string_i)
        h = (h* 16777619) %INT_32
        #print ('h', h)
    return h 


class Compressor8Bit(Compressor):
    
    def fit(self, ft_model, take_every=1):
        bucket_size = ft_model.f.getArgs().bucket
        self.storage['config']['minn'] = str(ft_model.f.getArgs().minn)  
        self.storage['config']['maxn'] = str(ft_model.f.getArgs().maxn)  
        cnt = 0
        word_num = len(ft_model.words)
        logging.debug('estimating params')
        min_ = 99999999.0
        max_ = -99999999.0
        for i in  tqdm.tqdm(range(0, bucket_size+word_num), total=bucket_size+word_num):
            v = ft_model.get_input_vector(i)
            
            min_ = min(min_, np.min(v))
            max_= max(max_, np.max(v))

            
        self.storage['config']['min'] = str(min_)
        self.storage['config']['max'] = str(max_)

        self.storage['config']['dim'] = ft_model.get_dimension()
        
        
        
        logging.debug('loading ngrams')
        
        for i in  tqdm.tqdm(range(0, bucket_size, take_every), total=bucket_size//take_every):
            self.storage['ngrams'][str(i)] = self.vector_to_bytes(ft_model.get_input_vector(i+word_num))
            cnt+=1
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
                h = hash_ft(ngram)
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
        min_ = float(self.storage['config']['min'])
        max_ = float(self.storage['config']['max'])
        
        v = np.round(255*(v-min_)/(max_-min_)).astype(np.uint8)
        
        
        return v.tostring()
        
    def bytes_to_vec(self, b):
        min_ = float(self.storage['config']['min'])
        max_ = float(self.storage['config']['max'])
        
        return (np.fromstring(b, np.uint8)/255)*(max_-min_)+min_

