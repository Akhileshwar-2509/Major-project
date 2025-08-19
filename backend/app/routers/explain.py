from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()


class ExplainRequest(BaseModel):
    crop: str
    cover_crops: List[str]
    weeds: List[str]


class ExplainResponse(BaseModel):
    narrative: List[str]


@router.post("/why", response_model=ExplainResponse)
def explain(req: ExplainRequest):
    lines: List[str] = []
    for cover in req.cover_crops:
        if cover.lower() == "rye":
            lines.append("Rye releases benzoxazinoids that suppress Amaranthus germination, improving maize yield")
        if cover.lower() == "mustard":
            lines.append("Mustard residues release isothiocyanates which suppress small-seeded annual weeds")
    if not lines:
        lines.append("Recommendations are based on documented allelopathic interactions and soil-fit heuristics")
    return ExplainResponse(narrative=lines)

