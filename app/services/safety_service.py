from app.core.constants import EMERGENCY_KEYWORDS

class SafetyService:

    def check_emergency(self, query: str):
        for keyword in EMERGENCY_KEYWORDS:
            if keyword in query.lower():
                return True
        return False