import csv
from pathlib import Path
from .db import Base, engine, SessionLocal
from .models import Crop, Weed, CoverCrop, Allelochemical


def run_seed(data_dir: str):
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        # seed basic entities
        for name in ["maize", "wheat", "soybean"]:
            if not session.query(Crop).filter_by(name=name).first():
                session.add(Crop(name=name))
        for name in ["amaranthus", "lolium", "trifolium"]:
            if not session.query(Weed).filter_by(name=name).first():
                session.add(Weed(name=name))
        for name in ["rye", "mustard", "clover"]:
            if not session.query(CoverCrop).filter_by(name=name).first():
                session.add(CoverCrop(name=name))
        session.commit()

        # seed allelopathy CSV
        csv_path = Path(data_dir) / "seed_allelopathy.csv"
        if csv_path.exists():
            with csv_path.open() as f:
                reader = csv.DictReader(f)
                for row in reader:
                    cover = session.query(CoverCrop).filter_by(name=row["cover_crop"].lower()).first()
                    weed = None
                    if row["target_type"].lower() == "weed":
                        weed = session.query(Weed).filter_by(name=row["target"].lower()).first()
                    if cover and weed:
                        exists = (
                            session.query(Allelochemical)
                            .filter_by(
                                name=row["chemical"],
                                source_cover_crop_id=cover.id,
                                effect_on_weed_id=weed.id,
                                effect=row["effect"].lower(),
                            )
                            .first()
                        )
                        if not exists:
                            session.add(
                                Allelochemical(
                                    name=row["chemical"],
                                    source_cover_crop_id=cover.id,
                                    effect_on_weed_id=weed.id,
                                    effect=row["effect"].lower(),
                                    evidence_strength=float(row["evidence_strength"] or 0.5),
                                )
                            )
                session.commit()
    finally:
        session.close()


if __name__ == "__main__":
    run_seed(str(Path(__file__).resolve().parents[1] / "data"))

