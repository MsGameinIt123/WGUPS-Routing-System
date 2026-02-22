from datetime import timedelta

class Truck:
    """Represents a delivery truck and tracks route progress."""
    def __init__(self, truck_id):
        self.truck_id = truck_id
        self.packages = []
        self.mileage = 0.0
        self.current_location = "Western Governors University"

        self.current_time = timedelta(hours=8)
