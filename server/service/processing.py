from models.vehicle import Vehicle

import re 
class ProcessingService:
    
    type = None
    lisence_plate = None
    axle_count = None
    height = None
    length = None 
    
    response_package = None 
    
    binary_data = bytes() # storing data 
    
    def process(self, data):
        self.retrieve_data(data) # assign binary_data attribute         
        self.processLength() # process length
        request_type = self.getType() # process request type 
        
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
            print(vehicle)
            # if successful: 
                #return package response
            #else: 
                # package error 
            pass 
        else: 
            pass # throw error: invalid request type
        
    def retrieve_data(self, data):  
        # self.binary_data = bytes(data) # using bytes and not bytearray because bytes type is immutable 
        self.binary_data = data # using bytes and not bytearray because bytes type is immutable 

        pass 
    
    def getType(self): 
        # get type from binary data
        request_type = int.from_bytes(self.binary_data[2:3]) # get the third byte for type.
        if request_type not in [1, 2]: 
            # throw error 
            pass
        else: 
            self.type = request_type
            return request_type 
            
    def processLength(self): 
        # get the length from binary data
        # if length of message is not consistent with the length of the binary data, throw an error
        
        # USE FOR BIG ENDIAN 
        specified_length = int.from_bytes(self.binary_data[:2], byteorder='big') # get the first two bytes for length. 
        
        # USE FOR LITTLE ENDIAN 
        # specified_length = int.from_bytes(self.binary_data[:2], byteorder='little') # get the first two bytes for length. 
        
        data_length = len(self.binary_data) - 2 # get the length of the data
        
        if(specified_length != data_length):
            # return an error message 
            pass
        
        self.length = specified_length
    
    def processPlate(self): 
        # process 10 chars of the string. if first char is empty, throw an error
        lp = self.binary_data[3:13].decode('utf-8').strip() # get the first 10 bytes for the license plate.
        
        # Make sure plate only contains alphanumeric characters and first character is not empty
        # regex = "^(?=.*[a-zA-Z])(?=.*[0-9])[A-Za-z0-9]+$"
        # pattern = re.compile(regex)
        # if(not re.search(pattern, str) or str[0] == " "): # if doesnt contain alphanumeric characters or first character is empty, return error 
        #     pass 
        #     # throw error: only alphanumeric characters
        
        self.lisence_plate = lp
         
    
    # process axel count + height 
    def processDataForInsert(self): 
        # BIG ENDIAN 
        self.axle_count = int.from_bytes(self.binary_data[13:15], byteorder='big') # get the first two bytes for length. 
        self.height = int.from_bytes(self.binary_data[-2:], byteorder='big') # get the first two bytes for length. 
        
        # LITTLE ENDIAN 
        # axels = int.from_bytes(self.binary_data[13:15], byteorder='little') # get the first two bytes for length. 
        # height = int.from_bytes(self.binary_data[-2:], byteorder='little') # get the first two bytes for length. 
        
        # throw error if too many axels 

    
    def packageResponse(self, vehicle): 
        # convert response back to binary 
        pass
    
    def packageErrorResponse(self, vehicle): 
        # convert response back to binary, cut off at 255 bytes 
        pass

    

    