from models.db import db 

class Vehicle(db.Model):
    # Specify tablename for the model so Flask knows which local mySQL table to reference 
    __tablename__ = 'vehicles' 
    
    id = db.Column(db.Integer, primary_key=True) # even though vehicle passage records are not unique, the vehicle id is unique, 
    # i am including a PK for database management. Alternative could be to use timestamps, or just not using a PK at all. 
    
    # plate name must have a length of 10. Length verification is done prior to insertion. 
    lisence_plate = db.Column(db.String(10)) 
    
    # short int, 2 bytes of space 
    axle_count = db.Column(db.SmallInteger) 
    height = db.Column(db.SmallInteger)
    
    # constructor 
    def __init__(self, lisence_plate, axle_count, height):
        self.lisence_plate = lisence_plate
        self.axle_count = axle_count
        self.height = height
  
    def __str__(self):
        return f"Vehicle: {self.lisence_plate} {self.axle_count} {self.height}"
       
    @classmethod 
    def insert(cls, lisence_plate, axle_count, height):
        try: 
            print("Inserting vehicle", lisence_plate, axle_count, height)
            vehicle = cls(lisence_plate, axle_count, height)
            db.session.add(vehicle)
            db.session.commit()
            return vehicle
        except Exception as e: 
            print("Error inserting vehicle", e)
            return e
    
    @classmethod
    def retrieve(cls, license_plate): 
        try: 
            # add try/catch blocks for error handling
            return cls.query.filter_by(lisence_plate=license_plate).first()
        except Exception as e: 
            print(e)
            return e
       
        
    
    