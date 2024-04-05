from models.vehicle import Vehicle
from service.error import ErrorService

import re 
class ProcessingService:
    
    type = None
    lisence_plate = None
    axle_count = None
    height = None
    length = None 
    
    response_package = None 
    
    binary_data = bytes() # initializing empty byte array  
    
    def process(self, data):
        self.retrieve_data(data) # assign binary_data attribute  
        request_type = self.getType() # process request type 
       
        length = self.processLength() # process length   
        if(isinstance(length, bytes)): # if request type is an error message, return error message
            return length
        
        plate = self.processPlate() # process license plate 
        if(isinstance(plate, bytes)): # if request type is an error message, return error message
            return plate 
        
        if(request_type == 1): # insert 
            self.processDataForInsert() # process axel / height 
            res = Vehicle.insert(self.lisence_plate, self.axle_count, self.height) # insert into database
            return res 
        
        elif(request_type == 2): # retrieve 
            vehicle = Vehicle.retrieve(self.lisence_plate) # retrieve from database
            return vehicle 
        else: 
            return ErrorService.packageErrorResponse(error_code=255, error="Invalid request type".encode('utf-8'))
        
    def retrieve_data(self, data):  
        # self.binary_data = bytes(data) # using bytes and not bytearray because bytes type is immutable 
        if(type(data)!=bytes): 
            self.binary_data = bytes(data)
        else: 
            self.binary_data = data # using bytes and not bytearray because bytes type is immutable 
    
    def getType(self): 
        # get type from binary data
        request_type = int.from_bytes(self.binary_data[2:3]) # get the third byte for type.
        self.type = request_type
            
    def processLength(self): 
        # get the length from binary data
        # if length of message is not consistent with the length of the binary data, throw an error
        
        # USE FOR BIG ENDIAN 
        specified_length = int.from_bytes(self.binary_data[:2], byteorder='big') # get the first two bytes for length. 
        
        # USE FOR LITTLE ENDIAN 
        # specified_length = int.from_bytes(self.binary_data[:2], byteorder='little') # get the first two bytes for length. 
        
        data_length = len(self.binary_data) - 2 # get the length of the data
        
         # if the specified length is not equal to the actual length, throw error
        if(specified_length != data_length): 
            return ErrorService.packageErrorResponse(error_code=255, error="Specified length does not match length of data".encode('utf-8'))
        
        self.length = specified_length
        return specified_length
    
    def processPlate(self): 
        # process 10 chars of the string. if first char is empty, throw an error
        lp = self.binary_data[3:13].decode('utf-8').strip() # get the first 10 bytes for the license plate.
            
        pattern = r'^[a-zA-Z0-9]+$'
        isAlphanumeric = bool(re.match(pattern, lp))
        
        if(isAlphanumeric): 
            self.lisence_plate = lp
            return 0 
        else: 
            return ErrorService.packageErrorResponse(error_code=255, error="License plate must be alphanumeric".encode('utf-8'))
         
    
    # process axel count + height 
    def processDataForInsert(self): 
        # BIG ENDIAN 
        self.axle_count = int.from_bytes(self.binary_data[13:15], byteorder='big') # get the first two bytes for length. 
        self.height = int.from_bytes(self.binary_data[-2:], byteorder='big') # get the first two bytes for length. 
        
        # LITTLE ENDIAN 
        # axels = int.from_bytes(self.binary_data[13:15], byteorder='little') # get the first two bytes for length. 
        # height = int.from_bytes(self.binary_data[-2:], byteorder='little') # get the first two bytes for length. 
        
        # throw error if too many axels 


    

    