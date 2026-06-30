import re
from datetime import datetime

class DateNormalizer:
    @staticmethod
    def normalize(date_str: str) -> str:
        if not date_str:
            return ""
        
        # Simple parsing for "Month YYYY" like "June 2025"
        try:
            # Clean up the string a bit
            clean_str = re.sub(r'[^a-zA-Z0-9\s]', ' ', date_str).strip()
            
            # Try to parse "Month YYYY"
            parsed_date = datetime.strptime(clean_str, "%B %Y")
            return parsed_date.strftime("%Y-%m")
        except ValueError:
            pass
            
        try:
             # Try to parse "Mon YYYY" (abbreviated)
             parsed_date = datetime.strptime(clean_str, "%b %Y")
             return parsed_date.strftime("%Y-%m")
        except ValueError:
             pass
             
        # Return original if parsing fails
        return str(date_str).strip()
