
import os
from typing import Any

import httpx
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.data.landmarks import LANDMARKS
from app.router.landmark_router import router as landmark_router
from app.router.routes import router as routes_router


app = FastAPI(
    title="SafeHer API",
    description=(
        "Mumbai route-awareness prototype. "
        "Route options are not assessed for personal safety."
    ),
    version="1.0.0",
)


app.include_router(landmark_router)
app.include_router(routes_router)

# Local development origins plus an optional deployed frontend origin.
allowed_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

frontend_origins = os.getenv("SAFEHER_FRONTEND_ORIGIN", "")
allowed_origins.extend(
    origin.strip()
    for origin in frontend_origins.split(",")
    if origin.strip()
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=list(set(allowed_origins)),
    allow_methods=["GET"],
    allow_headers=["*"],
)




SAFETY_NOTICE = (
    "These are driving routes, not verified safe walking routes. "
    "No route has been assessed for personal safety."
)


# API response models
class HealthResponse(BaseModel):
    status: str
    service: str


class Landmark(BaseModel):
    name: str
    longitude: float
    latitude: float


class LandmarkResponse(BaseModel):
    landmarks: list[Landmark]


class RouteOption(BaseModel):
    route_id: int
    distance_km: float
    duration_minutes: float
    geometry: dict[str, Any]
    safety_status: str


class RouteResponse(BaseModel):
    origin: str
    destination: str
    transport_mode: str
    routes: list[RouteOption]
    notice: str


@app.get("/")
def home():
    return {
        "message": "SafeHer API is running",
        "city": "Mumbai",
        "version": "1.0.0",
        "purpose": "Route awareness prototype",
    }


@app.get("/health", response_model=HealthResponse)
def health_check():
    return {
        "status": "healthy",
        "service": "safeher-api",
    }


@app.get("/landmarks", response_model=LandmarkResponse)
def get_landmarks():
    return {
        "landmarks": [
            {
                "name": name,
                "longitude": coordinates[0],
                "latitude": coordinates[1],
            }
            for name, coordinates in LANDMARKS.items()
        ]
    }


@app.get("/route", response_model=RouteResponse)
async def get_route(
    origin: str = Query(..., min_length=1, max_length=80),
    destination: str = Query(..., min_length=1, max_length=80),
):
    # Normalize whitespace, but preserve the official landmark names.
    origin = origin.strip()
    destination = destination.strip()

    if origin not in LANDMARKS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported origin. Choose from: {', '.join(LANDMARKS)}",
        )

    if destination not in LANDMARKS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported destination. Choose from: {', '.join(LANDMARKS)}",
        )

    if origin == destination:
        raise HTTPException(
            status_code=400,
            detail="Origin and destination must be different.",
        )

    start = LANDMARKS[origin]
    end = LANDMARKS[destination]

    url = (
        "https://router.project-osrm.org/route/v1/driving/"
        f"{start[0]},{start[1]};{end[0]},{end[1]}"
    )

    params = {
        "alternatives": "true",
        "overview": "full",
        "geometries": "geojson",
        "steps": "false",
    }

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="The routing service timed out. Please try again.",
        )

    except httpx.HTTPError:
        raise HTTPException(
            status_code=502,
            detail="The routing service is temporarily unavailable.",
        )

    except ValueError:
        raise HTTPException(
            status_code=502,
            detail="The routing service returned an invalid response.",
        )

    if not isinstance(data, dict):
        raise HTTPException(
            status_code=502,
            detail="Unexpected response from the routing service.",
        )

    if data.get("code") != "Ok":
        raise HTTPException(
            status_code=404,
            detail="No route was found between these landmarks.",
        )

    raw_routes = data.get("routes")

    if not isinstance(raw_routes, list) or not raw_routes:
        raise HTTPException(
            status_code=404,
            detail="No route was found between these landmarks.",
        )

    routes = []

    for index, route in enumerate(raw_routes, start=1):
        if not isinstance(route, dict):
            continue

        geometry = route.get("geometry")
        distance = route.get("distance")
        duration = route.get("duration")

        # Reject malformed route records rather than returning broken data.
        if (
            not isinstance(geometry, dict)
            or geometry.get("type") != "LineString"
            or not isinstance(geometry.get("coordinates"), list)
            or not isinstance(distance, (int, float))
            or not isinstance(duration, (int, float))
            or distance < 0
            or duration < 0
        ):
            continue

        routes.append(
            {
                "route_id": index,
                "distance_km": round(distance / 1000, 2),
                "duration_minutes": round(duration / 60, 1),
                "geometry": geometry,
                "safety_status": "Not assessed",
            }
        )

    if not routes:
        raise HTTPException(
            status_code=502,
            detail="The routing service returned no usable route data.",
        )

    return {
        "origin": origin,
        "destination": destination,
        "transport_mode": "driving",
        "routes": routes,
        "notice": SAFETY_NOTICE,
    }
