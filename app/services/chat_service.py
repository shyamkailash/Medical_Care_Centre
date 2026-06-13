from app.services.intent_service import IntentService
from app.services.safety_service import SafetyService
from app.agents.symptom_agent import SymptomAgent
from app.agents.medical_info_agent import MedicalInfoAgent
from app.llm.ollama_client import generate_response
from app.llm.prompt_templates import medical_prompt

class ChatService:

    def __init__(self):
        self.intent_service = IntentService()
        self.safety_service = SafetyService()
        self.symptom_agent = SymptomAgent()
        self.info_agent = MedicalInfoAgent()

    def handle_query(self, query: str) -> str:

        # 🚨 Emergency Check
        if self.safety_service.check_emergency(query):
            return "⚠️ This may be an emergency. Please contact a doctor immediately."

        # 🔍 Intent Detection
        intent = self.intent_service.detect_intent(query)

        # 🤖 Routing
        if intent == "symptom":
            context = self.symptom_agent.handle(query)
        elif intent == "info":
            context = self.info_agent.handle(query)
        else:
            context = ""

        # 🧠 LLM Response
        prompt = medical_prompt(query, context)
        response = generate_response(prompt)

        return response + "\n\n⚠️ This is not a medical diagnosis. Consult a doctor."