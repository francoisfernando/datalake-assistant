async def route_to_agent(orchestrator, query: str):
    answer = await orchestrator.route(query)
    final = await orchestrator.assemble_response(answer)
    return final

