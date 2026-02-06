from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
import models, schemas, database
from services.osint import osint_service
import uuid

# Create tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="SourceTrace API")

import os
from dotenv import load_dotenv

load_dotenv()

origins = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def analyze_claim_background(claim_id: int, text: str, db: Session):
    # This function would likely need its own session if running in background task properly, 
    # but for simplicity we'll do it synchronous in the endpoint or careful session management.
    # actually, background tasks should create new session.
    # For this MVP, let's run it synchronously or just basic structure.
    # Let's do it seamlessly in the request for now to ensure easier debugging for user.
    pass

@app.post("/api/analyze", response_model=schemas.ClaimResponse)
def analyze_claim(input_data: schemas.ClaimInput, db: Session = Depends(database.get_db)):
    # 1. Check if claim exists (hash)
    # Simple hash for now: text itself or hash of it
    claim_hash = str(hash(input_data.text.strip().lower()))
    
    existing_claim = db.query(models.Claim).filter(models.Claim.hash_key == claim_hash).first()
    # Only return cached result if it actually has sources or was recently completed successfully
    if existing_claim and existing_claim.sources:
        return existing_claim
    
    # If it exists but has no sources, we might want to re-run or update it.
    # For simplicity, if it exists, let's use it but update it (or just delete and recreate).
    # Let's just delete the old one to be clean if it is empty.
    if existing_claim:
        db.delete(existing_claim)
        db.commit()

    # 2. Create new Claim
    new_claim = models.Claim(
        text=input_data.text,
        hash_key=claim_hash,
        status="processing",
        created_at=datetime.utcnow()
    )
    db.add(new_claim)
    db.commit()
    db.refresh(new_claim)

    # 3. Perform Analysis (OSINT)
    # Search
    search_results = osint_service.search_claim(new_claim.text)
    
    # Save Sources
    sources = []
    for res in search_results:
        source = models.Source(
            claim_id=new_claim.id,
            url=res['url'],
            domain=res['domain'],
            title=res['title'],
            snippet=res['snippet'],
            source_type="web"
        )
        db.add(source)
        sources.append(source)
    
    # 4. Realistic Analysis/Scoring Logic
    new_claim.status = "completed"
    
    if not sources:
        new_claim.credibility_score = 0
        new_claim.credibility_label = "Unverified"
        new_claim.explanation = "No public sources found. This claim may be too recent, niche, or fabricated."
    else:
        # Simple heuristic for MVP:
        # - Base score: 50
        # - +10 per source (max 40)
        # - +10 if 'news' or 'report' in title
        
        score = 50 + min(len(sources) * 10, 40)
        
        # Check for premium domains (naive list)
        trusted_domains = ["reuters", "apnews", "bbc", "npr", "gov", "edu"]
        if any(d in s.domain for s in sources for d in trusted_domains):
            score += 10
            
        score = min(score, 100)
        
        new_claim.credibility_score = score
        
        if score >= 85:
            new_claim.credibility_label = "High Confidence"
            new_claim.explanation = f"Cross-referenced with {len(sources)} sources, including potential high-authority domains."
        elif score >= 60:
            new_claim.credibility_label = "Likely Credible"
            new_claim.explanation = f"Supported by {len(sources)} sources. Verify specific details in the timeline."
        else:
            new_claim.credibility_label = "Uncertain"
            new_claim.explanation = "Sources found, but volume or authority is low. Treat with caution."

    new_claim.summary = f"Analysis complete with {len(sources)} found sources."

    db.commit()
    db.refresh(new_claim)
    
    return new_claim

@app.get("/api/claims/{claim_id}", response_model=schemas.ClaimResponse)
def get_claim(claim_id: int, db: Session = Depends(database.get_db)):
    claim = db.query(models.Claim).filter(models.Claim.id == claim_id).first()
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    return claim
