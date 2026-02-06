from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core import database
from app import models, schemas
from app.services.claim_service import claim_service
from app.services.vector_store import vector_store
from app.services.explanation_service import explanation_service
from app.services.osint import osint_service
from app.services.scoring_service import scoring_service 
from datetime import datetime

router = APIRouter()

@router.post("/analyze", response_model=schemas.ClaimResponse)
def analyze_claim(input_data: schemas.ClaimInput, db: Session = Depends(database.get_db)):
    try:
        # 1. Normalize
        text = claim_service.normalize_claim(input_data.text)
        claim_hash = str(hash(text))

        # 2. Check Cache
        existing = db.query(models.Claim).filter(models.Claim.hash_key == claim_hash).first()
        if existing and existing.status == "completed":
            return existing

        # 3. Create Claim
        new_claim = models.Claim(
            text=text,
            hash_key=claim_hash,
            status="processing",
            entities=claim_service.extract_entities(text),
            created_at=datetime.utcnow()
        )
        db.add(new_claim)
        db.commit()
        db.refresh(new_claim)
        
        # Add to vector store
        new_claim.vector_id = vector_store.add_claim(new_claim.id, text)
        db.commit()

        # 4. OSINT Search
        search_results = osint_service.search_claim(text)
        sources = []
        
        for res in search_results:
            source = models.Source(
                claim_id=new_claim.id,
                url=res['url'],
                domain=res['domain'],
                title=res['title'],
                snippet=res['snippet'],
                source_type="web",
            )
            db.add(source)
            sources.append(source)
        
        # 6. Scoring & Explanation
        new_claim.credibility_score = scoring_service.calculate_score(text, sources)
        new_claim.credibility_label = scoring_service.get_label(new_claim.credibility_score)
        
        if sources:
            new_claim.explanation = f"AI Analysis: Verified against {len(sources)} sources."
        else:
            new_claim.explanation = "No data found."

        new_claim.status = "completed"
        db.commit()
        db.refresh(new_claim)
        
        return new_claim
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"CRASH: {str(e)}")

@router.get("/{claim_id}", response_model=schemas.ClaimResponse)
def get_claim(claim_id: int, db: Session = Depends(database.get_db)):
    claim = db.query(models.Claim).filter(models.Claim.id == claim_id).first()
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    return claim
