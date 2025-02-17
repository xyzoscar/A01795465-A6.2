# Hotel Reservation System  

This repository contains a **console-based hotel reservation system** that allows managing hotels, customers, and reservations. It supports **CRUD operations**, **data persistence using JSON files**, **input validation**, and **basic error handling**.  

## Features  

The system enables users to perform the following operations:  

### 1. Hotel Management  
**CRUD operations for hotels:**  
- Create a new hotel.  
- Delete an existing hotel.  
- Modify hotel details (location, rooms, email).  
- Display all available hotels.  

### 2. Customer Management  
**CRUD operations for customers:**  
- Create a new customer.  
- Delete an existing customer.  
- Modify customer details (name, phone).  
- Display all registered customers.  

### 3. Reservation Management  
**Manage reservations between customers and hotels:**  
- Create a reservation for a customer.  
- Cancel an existing reservation.  
- Automatically update hotel room availability.  

## Usage  

Ensure you have **Python 3.x** installed before running the system.  

### Running the application  

To start the hotel reservation system, run:

```bash
python main.py
```

For test coverage analysis, run:

```bash
coverage run -m unittest discover -s . -p "test_*.py"
coverage report
```