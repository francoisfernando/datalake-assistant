class FeedbackAgent:
    async def handle(self, query: str):
        return f"[FeedbackAgent] Feedback recorded for: {query}"

