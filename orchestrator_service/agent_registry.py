from agents.orchestrator_agent import OrchestratorAgent
from agents.retriever_agent import RetrieverAgent
from agents.reasoning_agent import ReasoningAgent
from agents.quality_agent import QualityAgent
from agents.lineage_agent import LineageAgent
from agents.feedback_agent import FeedbackAgent

class AgentRegistry:
    def __init__(self):
        self.agents = {
            "orchestrator_agent": OrchestratorAgent(),
            "retriever_agent": RetrieverAgent(),
            "reasoning_agent": ReasoningAgent(),
            "quality_agent": QualityAgent(),
            "lineage_agent": LineageAgent(),
            "feedback_agent": FeedbackAgent(),
        }

    def get(self, name: str):
        return self.agents[name]

