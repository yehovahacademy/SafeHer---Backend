
import httpx
from fastapi import APIRouter, HTTPException, Query

from app.data.landmarks import LANDMARKS
from app.schemas.route_schema import RouteResponse


router = APIRouter(
    prefix="/route",
    tags=["Routes"],
)

SAFETY_NOTICE = (
    "These are driving routes, not verified safe walking routes. "
    "No route has been assessed for personal safety."
)


@router.get("", response_model=RouteResponse)
async def get_route(
    origin: str = Query(..., min_length=1, max_length=80),
    destination: str = Query(..., min_length=1, max_length=80),
):
    origin = origin.strip()
    destination = destination.strip()

    if origin not in LANDMARKS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported origin. Choose a listed Mumbai landmark.",
        )

    if destination not in LANDMARKS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported destination. Choose a listed Mumbai landmark.",
        )

    if origin == destination:
        raise HTTPException(
            status_code=400,
            detail="Origin and destination must be different.",
        )

    start = LANDMARKS[origin]["coordinates"]
    end = LANDMARKS[destination]["coordinates"]

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
            detail="The routing service returned invalid data.",
        )

    if not isinstance(data, dict) or data.get("code") != "Ok":
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

    for index, item in enumerate(raw_routes, start=1):
        if not isinstance(item, dict):
            continue

        geometry = item.get("geometry")
        distance = item.get("distance")
        duration = item.get("duration")

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

        routes.append({
            "route_id": index,
            "distance_km": round(distance / 1000, 2),
            "duration_minutes": round(duration / 60, 1),
            "geometry": geometry,
            "safety_status": "Not assessed",
        })

    if not routes:
        raise HTTPException(
            status_code=502,
            detail="The routing service returned no usable routes.",
        )

    return {
        "origin": origin,
        "destination": destination,
        "transport_mode": "driving",
        "routes": routes,
        "notice": SAFETY_NOTICE,
    }
