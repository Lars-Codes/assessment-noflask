from flask import Blueprint
from models.vehicle import Vehicle
from service.processing import ProcessingService

vehicle_bp = Blueprint('vehicle_bp', __name__)

@vehicle_bp.route('/')
def main(): 
    ps = ProcessingService()
    
    endian = None # None, big, or little endian 
    
    # TYPE: INSERT 
    i_bigendian = bytes([0x00, 0x0F, 0x01, 0x41, 0x42, 0x43, 0x31, 0x32, 0x33, 0x34, 0x20, 0x20, 0x20, 0x00, 0x02, 0x00, 0x06])
    i_littleendian = bytes([0x0F, 0x00, 0x01, 0x41, 0x42, 0x43, 0x31, 0x32, 0x33, 0x34, 0x20, 0x20, 0x20, 0x02, 0x00, 0x06, 0x00])

    # TYPE: RETRUEVE 
    r_bigendian = bytes([0x00, 0x08, 0x02, 0x41, 0x42, 0x43, 0x31, 0x32, 0x33, 0x34, 0x20, 0x20, 0x20])
    r_littleendian = bytes([0x08, 0x00, 0x02, 0x41, 0x42, 0x43, 0x31, 0x32, 0x33, 0x34, 0x20, 0x20, 0x20])
    
    ans = ps.process(i_bigendian, 'big')
    
    print(ans)
    
    return "Hello World"