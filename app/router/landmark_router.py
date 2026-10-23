
from fastapi import APIRouter

from app.data.landmarks import LANDMARKS
from app.schemas.landmark_schema import LandmarkResponse


router = APIRouter(
    prefix="/landmarks",
    tags=["Landmarks"],
)


@router.get("", response_model=LandmarkResponse)
def get_landmarks():
    return {
        "landmarks": [
            {
                "name": name,
                "longitude": details["coordinates"][0],
                "latitude": details["coordinates"][1],
                "type": details["type"],
            }
            for name, details in LANDMARKS.items()
        ]
    }
