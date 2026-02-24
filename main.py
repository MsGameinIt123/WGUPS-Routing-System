#Madison Torres - Student ID #010869201 - C950 Task 2 WGUPS Routing Program
#This program simulates the WGUPS delivery routing program.
#It uses a custom hash table to store package data and a greedy nearest neighbor algorithm to determine efficient delivery routes.
#The program tracks mileage, delivery times, and allows supervisor queries for package status at any time during the day.

import csv
from package import Package
from hashtable import HashTable
from truck import Truck
from distance import DistanceTable
from datetime import timedelta

def load_packages(filename, hash_table):
    """Loads package data from CSV into the hash table. Initializes package attributes and flags delayed shipments."""
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader) #Skip header row
        
        #packages delayed on flight until 9:05 AM
        delayed_ids = {6, 25, 28, 32}
        
        for row in reader:
            
            #Skip empty rows
            if not row or not row[0].strip().isdigit():
                continue
            
            package_id = int(row[0])
            address = row[1]
            city = row[2]
            zip_code = row[4]
            deadline = row[5]
            weight = row[6]
            notes = row[7] if len(row) > 7 else ""
            
            package = Package(
                package_id,
                address,
                city,
                zip_code,
                deadline,
                weight,
                notes
            )
            
            #store original address for package 9 timeline display
            package.original_address = address
            
            #mark delayed packages
            if package_id in delayed_ids:
                package.delayed_until = timedelta(hours=9, minutes=5)
                package.status = "Delayed on flight"
            
            hash_table.insert(package_id, package)

#Uses a greedy nearest neighbor algorithm.
#At each step, the truck selects the closest undelivered package based on the distance table.
#Travel time is calculated using an average speed of 18 mph, and package status is updated upon delivery.        
def deliver_packages(truck, distance_table):
    """Delivers all packages assigned to a truck. Uses a nearest-neighbour routing strategy while prioritizing deadline-sensitive packages. Updates mileage, time, and delivery status."""
    while truck.packages:
        nearest_package = None
        shortest_distance = float('inf')
        priority = False
        
        for package in truck.packages:
            
            if hasattr(package, "correction_time"):
                if truck.current_time >= package.correction_time:
                    package.address = "410 S State St"
            
            distance = distance_table.get_distance(
                truck.current_location,
                package.address
            )
            
            deadline_priority = package.deadline != "EOD"
            
            if nearest_package is None:
                nearest_package = package
                shortest_distance = distance
                priority = deadline_priority
            elif deadline_priority and not priority:
                nearest_package = package
                shortest_distance = distance
                priority = True
            elif deadline_priority == priority and distance < shortest_distance:
                nearest_package = package
                shortest_distance = distance
                
        #Travel to the nearest package
        travel_time = timedelta(hours=shortest_distance / 18)
        truck.current_time += travel_time
        truck.mileage += shortest_distance
        truck.current_location = nearest_package.address
        
        #Deliver ALL packages at this address
        delivered = []
        
        for package in truck.packages:
            if package.address == truck.current_location:
                package.status = "Delivered"
                package.delivery_time = truck.current_time
                delivered.append(package)
                
        for package in delivered:
            truck.packages.remove(package)
            
def load_truck(truck, package_ids, package_table):
    delayed_packages = {6, 25, 28, 32}
    
    for pid in package_ids:
        package = package_table.lookup(pid)
        if package:
            #Do not load delayed packages yet
            if pid in delayed_packages:
                continue
            package.status = "En route"
            package.departure_time = truck.current_time
            package.truck_id = truck.truck_id
            truck.packages.append(package)

#Returns the truck to the hub after completing deliveries.
#This ensures mileage and time are calculated accurately and models real driver availability.
def return_to_hub(truck, distance_table):
    distance = distance_table.get_distance(
        truck.current_location,
        "Western Governors University"
    )
    
    travel_time = timedelta(hours=distance / 18)
    
    truck.current_time += travel_time
    truck.mileage += distance
    truck.current_location = "Western Governors University"
    
def get_package_status_at_time(package, query_time):
    """Returns the delivery status of a package at a specific time. Handles delayed arrivals, en route status, and completed deliveries."""
    #delayed flight packages
    if hasattr(package, "delayed_until"):
        if query_time < package.delayed_until:
            return "Delayed (arrives at 9:05)"
    
    if package.delivery_time and query_time >= package.delivery_time:
        return f"Delivered at {package.delivery_time}"
    
    if hasattr(package, "departure_time") and query_time >= package.departure_time:
        return "En route"
    return "At hub"

def print_truck_status(truck_id_list, time_string, package_table):
    hours, minutes = map(int, time_string.split(":"))
    query_time = timedelta(hours=hours, minutes=minutes)
    
    print(f"\nTruck status at {time_string}")
    print("-" * 40)
    
    for pid in truck_id_list:
        package = package_table.lookup(pid)
        status = get_package_status_at_time(package, query_time)
        print(f"Package {pid}: {status}")
        
def get_address_at_time(package, query_time):
    if hasattr(package, "correction_time") and package.correction_time:
        if query_time < package.correction_time:
            return package.original_address
    return package.address

def deliver_priority_package(truck, package, distance_table):
    """Immediately delivers a priority package. Used to ensure deadline-critical packages are delivered before time constraints."""
    distance = distance_table.get_distance(
        truck.current_location,
        package.address
    )
    travel_time = timedelta(hours=distance / 18)
    
    truck.current_time += travel_time
    truck.mileage += distance
    truck.current_location = package.address
    
    package.status = "Delivered"
    package.delivery_time = truck.current_time
    
    truck.packages.remove(package)
            
