
from typing import Any

from pydantic import BaseModel


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
