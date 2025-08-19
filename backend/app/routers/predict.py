from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List, Optional
import numpy as np

router = APIRouter()


class SoilInput(BaseModel):
    n: float = Field(..., description="Nitrogen (ppm)")
    p: float = Field(..., description="Phosphorus (ppm)")
    k: float = Field(..., description="Potassium (ppm)")
    ph: float
    organic_matter: float
    ec: float
    texture: str


class PredictRequest(BaseModel):
    soil: SoilInput
    crop: str
    candidate_cover_crops: List[str] = []
    weed_species: List[str] = []
    location: str
    season: str


class PredictResponse(BaseModel):
    predicted_yield_per_acre: float
    lower_ci: float
    upper_ci: float


@router.post("/yield", response_model=PredictResponse)
def predict_yield(req: PredictRequest):
    # Placeholder baseline model: simple linear heuristic for demo
    base = 0.1 * req.soil.n + 0.08 * req.soil.p + 0.06 * req.soil.k
    ph_adj = -abs(req.soil.ph - 6.5) * 1.5
    om_adj = min(req.soil.organic_matter, 6.0) * 0.8
    weather_adj = 5.0  # pretend fetched
    cover_bonus = 2.0 * len(req.candidate_cover_crops)
    weed_penalty = -1.5 * len(req.weed_species)
    pred = max(0.0, base + ph_adj + om_adj + weather_adj + cover_bonus + weed_penalty)
    std = max(1.0, 0.15 * pred)
    return PredictResponse(
        predicted_yield_per_acre=round(pred, 2),
        lower_ci=round(max(0.0, pred - 1.96 * std), 2),
        upper_ci=round(pred + 1.96 * std, 2),
    )

