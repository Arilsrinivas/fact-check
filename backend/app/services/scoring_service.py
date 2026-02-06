from typing import List
from app.models import Source

class ScoringService:
    def __init__(self):
        # Trusted domains boost score
        self.trusted_domains = [
            "wikipedia.org", "reuters.com", "apnews.com", "bbc.com", 
            "nytimes.com", "washingtonpost.com", "snopes.com", "factcheck.org",
            "politifact.com", "who.int", "nasa.gov", "nature.com"
        ]
        
        # Debunking keywords lower score
        self.debunk_keywords = [
            "fake", "hoax", "false", "debunk", "myth", "conspiracy", 
            "incorrect", "unfounded", "baseless", "lie", "rumor", "scam"
        ]
        
        # Support keywords boost score
        self.support_keywords = [
            "confirmed", "verified", "true", "accurate", "proven", 
            "evidence", "fact", "official", "released by"
        ]

    def calculate_score(self, claim_text: str, sources: List[Source]) -> float:
        if not sources:
            return 0.0

        score = 50.0 # Start neutral
        
        # 1. Domain Authority Check
        trusted_count = 0
        for s in sources:
            domain = s.domain.lower()
            if any(t in domain for t in self.trusted_domains):
                trusted_count += 1
                score += 10
        
        # Cap domain boost
        if trusted_count > 3: score += 5
        
        # 2. Content Analysis (Snippet Sentiment)
        debunk_hits = 0
        support_hits = 0
        
        for s in sources:
            snippet = (s.snippet or "").lower()
            title = (s.title or "").lower()
            content = snippet + " " + title
            
            # Check for debunking terms (strong penalty)
            if any(kw in content for kw in self.debunk_keywords):
                debunk_hits += 1
                score -= 15 
            
            # Check for supporting terms
            if any(kw in content for kw in self.support_keywords):
                support_hits += 1
                score += 5

        # 3. Contextual Adjustment
        # If we have many debunk hits, the score should crash
        if debunk_hits >= 2:
            score = min(score, 40.0) # Cap at low confidence
        
        if debunk_hits > trusted_count:
             score = max(0, score - 20)

        # Normalize
        return max(0.0, min(100.0, score))

    def get_label(self, score: float) -> str:
        if score >= 80: return "High Confidence"
        if score >= 60: return "Probable"
        if score >= 40: return "Debated / Uncertain"
        if score >= 20: return "Low Credibility"
        return "Likely False"

scoring_service = ScoringService()
