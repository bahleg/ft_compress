from ft_compress.interfaces.storage import Storage

class DictStorage(Storage):
    def __init__(self):
        super(Storage, self).__init__()
        self._buckets = {}


    def get_bucket(self, bucket):
        return self._buckets.get(bucket, None)
    
    def create_bucket(self, bucket):
        if bucket in self._buckets:
            raise ValueError('Attemp to create existing bucket: '+bucket)
        self._buckets[bucket] = {}
        return self._buckets[bucket]
    
    def __repr__(self):
        return '\n'.join(['Bucket: {0}: {1}'.format(b, repr(self._buckets[b])) for b in self._buckets])

if __name__=='__main__':
    d = DictStorage()
    print ('empty bucket:', d['test'])
    d['test']['123'] = '456'
    d['test2'][789] ='1023'
    print (d)
    exc = False 
    try:
        d.create_bucket('test')
    except:
        exc = True 
        print ('duplicate bucket creation checked')
    if not exc:
        raise ValueError('Could not raise value for duplicate!')
    