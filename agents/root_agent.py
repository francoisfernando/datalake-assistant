from google.adk.agents.llm_agent import LlmAgent
from google.adk.apps import App
from agents.quality_agent import create_data_quality_agent
from agents.lineage_agent import create_data_lineage_agent
from agents.retriever_agent import create_metadata_retriever_agent
from google.adk.tools import AgentTool


tools = [
    # using other agents as tools
    AgentTool(agent=create_data_quality_agent()),
    AgentTool(agent=create_data_lineage_agent()),
    AgentTool(agent=create_metadata_retriever_agent()),
]

available_tools = [tool for tool in tools if tool.agent is not None]

root_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="datalake_assitant_agent",
    # retry_options=retry_config,
    description="An agent that helps discovering a data lake.",
    instruction="""You are an intelligent agent for discovering various aspects of a data lake based on user queries.
Your job is to analyze user queries and gather relevant information by calling the appropriate specialized agent.

Available agents:
- data_quality_agent: Data quality, freshness, completeness, update timestamps
- lineage_agent: Data lineage, dependencies, derivations
- retriever_agent: Metadata, schemas, update timestamps
- reasoning_agent: Complex synthesis, explanations, multi-source questions

Analyze the query and call the appropriate tool or tools. If you need to synthesize information from multiple agents,
use the reasoning_agent.

All tools are designed to return a python dictionary with a "status" field indicating "success" or "error". Other available
fields depend on the specific tool called. Analyze the responses carefully to formulate your final answer.

If any tool returns status "error", explain the issue to the user clearly.

If you can't fulfill the user's request using the specialized agents, respond with:
"I'm sorry, but I am unable to assist with that request." and explain why.

""",
    tools=available_tools,
)

app = App(
    name="agents",
    root_agent=root_agent,
    # Optionally include App-level features:
    # plugins, context_cache_config, resumability_config
)
