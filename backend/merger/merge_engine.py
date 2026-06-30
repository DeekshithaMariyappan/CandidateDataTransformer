from typing import Dict, Any, List
from merger.conflict_resolution import ConflictResolver
from schema.candidate_profile import CandidateProfile
from normalizers.phone_normalizer import PhoneNormalizer
from normalizers.skill_normalizer import SkillNormalizer

class MergeEngine:
    def __init__(self):
        self.conflict_resolver = ConflictResolver()

    def merge(self, csv_data: Dict[str, Any], resume_data: Dict[str, Any]) -> CandidateProfile:
        profile = CandidateProfile()
        
        # Candidate ID
        csv_id = str(csv_data.get("candidate_id", "")) if csv_data.get("candidate_id") else None
        profile.candidate_id = self.conflict_resolver.resolve("candidate_id", csv_id, None, prefer_source="csv")
        
        # Merge Emails (Prefer CSV)
        csv_email = csv_data.get("email") or csv_data.get("emails", "")
        resume_emails = resume_data.get("emails", [])
        resume_email = resume_emails[0] if resume_emails else None
        
        selected_email = self.conflict_resolver.resolve("email", csv_email, resume_email, prefer_source="resume")
        if selected_email:
            profile.emails = [selected_email]
            
        # Merge Phones (Prefer normalized value, assume both can be normalized, prefer CSV if both valid)
        csv_phone = PhoneNormalizer.normalize(csv_data.get("phone", ""))
        resume_phones = resume_data.get("phones", [])
        resume_phone = PhoneNormalizer.normalize(resume_phones[0]) if resume_phones else None
        
        selected_phone = self.conflict_resolver.resolve("phone", csv_phone, resume_phone, prefer_source="resume")
        if selected_phone:
            profile.phones = [selected_phone]

        # Name
        csv_name = csv_data.get("name")
        resume_name = resume_data.get("full_name")
        profile.full_name = self.conflict_resolver.resolve("full_name", csv_name, resume_name, prefer_source="resume")

        # Skills (Union of all skills, normalized)
        csv_skills_raw = csv_data.get("skills", "")
        csv_skills = [s.strip() for s in str(csv_skills_raw).split(",")] if csv_skills_raw else []
        resume_skills_raw = resume_data.get("skills", [])
        
        all_skills = set()
        for s in csv_skills + resume_skills_raw:
            normalized_s = SkillNormalizer.normalize(s)
            if normalized_s:
                all_skills.add(normalized_s)
        profile.skills = list(all_skills)

        # Education (Prefer Resume)
        profile.education = resume_data.get("education", [])

        # Experience (Prefer Resume)
        profile.experience = resume_data.get("experience", [])

        # Projects
        profile.projects = resume_data.get("projects", [])
        
        # Headline
        profile.headline = resume_data.get("headline", "")

        profile.conflicts = self.conflict_resolver.conflicts
        
        return profile
