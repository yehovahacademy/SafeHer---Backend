
from pydantic import BaseModel


class Landmark(BaseModel):
    name: str
    longitude: float
    latitude: float
    type: str


class LandmarkResponse(BaseModel):
    landmarks: list[Landmark]
