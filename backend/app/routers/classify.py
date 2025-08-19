from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()


class ClassifyRequest(BaseModel):
    weeds: List[str]
    crop: str


class WeedClass(BaseModel):
    name: str
    label: str
    explanation: str


class ClassifyResponse(BaseModel):
    weeds: List[WeedClass]


WEED_EFFECTS = {
    ("amaranthus", "maize"): ("harmful", "competes for N and light; allelochemicals from maize less effective"),
    ("trifolium", "wheat"): ("beneficial", "fixes N and can suppress take-all when used as cover"),
}


@router.post("/weed", response_model=ClassifyResponse)
def classify_weeds(req: ClassifyRequest):
    results: List[WeedClass] = []
    for w in req.weeds:
        key = (w.lower(), req.crop.lower())
        if key in WEED_EFFECTS:
            label, explanation = WEED_EFFECTS[key]
        else:
            label, explanation = "neutral", "no strong documented allelopathic interaction"
        results.append(WeedClass(name=w, label=label, explanation=explanation))
    return ClassifyResponse(weeds=results)

