class Package:
    def __init__(self, package_id, address, city, zip_code, deadline, weight, notes=""):
        self.package_id = package_id
        self.address = address
        self.original_address = address
        self.city = city
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        
        #These change as the program runs
        self.status = "At hub"
        #self.correction_time = correction_time
        self.delivery_time = None
        
    def __str__(self):
        return (f"Package {self.package_id}: "
                f"{self.address}, {self.city} {self.zip_code} | "
                f"Deadline: {self.deadline} | "
                f"Status: {self.status} | "
                f"Delivered at: {self.delivery_time}")