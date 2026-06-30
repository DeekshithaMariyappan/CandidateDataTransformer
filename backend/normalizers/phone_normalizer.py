import phonenumbers
from typing import Optional

class PhoneNormalizer:
    @staticmethod
    def normalize(phone: str, default_region: str = "IN") -> Optional[str]:
        if not phone:
            return None
        try:
            # Parse the phone number
            parsed_number = phonenumbers.parse(str(phone), default_region)
            
            # Format to E.164 standard (e.g. +919876543210)
            if phonenumbers.is_valid_number(parsed_number):
                return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)
        except Exception:
            pass
        return str(phone).strip()
