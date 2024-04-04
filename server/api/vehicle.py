from flask import Blueprint
from models.vehicle import Vehicle

vehicle_bp = Blueprint('vehicle_bp', __name__)

@vehicle_bp.route('/')
def main(): 
    return "testing"