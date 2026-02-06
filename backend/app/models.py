from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class Claim(Base):
    __tablename__ = "claims"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    hash_key = Column(String, unique=True, index=True)
    status = Column(String, default="processing")
    
    # Analysis results
    entities = Column(JSON, nullable=True)
    summary = Column(Text, nullable=True)
    credibility_score = Column(Float, nullable=True)
    credibility_label = Column(String, nullable=True)
    explanation = Column(Text, nullable=True)
    
    # Vector ID for similarity search
    vector_id = Column(String, nullable=True)

    sources = relationship("Source", back_populates="claim")

class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    claim_id = Column(Integer, ForeignKey("claims.id"))
    url = Column(String, nullable=False)
    domain = Column(String, nullable=False)
    title = Column(String, nullable=True)
    snippet = Column(Text, nullable=True)
    published_at = Column(DateTime, nullable=True)
    source_type = Column(String, default="unknown")
    
    # Advanced Metadata
    is_archive = Column(Boolean, default=False)
    wayback_url = Column(String, nullable=True)
    domain_age_days = Column(Integer, nullable=True)

    claim = relationship("Claim", back_populates="sources")
