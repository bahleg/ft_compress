class Compressor:
    
    @property
    def config(self):
        raise NotImplementedError()
        
    def info(self):
        raise NotImplementedError()
        
    def vector_to_bytes(self, v):
        raise NotImplementedError()
        
    def bytes_to_vec(self, b):
        raise NotImplementedError()
        

        