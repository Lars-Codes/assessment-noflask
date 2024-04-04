from models.vehicle import Vehicle

class ProcessingService:
    
    type = None
    lisence_plate = None
    axle_count = None
    height = None
    length = None 
    
    response_package = None 
    
    binary_data = bytearray() # storing data 
    
    def process(self, data):
        self.retrieve_data(data) # assign binary_data attribute 
        request_type = self.getType() # process request type 
        
        self.processLength() # process length
        self.processPlate() # process license plate 
        
        if(request_type == 1): # insert 
            self.processDataForInsert() # process axel / height 
            vehicle = Vehicle.insert(self.lisence_plate, self.axle_count, self.height) # insert into database
            # if successful: 
                #return self.packageResponse(vehicle)
            #else: 
                # retrieve error  
        elif(request_type == 2): # retrieve 
            vehicle = Vehicle.retrieve(self.lisence_plate) # retrieve from database
            # if successful: 
                #return package response
            #else: 
                # package error 
            pass 
        else: 
            pass # throw error: invalid request type
        
    def retrieve_data(self, data):  
        self.binary_data = bytearray(data) 
        pass 
    
    def getType(self): 
        # get type from binary data
        pass 
    
    def processLength(self): 
        # get the length from binary data
        # if length of message is not consistent with the length of the binary data, throw an error
        pass 
    
    def processPlate(self): 
        # process 10 chars of the string. if first char is empty, throw an error
        pass 
    
    def processDataForInsert(self): 
        # process axel count + height 
        pass
    
    def packageResponse(self, vehicle): 
        # convert response back to binary 
        pass
    
    def packageErrorResponse(self, vehicle): 
        # convert response back to binary, cut off at 255 bytes 
        pass
    
    

    