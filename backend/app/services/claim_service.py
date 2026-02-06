import spacy
from sqlalchemy.orm import Session
from app.models import Claim
import datetime

# Load NLP model
try:
    nlp = spacy.load("en_core_web_sm")
except:
    # Fallback if not downloaded (though it should be)
    nlp = None

class ClaimService:
    def extract_entities(self, text: str):
        if not nlp:
            return []
        doc = nlp(text)
        entities = []
        for ent in doc.ents:
            entities.append({"text": ent.text, "label": ent.label_})
        return entities

    def normalize_claim(self, text: str):
        # Basic normalization for now
        return text.strip().lower()

claim_service = ClaimService()
