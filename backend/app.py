# backend/app.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from datetime import date
import numpy as np
from ortools.constraint_solver import pywrapcp, routing_enums_pb2

from backend.models import Base, Job
from backend.crud import engine, get_db
from backend.schemas import JobSchema, JobCreate

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Landscaping Dashboard API",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Jobs Endpoint 
@app.get("/jobs/", response_model=List[JobSchema])
def read_jobs(db: Session = Depends(get_db)):
    return db.query(Job).all()


# Reschedule Endpoint
class RescheduleRequest(BaseModel):
    scheduled: date

@app.patch("/jobs/{job_id}/reschedule", response_model=JobSchema)
def reschedule_job(
    job_id: int,
    payload: RescheduleRequest,
    db: Session = Depends(get_db),
):
    job = db.query(Job).get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    job.scheduled = payload.scheduled
    db.commit()
    db.refresh(job)
    return job


# Route Optimization Endpoint 
class OptimizeRequest(BaseModel):
    coords: List[dict] 
    
@app.post("/optimize/")
def optimize_route(req: OptimizeRequest):
    coords = req.coords
    n = len(coords)
    if n < 2:
        return {"route": list(range(n))}

    dist_matrix = []
    for i in range(n):
        xi, yi = coords[i]["latitude"], coords[i]["longitude"]
        row = []
        for j in range(n):
            xj, yj = coords[j]["latitude"], coords[j]["longitude"]
            d = np.hypot(xi - xj, yi - yj)
            row.append(int(d * 100000))
        dist_matrix.append(row)

    manager = pywrapcp.RoutingIndexManager(n, 1, 0)
    routing = pywrapcp.RoutingModel(manager)
    def distance_callback(from_index, to_index):
        return dist_matrix[
            manager.IndexToNode(from_index)
        ][
            manager.IndexToNode(to_index)
        ]
    transit_idx = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_idx)
    search_params = pywrapcp.DefaultRoutingSearchParameters()
    search_params.time_limit.seconds = 2

    solution = routing.SolveWithParameters(search_params)
    if not solution:
        raise HTTPException(status_code=500, detail="No route found")

    # Extract the route order
    index = routing.Start(0)
    route = []
    while not routing.IsEnd(index):
        route.append(manager.IndexToNode(index))
        index = solution.Value(routing.NextVar(index))

    return {"route": route}
