from typing import List, Dict, Any
from schema.candidate_profile import FieldProvenance, CandidateProfile

class ProvenanceTracker:
    def __init__(self):
        self.provenance: List[FieldProvenance] = []

    def track(self, field: str, source: str, original_value: Any = None):
        self.provenance.append(FieldProvenance(
            field=field,
            source=source,
            original_value=original_value
        ))

    def build_provenance(self, profile: CandidateProfile, csv_data: Dict[str, Any], resume_data: Dict[str, Any]):
        # Simple tracking logic based on presence and conflict resolution
        
        # Email
        if profile.emails:
            source = "csv" if csv_data.get("email") else "resume_llm"
            self.track("emails", source, profile.emails[0])
            
        # Phone
        if profile.phones:
            source = "csv" if csv_data.get("phone") else "resume_llm"
            self.track("phones", source, profile.phones[0])
            
        # Name
        if profile.full_name:
            source = "resume_llm" if resume_data.get("full_name") else "csv"
            self.track("full_name", source, profile.full_name)
            
        # Skills
        if profile.skills:
            # We merged them, so we'll mark as merged
            self.track("skills", "merged (csv + resume_llm)")
            
        # Education
        if profile.education:
            self.track("education", "resume_llm")
            
        # Experience
        if profile.experience:
            self.track("experience", "resume_llm")
            
        profile.provenance = self.provenance
