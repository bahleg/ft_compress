class Storage:
    
    def get_bucket(self, bucket):
        raise NotImplementedError()
    
    def create_bucket(self, bucket):
        raise NotImplementedError()

    def get_value(self, key, bucket):
        return self.get_bucket(bucket)['key']
    
    def set_value(self, key, value, bucket):            
        self['bucket']['key'] = value 
        
    def __getitem__(self, bucket):
        bucket_ = self.get_bucket(bucket)
        if bucket_ is None:
            bucket_ = self.create_bucket(bucket)
        return bucket_
