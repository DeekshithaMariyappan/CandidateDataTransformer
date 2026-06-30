from typing import List
from schema.candidate_profile import ConflictRecord

class ConflictResolver:
    def __init__(self):
        self.conflicts: List[ConflictRecord] = []

    def resolve(self, field: str, csv_value: any, resume_value: any, prefer_source: str) -> any:
        """
        Resolves a conflict between CSV and Resume data and records the decision.
        """
        if csv_value and not resume_value:
            return csv_value
        if resume_value and not csv_value:
            return resume_value
        if csv_value == resume_value:
            return csv_value

        # A conflict exists
        selected = csv_value if prefer_source == "csv" else resume_value
        reason = f"prefer_{prefer_source}"

        conflict = ConflictRecord(
            field=field,
            csv_value=csv_value,
            resume_value=resume_value,
            selected=selected,
            reason=reason
        )
        self.conflicts.append(conflict)
        return selected

    def get_conflicts(self) -> List[dict]:
        return [c.dict() for c in self.conflicts]
