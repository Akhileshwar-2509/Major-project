from fastapi import APIRouter, Response
from pydantic import BaseModel
from typing import List
import csv
import io

router = APIRouter()


class Advisory(BaseModel):
    crop: str
    predicted_yield_per_acre: float
    ci_low: float
    ci_high: float
    cover_recs: List[str]
    fertilizer_schedule: List[str]


@router.post("/csv")
def export_csv(advisory: Advisory):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["crop", advisory.crop])
    writer.writerow(["yield_bu_ac", advisory.predicted_yield_per_acre])
    writer.writerow(["ci_low", advisory.ci_low])
    writer.writerow(["ci_high", advisory.ci_high])
    writer.writerow(["cover_recommendations"])
    for r in advisory.cover_recs:
        writer.writerow([r])
    writer.writerow(["fertilizer_schedule"])
    for line in advisory.fertilizer_schedule:
        writer.writerow([line])
    csv_bytes = output.getvalue().encode()
    return Response(content=csv_bytes, media_type="text/csv", headers={"Content-Disposition": "attachment; filename=advisory.csv"})

