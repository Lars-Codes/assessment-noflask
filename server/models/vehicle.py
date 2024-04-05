from models.db import db 
from  service.error import ErrorService
from sqlalchemy import Column, DateTime, func

class Vehicle(db.Model):
    # Specify tablename for the model so Flask knows which local mySQL table to reference 
    __tablename__ = 'vehicles' 
    
    id = db.Column(db.Integer, primary_key=True) # even though vehicle passage records are not unique, the vehicle id is unique, 
    # i am including a PK for database management.
    
    # plate name must have a length of 10. Length verification is done prior to insertion. 
    licence_plate = db.Column(db.String(10)) 
    
    # short int, 2 bytes of space 
    axle_count = db.Column(db.SmallInteger) 
    height = db.Column(db.SmallInteger)
    
    created_at = Column(DateTime, default=func.now()) # including timestamp to ensure retrieval of LATEST record
        
    # constructor 
    def __init__(self, licence_plate, axle_count, height):
        self.licence_plate = licence_plate
        self.axle_count = axle_count
        self.height = height
  
    #toString method 
    def __str__(self):
        return f"Vehicle: {self.id} {self.licence_plate} {self.axle_count} {self.height}"
       
    @classmethod 
    def insert(cls, licence_plate, axle_count, height):
        try: 
            vehicle = cls(licence_plate, axle_count, height)
            db.session.add(vehicle)
            db.session.commit()
            return bytes([0x00]) # Response 0 for success 
        except Exception as e: 
            print(e)
            error_bytes = str(e).encode('utf-8') # encode error into bytes
            return ErrorService.packageErrorResponse(error_code=500, error=error_bytes)
    
    @classmethod
    def retrieve(cls, licence_plate, endian): 
        try: 
            # retrieve latest record based on timestap 
            vehicle = cls.query.filter_by(licence_plate=licence_plate).order_by(cls.created_at.desc()).first()
            
            if vehicle is None: 
                return ErrorService.packageErrorResponse(error_code=9, error="Vehicle not found".encode('utf-8'))
            else: 
                return bytes([0x03]) + vehicle.licence_plate.encode('utf-8') + vehicle.axle_count.to_bytes(2, endian) + vehicle.height.to_bytes(2, endian)                            

        except Exception as e: 
            print(e)
            error_bytes = str(e).encode('utf-8') # encode error into bytes
            return ErrorService.packageErrorResponse(error_code=9, error=error_bytes)

       
        
    
    