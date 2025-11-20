from orchestrator_service.agent_registry import AgentRegistry

class Orchestrator:
    """
    Central ADK-style orchestrator: intent detection, IAM checks,
    routing, evidence merging, and response assembly.
    """

    def __init__(self):
        self.registry = AgentRegistry()

    async def handle_intent(self, query: str):
        """Very naive intent router. Replace with LLM-based intent model."""
        q = query.lower()
        if "lineage" in q or "derived" in q:
            return "lineage_agent"
        if "quality" in q or "fresh" in q:
            return "quality_agent"
        if "last updated" in q or "update" in q:
            return "retriever_agent"
        if "assumption" in q or "provenance" in q:
            return "reasoning_agent"
        return "reasoning_agent"  # default fallback

    async def route(self, query: str):
        """Determine intent then route to appropriate agent."""
        agent_name = await self.handle_intent(query)
        agent = self.registry.get(agent_name)
        if agent_name == "reasoning_agent":
            # pass evidence list you obtained from RetrieverAgent
            evidence = [...]   # whatever retriever returned
            return await agent.handle(query, evidence=evidence)
        else:
            return await agent.handle(query)


    async def assemble_response(self, answer):
        """Add provenance, metadata, etc."""
        return {"answer": answer, "confidence": 0.92}

