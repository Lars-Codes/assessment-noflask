class ErrorService:
    
    @classmethod
    def packageErrorResponse(cls, error_code=None, error=None):        
        if len(error) > 255:
            err = error[:255]
        else:
            err = error
            
        return bytes([error_code]) + err
            
            
