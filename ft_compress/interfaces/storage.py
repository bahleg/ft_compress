class Storage:
    
    
    def __getattr__(self, attr):
        raise NotImplementedError()
            
    def load_from_file(self, path):
        raise NotImplementedError()
        
    def load_from_compressor(self, compressor):
        raise NotImplementedError()
        
    def dump_to_file(self, path):
        raise NotImplementedError()
        
      