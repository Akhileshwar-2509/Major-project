from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict

router = APIRouter()


class RecommendRequest(BaseModel):
    crop: str
    soil_texture: str
    weed_species: List[str] = []
    candidates: List[str] = []


class CoverRec(BaseModel):
    name: str
    score: float
    reasons: List[str]


class RecommendResponse(BaseModel):
    recommendations: List[CoverRec]


ALLELO_RULES = {
    ("rye", "amaranthus"): ("inhibit", "benzoxazinoids suppress amaranthus germination"),
    ("mustard", "lolium"): ("inhibit", "isothiocyanates reduce ryegrass emergence"),
}


@router.post("/cover", response_model=RecommendResponse)
def recommend_cover(req: RecommendRequest):
    recs: List[CoverRec] = []
    for cand in req.candidates:
        score = 50.0
        reasons: List[str] = []
        for weed in req.weed_species:
            key = (cand.lower(), weed.lower())
            if key in ALLELO_RULES:
                eff, why = ALLELO_RULES[key]
                if eff == "inhibit":
                    score += 15.0
                elif eff == "promote":
                    score -= 20.0
                reasons.append(f"{cand} vs {weed}: {why}")
        if req.soil_texture.lower() in ["sandy", "loamy"] and cand.lower() == "rye":
            score += 5
            reasons.append("Rye improves aggregation in sandy/loamy soils")
        recs.append(CoverRec(name=cand, score=round(score, 1), reasons=reasons))

    recs.sort(key=lambda r: r.score, reverse=True)
    return RecommendResponse(recommendations=recs)

