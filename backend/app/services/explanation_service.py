import ollama
from app.models import Claim

class ExplanationService:
    def generate_explanation(self, claim: Claim):
        # Construct prompt
        sources_text = "\n".join([f"- {s.title} ({s.domain})" for s in claim.sources])
        prompt = f"""
        Analyze the following claim based on the provided evidence sources.
        Claim: "{claim.text}"
        
        Evidence:
        {sources_text}
        
        Task:
        1. Determine if the claim is supported, disputed, or debunked.
        2. Write a neutral, 2-sentence summary explaining why.
        3. Do not invent information.
        
        Output:
        """
        
        try:
            # Assumes Ollama is running on localhost:11434
            response = ollama.chat(model='llama3', messages=[
                {'role': 'user', 'content': prompt},
            ])
            return response['message']['content']
        except Exception as e:
            print(f"Ollama Error: {e}")
            return "AI Explanation unavailable (Ollama service not reachable)."

explanation_service = ExplanationService()
