from dataclasses import dataclass
from typing import List, Dict, Tuple


@dataclass
class AllelopathyRule:
    cover_crop: str
    target: str  # weed or crop
    target_type: str  # 'weed' or 'crop'
    effect: str  # inhibit, promote, neutral
    chemical: str
    evidence_strength: float
    citation: str


RULES: List[AllelopathyRule] = [
    AllelopathyRule(
        cover_crop="rye",
        target="amaranthus",
        target_type="weed",
        effect="inhibit",
        chemical="benzoxazinoids (DIBOA, DIMBOA)",
        evidence_strength=0.8,
        citation="Barnes & Putnam 1983; Schulz et al. 2013",
    ),
    AllelopathyRule(
        cover_crop="mustard",
        target="lolium",
        target_type="weed",
        effect="inhibit",
        chemical="isothiocyanates (ITCs)",
        evidence_strength=0.7,
        citation="Brown & Morra 1997",
    ),
]


def get_rules_index() -> Dict[Tuple[str, str], AllelopathyRule]:
    return { (r.cover_crop.lower(), r.target.lower()): r for r in RULES }

