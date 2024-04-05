from models.vehicle import Vehicle
from service.error import ErrorService

import re 
class ProcessingService:
    
    type = None
    licence_plate = None
    axle_count = None
    height = None
    length = None 
    
    response_package = None 
    
    endian = None 
    
    binary_data = bytes() # initializing empty byte array  
    
    def process(self, data, endian=None): 
        self.endian = endian
        
        self.retrieve_data(data) # assign binary_data attribute  
        request_type = self.getType() # process request type 
       
        length = self.processLength() # process length   
        if(isinstance(length, bytes)): # if request type is an error message, return error message
            return length
        
        plate = self.processPlate() # process license plate 
        if(isinstance(plate, bytes)): # if request type is an error message, return error message
            return plate 
        
        if(self.type == 1): # insert 
            self.processDataForInsert() # process axel / height 
            res = Vehicle.insert(self.licence_plate, self.axle_count, self.height) # insert into database
            return res 
        
        elif(self.type == 2): # retrieve 
            vehicle = Vehicle.retrieve(self.licence_plate, self.endian) # retrieve from database
            return vehicle 
        else: 
            return ErrorService.packageErrorResponse(error_code=255, error="Invalid request type".encode('utf-8'))
        
    def retrieve_data(self, data):  
        # using bytes and not bytearray because bytes type is immutable 
        if(type(data)!=bytes): 
            self.binary_data = bytes(data)
        else: 
            self.binary_data = data # using bytes and not bytearray because bytes type is immutable 
    
    def getType(self): 
        # get type from binary data
        request_type = int.from_bytes(self.binary_data[2:3]) # get the third byte for type.
        self.type = request_type
            
    def processLength(self): 
        data_length = len(self.binary_data) - 2 # get the length of the data 
        
        if(self.endian == None): 
            self.detectEndianness(data_length)
            
        specified_length = int.from_bytes(self.binary_data[:2], byteorder=self.endian)
        
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
            self.licence_plate = lp
            return 0 
        else: 
            return ErrorService.packageErrorResponse(error_code=255, error="License plate must be alphanumeric".encode('utf-8'))
         
    
    # process axel count + height 
    def processDataForInsert(self): 
        # BIG ENDIAN 
        self.axle_count = int.from_bytes(self.binary_data[13:15], byteorder=self.endian) # get the first two bytes for length. 
        self.height = int.from_bytes(self.binary_data[-2:], byteorder=self.endian) # get the first two bytes for length. 
        
    def detectEndianness(self, data_length): 
        specified_length = int.from_bytes(self.binary_data[:2], byteorder='big') # get the first two bytes for length. 
        if(specified_length != data_length): 
            specified_length = int.from_bytes(self.binary_data[:2], byteorder='little') # get the first two bytes for length. 
            if(specified_length != data_length): 
                return ErrorService.packageErrorResponse(error_code=255, error="Specified length does not match length of data".encode('utf-8'))
            else: 
                self.endian = 'little'
        else: 
            self.endian = 'big'
        
        return specified_length



    

    