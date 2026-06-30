from schema.candidate_profile import CandidateProfile

class ConfidenceEngine:
    def __init__(self):
        # Base confidence scores based on source
        self.SOURCE_CONFIDENCE_MAP = {
            "csv": 0.95,
            "resume_llm": 0.85,
            "merged (csv + resume_llm)": 0.90,
        }
        
    def calculate(self, profile: CandidateProfile):
        scores = {}
        
        for prov in profile.provenance:
            field = prov.field
            source = prov.source
            score = self.SOURCE_CONFIDENCE_MAP.get(source, 0.5)
            
            # Additional heuristic: increase confidence for structured LLM arrays
            if source == "resume_llm" and field in ["education", "experience"]:
                score = 0.90  # As per implementation.md example
                
            scores[field] = score
            
        profile.confidence_scores = scores
        
        if scores:
            profile.overall_confidence = sum(scores.values()) / len(scores)
        else:
            profile.overall_confidence = 0.0
