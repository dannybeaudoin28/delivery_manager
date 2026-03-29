# Delivery Route Optimization System

A full-stack Django application that manages delivery queues and generates optimized delivery routes using real-time routing data.

## Overview

This project simulates a delivery management system for small businesses (e.g., pizzerias) where dispatchers can:

 Add and manage delivery orders
 Assign deliveries to drivers
 Generate optimized delivery routes
 Track delivery status in real-time

The system integrates with the **Google Routes API** to dynamically calculate efficient routes based on distance and travel time.

---

## Features

### Delivery Management

* Add new deliveries with address → auto-geocoded to coordinates
* View all deliveries (assigned and unassigned)
* Delete individual or all unassigned deliveries
* Mark deliveries as **Delivered**
* Automatically frees driver when route is completed

### Route Generation

* Generate optimized routes using a greedy nearest-neighbor approach
* Calculates:

  * Distance between stops
  * Time between stops
  * Total route distance and duration
* Assigns route to selected driver
* Prevents assigning routes to drivers already in use

### Driver Management

* Drivers created via Django Admin
* Dropdown selection in UI
* One-to-one relationship with routes

### Architecture

 **Command Pattern** for business logic (e.g., `GenerateRouteCommand`)
 **Repository Pattern** for database abstraction
 **Factory Pattern** for creation of different Delivery types
 Clean separation of:

   Views (UI logic)
   Services (routing logic)
   Commands (actions)
   Models (data)

---

## Tech Stack

 **Backend:** Django (Python)
 **Database:** MySQL (Google Cloud SQL via Proxy)
 **API:** Google Routes API
 **Frontend:** Django Templates + CSS
 **Other Libraries:**

   `requests`
   `geocoder`
   `polyline`
   `python-dotenv`

---

## Project Structure

```
myproject/
│
├── deliverymanager/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── commands/
│   ├── repositories/
│   ├── services/
│   └── templates/
│
├── myproject/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── proxy/              # (ignored in Git)
├── venv/               # (ignored in Git)
├── requirements.txt
└── manage.py
```

---

## Environment Variables

Create a `.env` file in the project root:

```
STORE_LATITUDE=44.2185282
STORE_LONGITUDE=-76.5713825

ROUTES_API_KEY=your_google_routes_api_key
ROUTES_GROUP_API_URL=https://routes.googleapis.com/distanceMatrix/v2:computeRouteMatrix
```

---
## Quick Setup
1. Navigate to project route directory
2. Open terminal
3. Run: .\start.ps1

## Detailed Setup Instructions

### 1. Clone the repository / Navigate inside with a CLI


### 2. Create virtual environment

```
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Start Cloud SQL Proxy

```
.\path_to_proxy\cloud-sql-proxy.exe --credentials-file="path/key.json" --port=3306 PROJECT:REGION:INSTANCE
```

### 5. Run migrations

```
python manage.py migrate
```

### 6. Create admin user

```
python manage.py createsuperuser
```

### 7. Run server

```
python manage.py runserver
```

---

## Usage

1. Go to `/admin` → create drivers
2. Open dashboard
3. Add deliveries
4. Select a driver
5. Click **Generate Route**
6. View optimized route and stop order
7. Mark deliveries as completed

---

## How Routing Works

The routing system uses a **greedy nearest-neighbor algorithm**:

1. Start at origin (home/store)
2. Query Google Route Matrix API
3. Select closest valid destination
4. Repeat until all deliveries are assigned

Each step stores:

 Distance from previous stop
 Time from previous stop

---

## Future Improvements

 Map visualization (Google Maps / Leaflet)
 Real-time updates with WebSockets
 Smarter routing (TSP optimization)
 Driver mobile interface
 Authentication system

---

## Notes

 The `proxy/` folder and credentials are excluded from Git for security
 A Cloud SQL proxy is required for database connectivity
 Designed with scalability and clean architecture in mind

---

## Author

Danny Beaudoin
Software Engineering Technology @ McMaster University
28 March 2026

---