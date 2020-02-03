from ft_compress.interfaces.storage import Storage
import json 

class DictStorage(Storage):
    """
    Storage based on dictionary.
    Note that save and loading functions are implemented
    via json, so all the objects inside the storage must be json-serializable!
    """
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
        return '\n'.join(['Bucket: {0}: {1}...'.format(b, repr(list(self._buckets[b].items())[:10])) for b in self._buckets])

    
    def save(self, path):        
        with open(path, 'w') as out:
            json.dump(self._buckets, out)
            
    def load(self, path):
        with open(path) as inp:
            self._buckets = json.load(inp)
            
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
    d.save('test.json')
    d = DictStorage()
    d.load('test.json')
    print (d)