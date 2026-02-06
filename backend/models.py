from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class Claim(Base):
    __tablename__ = "claims"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    hash_key = Column(String, unique=True, index=True)  # To avoid duplicates
    status = Column(String, default="processing") # processing, completed, error
    
    # Analysis results
    entities = Column(JSON, nullable=True) # Extracted people, orgs
    summary = Column(Text, nullable=True)
    credibility_score = Column(Integer, nullable=True) # 0-100
    credibility_label = Column(String, nullable=True) # High, Low, etc.
    explanation = Column(Text, nullable=True)

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
    source_type = Column(String, default="unknown") # news, blog, social, etc.
    credibility_rank = Column(String, nullable=True) # A, B, C, etc. based on domain

    claim = relationship("Claim", back_populates="sources")
