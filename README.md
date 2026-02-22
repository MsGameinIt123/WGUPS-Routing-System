# WGUPS Routing System
A Python-based logistics routing simulation that optimizes delivery routes while meeting strict delivery deadlines and operational constraints.
## Overview
This program simulates the Wester Governors University Parcel Service (WGUPS) delivery operation. It calculates efficient delivery routes, tracks package status over time, and ensures all deliveries meet deadlines while minimizing mileage.
## Features
- Greedy nearest-neighbor routing algorithm
- Deadline-aware delivery priorization
- Time-based package status tracking
- Delayed shipment handling
- Dynamic address correction handling
- Supervisor lookup interface
- Custom hash table for efficient package storage
- Total mileage optimization ( < 140 miles)
## Algorithms & Data Structures
- Greedy Nearest Neighbor Algorithm for route optimization
- Custom Hash Table for O(1) package lookup
- Constraint-based routing adjustments for deadline compliance
## Delivery Constraints Modeled
- Package deadlines (10:30 AM & EOD)
- Delayed flight arrivals (9:05 AM)
- Address correction timing (10:20 AM)
- Truck capacity limits
- Two-driver operational constraints
## Example Output
## Supervisor Interface
Users can:
- Lookup package status at any time
- View all package statuses at a specific time
- Track delivery progress
## How to Run
1. Clone the repository
2. Ensure Python 3.9+ is installed
3. Run:
## Technologies Used
- Python
- Algorithm Design
- Data Structures
- Time-based simulation logic
## Learning Outcomes
This project demonstrates:
- algorithmic problem solving
- logistics optimization
- time-based system modeling
- custom data structure implementation
- real-world constraint handling