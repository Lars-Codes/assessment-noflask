# storing temporary in-memory database 
class db: 
    
    data = []
    
    @classmethod
    def getVehicle(cls, license_plate): 
        for vehicle in reversed(cls.data):
            if vehicle.licence_plate == license_plate:
                return vehicle
        return None
    
    @classmethod
    def insertVehicle(cls, vehicle): 
        cls.data.append(vehicle)
        
    @classmethod
    def getData(cls): 
        return cls.data