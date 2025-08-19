from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base


class Crop(Base):
    __tablename__ = "crops"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)


class Weed(Base):
    __tablename__ = "weeds"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)


class CoverCrop(Base):
    __tablename__ = "cover_crops"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, index=True)


class Allelochemical(Base):
    __tablename__ = "allelochemicals"
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    source_cover_crop_id = Column(Integer, ForeignKey("cover_crops.id"))
    effect_on_weed_id = Column(Integer, ForeignKey("weeds.id"))
    effect = Column(String)  # inhibit, promote, neutral
    evidence_strength = Column(Float)  # 0..1


class SoilSample(Base):
    __tablename__ = "soil_samples"
    id = Column(Integer, primary_key=True)
    n = Column(Float)
    p = Column(Float)
    k = Column(Float)
    ph = Column(Float)
    organic_matter = Column(Float)
    ec = Column(Float)
    texture = Column(String)