def main():
    package_table = HashTable()
    load_packages("data/packages.csv", package_table)
    
    distance_table = DistanceTable()
    distance_table.load_distances("data/distances.csv")
    
    truck1 = Truck(1)
    truck2 = Truck(2)
    truck3 = Truck(3)
    
    #Assign package IDs to each truck (9 will be added later as per assignment requirement)
    truck1_ids = [1, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40]       
    truck2_ids = [3, 18, 36, 38, 2, 4, 5, 7, 8, 10, 11, 21, 22, 23, 24]
    truck3_ids = [12, 17, 26, 27, 33, 35, 39]
    
    #Load trucks
    load_truck(truck1, truck1_ids, package_table)
    load_truck(truck2, truck2_ids, package_table)
    load_truck(truck3, truck3_ids, package_table)
    
    #Deliver Trucks 1 and 2
    deliver_packages(truck1, distance_table)
    return_to_hub(truck1, distance_table)
    
    deliver_packages(truck2, distance_table)
    return_to_hub(truck2, distance_table)
    
    #Only two drivers are available.
    #Truck 3 departs when the earliest driver returns to the hub.
    earliest_return = min(truck1.current_time, truck2.current_time)
    truck3.current_time = earliest_return
    
    #delayed packages
    delay_time = timedelta(hours=9, minutes=5)

    driver_available_time = min(truck1.current_time, truck2.current_time)
    delay_time = timedelta(hours=9, minutes=5)
    truck3.current_time = max(driver_available_time, delay_time)
        
    for pid in [6, 25, 28, 32]:
        pkg = package_table.lookup(pid)
        if pkg:
            pkg.status = "En route"
            pkg.departure_time = truck3.current_time
            pkg.truck_id = truck3.truck_id
            truck3.packages.append(pkg)
    
    #Prioritize package 6 and 25 (10:30 deadline)
    
    pkg6 = package_table.lookup(6)
    pkg25 = package_table.lookup(25)
    
    dist6 = distance_table.get_distance(truck3.current_location, pkg6.address)
    dist25 = distance_table.get_distance(truck3.current_location, pkg25.address)
    
    if dist25 < dist6:
        deliver_priority_package(truck3, pkg25, distance_table)
        deliver_priority_package(truck3, pkg6, distance_table)
    else:
        deliver_priority_package(truck3, pkg6, distance_table)
        deliver_priority_package(truck3, pkg25, distance_table)
    
    #Package 9 has an incorrect address that is corrected at 10:20 AM.
    #Truck 3 departure time is adjusted if necessary to ensure the address correction occurs before delivery.
    correction_time = timedelta(hours=10, minutes=20)
    package9 = package_table.lookup(9)
    
    package9.correction_time = correction_time
    package9.status = "At hub"
            
    if truck3.current_time < correction_time:
        truck3.current_time = correction_time

    package9.status = "En route"
    package9.departure_time = truck3.current_time
    package9.truck_id = truck3.truck_id
    truck3.packages.append(package9)
    
    #Deliver Truck 3
    deliver_packages(truck3, distance_table)
    return_to_hub(truck3, distance_table)
    
    #Calculate total mileage
    total_mileage = truck1.mileage + truck2.mileage + truck3.mileage
    
    #Output mileage and time for returned trucks
    print(f"Truck 1 mileage: {truck1.mileage:.3f}")
    print(f"Truck 2 mileage: {truck2.mileage:.3f}")
    print(f"Truck 3 mileage: {truck3.mileage:.3f}")
    
    print("Truck 1 return time: ", truck1.current_time)
    print("Truck 2 return time: ", truck2.current_time)
    print("Truck 3 return time: ", truck3.current_time)
    
    print(f"Total mileage: {total_mileage:.3f}")
    
    #Supervisor interface allows lookup of package status at any specified time.
    #Status transitions between "At hub", "En route", and "Delivered" are determined dynamically based on departure and delivery timestamps.
    while True:
        print("\nSupervisor Menu")
        print("1. Lookup Package by ID")
        print("2. View ALL Packages at a Specific Time")
        print("3. Exit")
        
        choice = input("Enter choice: ")
        
        if choice == "1":
            try:
                package_id = int(input("Enter package ID: "))
                time_input = input("Enter time (HH:MM, 24-hour format): ")
                
                hours, minutes = map(int, time_input.split(":"))
                query_time = timedelta(hours=hours, minutes=minutes)
                
                package = package_table.lookup(package_id)
                
                if package:
                    status = get_package_status_at_time(package, query_time)
                    print(f"\nPackage ID: {package.package_id}")
                    display_address = get_address_at_time(package, query_time)
                    print(f"Address: {display_address}")
                    print(f"Deadline: {package.deadline}")
                    print(f"Weight: {package.weight}")
                    print(f"Status at {time_input}: {status}")
                    print(f"Truck: {getattr(package, 'truck_id', 'N/A')}")
                else:
                    print("Package not found.")
            except:
                print("Invalid input")
        elif choice == "2":
            try:
                time_input=input("Enter time (HH:MM): ")
                hours, minutes = map(int, time_input.split(":"))
                query_time = timedelta(hours=hours, minutes=minutes)
            
                print("\nAll Package Statuses at ", time_input)
                print("-" * 60)
            
                for pid in range(1, 41):
                    package = package_table.lookup(pid)
                    status = get_package_status_at_time(package, query_time)
                    address = get_address_at_time(package, query_time)
                
                    print(
                        f"ID: {package.package_id} | "
                        f"{address} | "
                        f"Deadine: {package.deadline} | "
                        f"{status} | "
                        f"Truck: {getattr(package, 'truck_id', 'N/A')}"
                    )
            except:
                print("Invalid time format")
        elif choice == "3":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":

    main()
