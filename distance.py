import csv
import re

class DistanceTable:
    def __init__(self):
        self.addresses = []
        self.distances = []

    # Debugging load_distances (to make sure the distances.csv file is being read)
    """ def load_distances(self, filename):
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)
            
            print("Printing first 15 rows of distance file:\n")
            for i in range(15):
                print(f"Row {i}:", rows[i]) """
    
    def load_distances(self, filename):
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)

            # Row 7 contains the header addresses
            header_row = rows[7]

            # Addresses start at column 2
            self.addresses = [cell.strip() for cell in header_row[2:]]

            # Distance rows start at row 8
            for row in rows[8:]:
                # Distance values start at column 2
                cleaned_row = [cell.strip() for cell in row[2:]]
                self.distances.append(cleaned_row)

    # Matches addresses using street numbers and partial string matching.
    # This handles formatting inconsistencies between the package file and the distance table (e.g., abbreviations like "Sta" vs "Station")
    def get_distance(self, address1, address2):
        
        def extract_number(address):
            match = re.search(r'\d+', address)
            return match.group() if match else None
        
        num1 = extract_number(address1)
        num2 = extract_number(address2)
        
        # Find column indexes of addresses
        index1 = None
        index2 = None
        
        for i, address in enumerate(self.addresses):
            normalized = address.lower()
            
            #Match address1
            if num1:
                if num1 in normalized:
                    index1 = i
            else:
                if address1.lower() in normalized:
                    index1 = i
            
            #Match address2
            if num2:
                if num2 in normalized:
                    index2 = i
            else:
                if address2.lower() in normalized:
                    index2 = i
                
        if index1 is None or index2 is None:
            print("FAILED LOOKUP")
            print("Address1: ", address1)
            print("Address2: ", address2)
            raise ValueError("Address not found in distance table")

        distance = self.distances[index1][index2]

        # If empty, check opposite direction
        if distance == "":
            distance = self.distances[index2][index1]

        return float(distance)