from ft_compress.interfaces.storage import Storage
import shelve 


class ShelveStorage(Storage):
    """
    Storage based on shelve - built-in python library for 
    disk dict-like objects
    """
    def __init__(self, filename, flag, **shelve_args):
        super(Storage, self).__init__()        
        self._db = shelve.open(filename, flag=flag, **shelve_args)
        self.buckets = {}


    def get_bucket(self, bucket):
        return self.buckets.get(bucket, None)
        
    
    def create_bucket(self, bucket):
        self.buckets[bucket] = BucketEmulator(self._db, bucket)
        return self.buckets[bucket]
    
    def __repr__(self):
        return 'Shelve Storage'


class BucketEmulator:
    def __init__(self, db, prefix):
        self.db = db 
        self.prefix = prefix
    
    def __getitem__(self, key):
        return self.db['{0}.{1}'.format(self.prefix, key)]
    
    def __setitem__(self, key, value):
        self.db['{0}.{1}'.format(self.prefix, key)] = value 
        

        

    
            
if __name__=='__main__':
    d = ShelveStorage('test', 'c')
    print ('empty bucket:', d['test'])
    d['test']['123'] = '456'
    d['test2'][789] ='1023'
    print (d['test']['123'])
    print (d['test2'][789])
    exc = False 

    d = ShelveStorage('test','r')
    print (d['test']['123'])
    print (d['test2'][789])
    print (d)