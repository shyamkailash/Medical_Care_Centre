from app.agents.base_agent import BaseAgent

class MedicalInfoAgent(BaseAgent):

    def handle(self, query: str):
        return "User is asking for general medical information."