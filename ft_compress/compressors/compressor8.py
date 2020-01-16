from interfaces.compressor import Compressor
import numpy as np
import logging


class Compressor8bit(Compressor):

    def fit(self, ft_model, take_every=1):
        self.ngrams = {}
        self.storage['config']['dim'] = ft_model.get_dimension()
        logging.debug('loading words')

        for w_id, w in enumerate(ft_model.words):
            if w_id % take_every != 0:
                continue
            ngrams, ids = ft_model.get_subwords(w)
            for n, i in zip(ngrams, ids):
                self.ngrams[n] = i
        logging.debug('Estimating parameters')
        min_ = 99999999
        max_ = -99999999
        for id in self.ngrams.values():
            old_id = self.ngrams[n]
            v = ft_model.get_input_vector(old_id)

            min_ = min(min_, v.min())
            max_ = max(max_, v.max())
        self.storage['config']['min'] = min_ 
        self.storage['config']['max'] = max_ 

        logging.debug('filling matrix')
        maxn = 0
        for new_id, n in enumerate(self.ngrams):
            old_id = self.ngrams[n]
            self.storage['ngrams'][n] = self.vector_to_bytes(
                ft_model.get_input_vector(old_id))
            if not (n.startswith('<') and n.endswith('>')):
                maxn = max(maxn, len(n))
        self.storage['config']['n'] = str(maxn)
        logging.debug('ready')
        self.storage['info']['vec len'] = str(len(ft_model.get_input_vector(old_id)))
        self.storage['info']['ngram len'] = str(
            sum([len(n) for n in self.ngrams]))
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
        size += int(self.storage['info']['ngram count']) * \
            int(self.storage['info']['vec len'])
        size /= 1024
        size /= 1024
        return 'Number of ngrams: {0}. Approximate size: {1} MB'.format(self.storage['info']['ngram count'], size)

    def vector_to_bytes(self, v):
        min_ = self.storage['config']['min']
        max_ = self.storage['config']['max']
        
        v = np.round(255*(v-min_)/(max_-min_)).astype(np.uint8)
        return v.tostring()

    def bytes_to_vec(self, b):
        min_ = self.storage['config']['min']
        max_ = self.storage['config']['max']
        
        return (np.fromstring(b, np.uint8)/255)*(max_-min_)+min_
