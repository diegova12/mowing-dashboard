# Landscaping Dashboard

A full-stack web application to manage, visualize, and forecast landscaping job schedules, routes, and revenues. This project features a FastAPI backend connected to a PostgreSQL/PostGIS database and a Streamlit frontend dashboard with interactive visualizations (calendar, map view, financials, and forecasting).

---

## Project Overview

The Landscaping Dashboard helps a landscaping business:

- **Schedule & Manage Jobs:** View and drag-and-drop jobs on a calendar.  
- **Optimize Routes:** Compute the optimal route for crews each day.  
- **Visualize Locations:** Plot jobs on a Mapbox/OpenStreetMap view.  
- **Track Financials:** Aggregate monthly and per-service revenue with interactive bar charts.  
- **Forecast Revenue:** Generate a 12-month revenue forecast using Prophet.  
- **Weather Alerts:** Display current weather and tomorrow’s rain/freeze warnings based on job locations.  

---

## Features

- **Interactive Calendar (FullCalendar via Streamlit Component)**  
  - Monthly view with draggable job events  
  - Live rescheduling via PATCH calls to the backend  
- **Map View & Route Optimization**  
  - Plot current job locations on a map  
  - “Optimize Today’s Route” button calls backend TSP solver  
- **Financial Dashboard**  
  - Monthly revenue by service bar chart  
  - KPIs: jobs today, revenue today, revenue this month, unique clients  
- **Prophet Forecast**  
  - 12-month revenue projection (with historical line fallback when data is insufficient)  
- **Weather Sidebar**  
  - Fetch current weather from OpenWeatherMap for first job location  
  - Show rain/freeze warnings for tomorrow  
- **Database (PostgreSQL + PostGIS)**  
  - Stores clients, crews, jobs (with geometry), payments  
  - Alembic migrations for schema versioning  
- **Seed Data Script**  
  - Populate sample clients, crews, jobs, and payments  
  - Can be customized for additional dummy data  

---

## Tech Stack

- **Backend**:  
  - Python 3.13  
  - FastAPI  
  - SQLAlchemy (ORM)  
  - Alembic (migrations)  
  - PostgreSQL + PostGIS (geometry)  
  - Uvicorn (ASGI server)  
- **Frontend**:  
  - Python 3.13  
  - Streamlit  
  - Plotly (express & graph_objects)  
  - `streamlit-calendar-semver` (FullCalendar integration)  
  - Pandas, Prophet (for forecasting)  
- **Other**:  
  - Docker (optional, for local Postgres)  
  - `dotenv` (environment variables)  
  - Requests (HTTP client)  
  - Faker (seed data generation)  

---

## Screenshots

<details>
<summary>Click to expand sample app screenshots</summary>

1. **Landing Dashboard & KPI Cards**  
<img width="1459" alt="Screenshot 2025-06-01 at 9 40 43 PM" src="https://github.com/user-attachments/assets/ea669c5b-b0e3-420b-a3c8-d1a61ffb0b4d" />


2. **Calendar View (FullCalendar)**  
<img width="993" alt="Screenshot 2025-06-01 at 9 41 16 PM" src="https://github.com/user-attachments/assets/53873b54-6397-46c4-b4c8-afcd3b38bca3" />

3. **Map View & Route Optimization**  
<img width="1015" alt="Screenshot 2025-06-01 at 9 42 05 PM" src="https://github.com/user-attachments/assets/7adf4b21-716d-4c9f-a16b-81344e07ec5f" />
<img width="1000" alt="Screenshot 2025-06-01 at 9 42 21 PM" src="https://github.com/user-attachments/assets/4315f2c2-3a02-4bb2-826d-e8f1d3287f83" />

4. **Financials (Monthly Revenue by Service)**  
<img width="997" alt="Screenshot 2025-06-01 at 9 42 43 PM" src="https://github.com/user-attachments/assets/2cf415f6-8f5e-4475-855a-5fd80f1fce97" />

5. **Revenue Forecast (Prophet)**  
<img width="1020" alt="Screenshot 2025-06-01 at 9 42 58 PM" src="https://github.com/user-attachments/assets/17257539-eb1e-40f1-b115-a2e38d7eadcc" />

6. **Weather Alerts Sidebar**  
<img width="337" alt="Screenshot 2025-06-01 at 9 43 16 PM" src="https://github.com/user-attachments/assets/593327cb-0e46-425f-bc5f-87895d037eb1" />

</details>
