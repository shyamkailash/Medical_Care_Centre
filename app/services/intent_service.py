class IntentService:

    def detect_intent(self, query: str) -> str:
        query = query.lower()

        if any(x in query for x in ["pain", "fever", "symptom"]):
            return "symptom"
        elif any(x in query for x in ["what is", "define", "explain"]):
            return "info"
        else:
            return "general"