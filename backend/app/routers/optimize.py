from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()


class OptimizeRequest(BaseModel):
    crop: str
    n: float
    p: float
    k: float
    season: str


class Dose(BaseModel):
    time: str
    n: float
    p: float
    k: float
    note: str


class OptimizeResponse(BaseModel):
    schedule: List[Dose]


@router.post("/fertilizer", response_model=OptimizeResponse)
def optimize_fertilizer(req: OptimizeRequest):
    total_n, total_p, total_k = req.n, req.p, req.k
    split = [0.5, 0.3, 0.2]
    times = ["basal", "tillering/veg", "pre-flowering"]
    notes = [
        "Incorporate before sowing",
        "Apply with irrigation",
        "Side-dress before flowering",
    ]
    schedule: List[Dose] = []
    for frac, t, note in zip(split, times, notes):
        schedule.append(
            Dose(time=t, n=round(total_n * frac, 1), p=round(total_p * frac, 1), k=round(total_k * frac, 1), note=note)
        )
    return OptimizeResponse(schedule=schedule)

