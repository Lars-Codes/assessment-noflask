from  service.error import ErrorService
from database.temp_db import db
class Vehicle:
    # Specify tablename for the model so Flask knows which local mySQL table to reference 
    __tablename__ = 'vehicles' 
    
    id = None 
    license_plate = None
    axle_count = None
    height = None
    created_at = None
        
    
    # constructor 
    def __init__(self, licence_plate, axle_count, height):
        self.licence_plate = licence_plate
        self.axle_count = axle_count
        self.height = height
  
    #toString method 
    def __str__(self):
        return f"Vehicle: {self.id} {self.licence_plate} {self.axle_count} {self.height}"
       
    @classmethod 
    def insert(cls, licence_plate, axle_count, height, endian):
        try: 
            vehicle = cls(licence_plate.strip(), axle_count, height)
            db.insertVehicle(vehicle)
            size = 1 
            return size.to_bytes(2, endian) + bytes([0x0]) # Response 0 for success
        except Exception as e: 
            print(e)
            error_bytes = str(e).encode('utf-8') # encode error into bytes
            return ErrorService.packageErrorResponse(error_code=255, error=error_bytes, endian=endian)
    
    @classmethod
    def retrieve(cls, licence_plate, endian): 
        try: 
            # retrieve latest record based on timestap 
                
            # vehicle = cls.query.filter_by(licence_plate=licence_plate).order_by(cls.created_at.desc()).first()
            print(licence_plate)
            vehicle = db.getVehicle(licence_plate)
            
            if vehicle is None: 
                return ErrorService.packageErrorResponse(error_code=9, error="Vehicle not found".encode('utf-8'), endian=endian)
            else: 
                if len(vehicle.licence_plate) < 10: 
                    vehicle.licence_platelp = vehicle.licence_plate + ' '*(10-len(vehicle.licence_plate)) # pad with spaces
                size = 15    
                return size.to_bytes(2, endian) + bytes([0x03]) + vehicle.licence_plate.encode('utf-8') + vehicle.axle_count.to_bytes(2, endian) + vehicle.height.to_bytes(2, endian)                            

        except Exception as e: 
            print(e)
            error_bytes = str(e).encode('utf-8') # encode error into bytes
            return ErrorService.packageErrorResponse(error_code=9, error=error_bytes, endian=endian)
       
        
    
    