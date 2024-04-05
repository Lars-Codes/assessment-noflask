from models.vehicle import Vehicle
from service.error import ErrorService

import re 
class ProcessingService:
    
    # store data from byte array  
    type = None
    licence_plate = None
    axle_count = None
    height = None
    length = None 
    
    # store endianness 
    endian = None 
    
    binary_data = bytes() # initializing empty byte array  
    
    # Main processing functions to call other functions 
    def process(self, data, endian=None): 
        self.endian = endian # store endianness
        
        self.retrieve_data(data) # Store data and cast to bytes if not already bytes
        
        request_type = self.getType() # process request type (third byte)
       
        length = self.processLength() # process length (first and second bytes) and detect endianness if not specified 
        
        if(isinstance(length, bytes)): # if request type is an error message, return error message. 
            return length
        
        plate = self.processPlate() # process license plate (next 10 bytes)
        if(isinstance(plate, bytes)): # if request type is an error message, return error message
            return plate 
        
        if(self.type == 1): # If type is 1, it is an insert.  
            self.processDataForInsert() # Process bytes that specify the axels / height 
            res = Vehicle.insert(self.licence_plate, self.axle_count, self.height) # insert into database
            return res # return response from database -- either success or error
        
        elif(self.type == 2): # If type is 2, it is a retrieve. 
            vehicle = Vehicle.retrieve(self.licence_plate, self.endian) # retrieve from database
            return vehicle # return response from database -- either success with data, or error
        else: # Invalid request type 
            return ErrorService.packageErrorResponse(error_code=500, error="Invalid request type".encode('utf-8'))
        
    def retrieve_data(self, data):  
        # using bytes and not bytearray because bytes type is immutable. 
        if(type(data)!=bytes): # If the type is not a byte array, cast it to bytes. Assign to attribute binary_data.
            self.binary_data = bytes(data) 
        else: 
            self.binary_data = data # using bytes and not bytearray because bytes type is immutable 
    
    def getType(self): 
        # get type from binary data
        request_type = int.from_bytes(self.binary_data[2:3]) # get the third byte for type.
        self.type = request_type
            
    def processLength(self): # Process specified length of data
        data_length = len(self.binary_data) - 2 # get the length of the data (minus 2 bytes that store the length)
        
        if(self.endian == None): # If endianness is not specified, detect it.
            endian = self.detectEndianness(data_length)
            if(isinstance(endian, bytes)): # if request type is an error message, return error message. 
                return endian
            
        # Length is stored in the first two bytes of the binary data. 
        specified_length = int.from_bytes(self.binary_data[:2], byteorder=self.endian)
        
        self.length = specified_length # Store length in attribute 
        
        return specified_length
    
    def processPlate(self): 
        # process 10 chars of the string. 
        lp = self.binary_data[3:13].decode('utf-8').strip() # get the first 10 bytes for the license plate.
        
        # Make sure plate only contains alphanumeric characters 
        pattern = r'^[a-zA-Z0-9]+$'
        isAlphanumeric = bool(re.match(pattern, lp))
        
        # If not alphanumeric or plate is empty, return error message
        if(not isAlphanumeric): 
            return ErrorService.packageErrorResponse(error_code=500, error="License plate must be alphanumeric".encode('utf-8'))
        elif(lp == '          '): 
            return ErrorService.packageErrorResponse(error_code=500, error="License plate cannot be empty".encode('utf-8'))

        self.licence_plate = lp
        return 0 

    # process axel count + height 
    def processDataForInsert(self): 
        self.axle_count = int.from_bytes(self.binary_data[13:15], byteorder=self.endian) # Process axel count 
        self.height = int.from_bytes(self.binary_data[-2:], byteorder=self.endian) # Process height 
        
    def detectEndianness(self, data_length): 
        specified_length = int.from_bytes(self.binary_data[:2], byteorder='big') # get the first two bytes for length. 
        if(specified_length != data_length): # If the specified length does not match the length of the data, try to convert using little endian order.
            specified_length = int.from_bytes(self.binary_data[:2], byteorder='little') 
            if(specified_length != data_length): # If the specified length does not match the length of the data, return error message.
                return ErrorService.packageErrorResponse(error_code=500, error="Specified length does not match length of data".encode('utf-8'))
            else: # If it wasn't big but now it matches, endianness must be little. 
                self.endian = 'little'
        else: # If it matches the big endian order, endianness must be big.
            self.endian = 'big'
        
        return specified_length # Return the length of the data.



    

    