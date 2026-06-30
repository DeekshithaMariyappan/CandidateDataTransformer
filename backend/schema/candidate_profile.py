from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class FieldProvenance(BaseModel):
    field: str
    source: str
    original_value: Optional[Any] = None

class ConflictRecord(BaseModel):
    field: str
    csv_value: Optional[Any] = None
    resume_value: Optional[Any] = None
    selected: Optional[Any] = None
    reason: str

class CandidateProfile(BaseModel):
    candidate_id: Optional[str] = None
    full_name: Optional[str] = None
    emails: List[str] = []
    phones: List[str] = []
    headline: Optional[str] = None
    skills: List[str] = []
    education: List[str] = []
    experience: List[Dict[str, Any]] = []
    projects: List[Dict[str, Any]] = []
    
    provenance: List[FieldProvenance] = []
    conflicts: List[ConflictRecord] = []
    confidence_scores: Dict[str, float] = {}
    overall_confidence: float = 0.0

class TransformationResponse(BaseModel):
    profile: Dict[str, Any]
    confidence: Dict[str, float]
    provenance: List[Dict[str, Any]]
    conflicts: List[Dict[str, Any]]
