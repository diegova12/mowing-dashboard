# Landscaping Dashboard

A full-stack scheduling & analytics dashboard for a small landscaping business.  
Built with **FastAPI** + **SQLAlchemy** + **PostgreSQL** on the backend, and **Streamlit** + **Plotly** + **FullCalendar** on the frontend.

## Features

- **Job CRUD & Rescheduling** via REST  
- **Drag-and-drop** calendar view (FullCalendar)  
- **Route optimization** (TSP via OR-Tools)  
- **Map view** of job locations  
- **Financial analytics** & **monthly revenue** charts  
- **Prophet**-powered **12-month revenue forecast**  
- **Real-time weather alerts** (OpenWeatherMap API)  

---

## Quickstart

### 1. Clone & Install

```bash
git clone https://github.com/your-username/landscaping-dashboard.git
cd landscaping-dashboard

# Backend dependencies
pip install fastapi uvicorn sqlalchemy psycopg2-binary alembic ortools

# Frontend dependencies
pip install streamlit pandas requests plotly prophet python-dotenv streamlit-calendar-semver
