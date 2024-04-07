from flask import Blueprint, render_template, request
from models.vehicle import Vehicle
from service.processing import ProcessingService
from service.error import ErrorService

vehicle_bp = Blueprint('vehicle_bp', __name__) # define blueprint for application 

@vehicle_bp.route('/') # define route to access from web interface 
def main(): 
    """
        #INSERT DUMMY DATA 
        endian = None # Replace here to retrieve endianness from client app 
        # TYPE: INSERT 
        i_bigendian = bytes([0x00, 0x0F, 0x01, 0x41, 0x42, 0x43, 0x31, 0x32, 0x33, 0x34, 0x20, 0x20, 0x20, 0x00, 0x02, 0x00, 0x06])
        i_littleendian = bytes([0x0F, 0x00, 0x01, 0x41, 0x42, 0x43, 0x31, 0x32, 0x33, 0x34, 0x20, 0x20, 0x20, 0x02, 0x00, 0x06, 0x00])
        # TYPE: RETRIEVE 
        r_bigendian = bytes([0x00, 0x08, 0x02, 0x41, 0x42, 0x43, 0x31, 0x32, 0x33, 0x34, 0x20, 0x20, 0x20])
        r_littleendian = bytes([0x08, 0x00, 0x02, 0x41, 0x42, 0x43, 0x31, 0x32, 0x33, 0x34, 0x20, 0x20, 0x20])
        ps = ProcessingService() # define ProcessingService object to process byte data 
        ans = ps.process(i_bigendian, 'big') # Process data 
    """
    
    vehicles = Vehicle.getAll() # retrieve all vehicles from database

    return render_template('index.html', vehicles=vehicles) # render template with vehicles

@vehicle_bp.route('/query', methods=['GET']) # define route to access from web interface
def query(): 
    # Get information from form 
    licence_plate = request.args.get('licence_plate').lstrip()
    endian = request.args.get('endian')
    
    # Convert endian string to 'little' or 'big'
    endian = convertEndianString(endian)
    
    # Convert data to bytes
    data = convertToBytes(query_type=2, lp=licence_plate, endian=endian)
    
    if(data[0] == 0): # if request type is an error message, return error message. 
        return convertResponse(data[1], endian)  
    
    ps = ProcessingService() # define ProcessingService object to process byte data 

    # Process data for query 
    ans = ps.process(data[1], endian) # Process data 

    # Convert response to human-readable format
    return convertResponse(ans, endian)

@vehicle_bp.route('/insert', methods=['POST']) # define route to access from web interface
def insert(): 
    # Get information from form
    licence_plate = request.form.get('licence_plate')
    axle_count = request.form.get('axle_count')
    height = request.form.get('height')
    endian = request.form.get('endian')
    
    # Convert endian string to 'little' or 'big'
    endian = convertEndianString(endian)

    # Convert data to bytes
    data = convertToBytes(query_type=1, lp=licence_plate, axels=axle_count, height=height, endian=endian)
    
    if(data[0] == 0): # if request type is an error message, return error message. 
        return convertResponse(data[1], endian)
    
    # Process data for insert
    ps = ProcessingService()
    
    # Process data for insert
    ans = ps.process(data[1], endian) # Process data 
    
    # Convert response to human-readable format
    return convertResponse(ans, endian)


def convertToBytes(length=None, query_type=None, lp=None, axels=None, height=None, endian=None): 
    
    if len(lp) < 10: 
        lp = lp + ' '*(10-len(lp)) # pad with spaces
    elif(len(lp) > 10):
        return [0, ErrorService.packageErrorResponse(error_code=255, error="License plate must be 10 characters or less".encode('utf-8'), endian=endian)]
        
    if(query_type == 2): # Process data for retrieval 
        length = 1 + len(lp) # length is 2 bytes (type) + length of licence plate
        if(endian): 
            data = length.to_bytes(2, endian) + query_type.to_bytes(1, endian) + lp.encode('ascii')
        else: # default to big 
            data = length.to_bytes(2, 'big') + query_type.to_bytes(1, 'big') + lp.encode('ascii')
    else: # process data for insertion 
        length = 15 
        data_type = 1 
        
        if(not axels or not height):
            return [0, ErrorService.packageErrorResponse(error_code=255, error="Axels and height must be specified".encode('utf-8'), endian=endian)]
        elif(not axels.isdigit() or not height.isdigit()):
            return [0, ErrorService.packageErrorResponse(error_code=255, error="Height and axels must be integers".encode('utf-8'), endian=endian)]

        if(endian): 
            data = length.to_bytes(2, endian) + data_type.to_bytes(1, endian) + lp.encode('ascii') + int(axels).to_bytes(2, endian) + int(height).to_bytes(2, endian)
        else: # default to big
            data = length.to_bytes(2, 'big') + data_type.to_bytes(1, 'big') + lp.encode('ascii') + int(axels).to_bytes(2, 'big') + int(height).to_bytes(2, 'big') 

    return [1, data]

def convertEndianString(string): # Convert string to 'little' or 'big'
    if(string == "Big endian"): 
        return 'big'
    elif(string == "Little endian"):
        return 'little'
    else:
        return 'big'
    
# Convert response to human-readable format
def convertResponse(data, endian): 
    length = int.from_bytes(data[:2], byteorder=endian) # get the first two bytes for length
    type = int.from_bytes(data[2:3]) # get the third byte for type
    hex_list = []
    
    for byte in data[:2]: # Length is 2 bytes 
        hex_list.append('0x' + format(byte, '02x'))
        
    hex_list.append(hex(type)) # append type 
    
    # 3 is succesful query response 
    if(type == 3): 
        plate = data[3:13].decode('utf-8')
        plate_list = [hex(ord(c)) for c in plate]
        hex_list.extend(plate_list)
        
        axels_int = int.from_bytes(data[13:15], byteorder=endian)
        height_int = int.from_bytes(data[-2:], byteorder=endian)
        
        for byte in data[13:15]:
            hex_list.append('0x' + format(byte, '02x'))
            
        for byte in data[-2:]:
            hex_list.append('0x' + format(byte, '02x'))
        
        return "BIN DATA: " + str(hex_list) + "<br><br>" + "<b>DECODED MESSAGE:</b> " + "<br><br>" + "Length of data (bytes): " + str(length) + "<br>" + "Type: " + str(type) + "<br>" + "License Plate: " + plate + "<br>" + "Axels: " + str(axels_int) + "<br>" + "Height: " + str(height_int) + " ft"
    
    elif(type==0): # 0 is successful insert response
        return "BIN DATA: " + str(hex_list) + "<br><br>" + "<b>DECODED MESSAGE:</b> " + "<br><br>" + "Length of data (bytes): " + str(length) + "<br>" + "Type: " + str(type) + "<br>" + "Success"
    
    else: # error response
        error_message = data[3:].decode('utf-8')
        binary_list = [hex(ord(c)) for c in error_message]        
        hex_list.extend(binary_list)
        return "BIN DATA: " + str(hex_list) + "<br><br>" + "<b>DECODED MESSAGE:</b> " + "<br><br>" + "Length of data (bytes): " + str(length) + "<br>" + "Type (error code): " + str(type) + "<br>" + "Error Description: " + error_message
    
     

    



