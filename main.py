from fastapi import FastAPI, HTTPException
from orchestrator_service.orchestrator import Orchestrator
from orchestrator_service.router import route_to_agent

app = FastAPI(title="ADK Multi-Agent Orchestrator")

orchestrator = Orchestrator()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/query")
async def query(payload: dict):
    if "query" not in payload:
        raise HTTPException(400, "Missing 'query' field")

    user_query = payload["query"]
    response = await route_to_agent(orchestrator, user_query)
    return {"response": response}

