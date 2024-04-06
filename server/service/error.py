class ErrorService:
    
    @classmethod
    def packageErrorResponse(cls, error_code=None, error=None, endian=None):        
        if len(error) > 255:
            err = error[:255]
        else:
            err = error
        
        length = len(error) + 1 # length is the length of the error + 1, number of bytes for code     

        return length.to_bytes(2, endian) + bytes([error_code]) + err 
            
            
