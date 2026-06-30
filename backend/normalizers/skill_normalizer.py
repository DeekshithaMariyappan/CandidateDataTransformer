import re

class SkillNormalizer:
    # A simple mapping to normalize common variations
    SKILL_MAP = {
        "reactjs": "React",
        "react.js": "React",
        "react": "React",
        "nodejs": "Node.js",
        "node.js": "Node.js",
        "node": "Node.js",
        "js": "JavaScript",
        "javascript": "JavaScript",
        "ts": "TypeScript",
        "typescript": "TypeScript",
        "python3": "Python",
        "python": "Python",
        "java8": "Java",
        "java": "Java",
        "c++": "C++",
        "cpp": "C++",
        "html5": "HTML",
        "css3": "CSS",
    }

    @classmethod
    def normalize(cls, skill: str) -> str:
        if not skill:
            return ""
        
        # Lowercase and strip for lookup
        clean_skill = skill.lower().strip()
        
        # Return mapped version or title-cased original if no mapping exists
        return cls.SKILL_MAP.get(clean_skill, skill.strip().title())
