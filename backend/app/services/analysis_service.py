import whois
import waybackpy
from datetime import datetime
from urllib.parse import urlparse

class AnalysisService:
    async def analyze_source(self, url: str):
        domain = urlparse(url).netloc
        metadata = {
            "domain_age_days": None,
            "has_archive": False,
            "wayback_url": None
        }
        
        # 1. Whois (Blocking, should be async ideally or threaded)
        try:
            w = whois.whois(domain)
            if w.creation_date:
                creation_date = w.creation_date
                if isinstance(creation_date, list):
                    creation_date = creation_date[0]
                
                age = (datetime.now() - creation_date).days
                metadata["domain_age_days"] = age
        except:
            pass # Whois often fails or is blocked

        # 2. Wayback Machine
        try:
            user_agent = "SourceTrace-Bot/1.0"
            wayback = waybackpy.Url(url, user_agent)
            archive = wayback.oldest()
            if archive:
                metadata["has_archive"] = True
                metadata["wayback_url"] = archive.archive_url
        except:
            pass 

        return metadata

analysis_service = AnalysisService()
