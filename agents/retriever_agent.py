import logging
from tools.metadata_tool import create_metadata_tool
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from agents.common_config import retry_config
from typing import Optional

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def create_metadata_retriever_agent() -> Optional[LlmAgent]:
    """Creates and returns a metdata retriver agent."""

    tools = [
        create_metadata_tool(),
    ]

    available_tools = [tool for tool in tools if tool is not None]
    if available_tools == []:
        logger.warning("No metadata tools available for MetadataRetrieverAgent.")
        return None

    return LlmAgent(
        name="MetadataRetrieverAgent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""You are a specialized metadata retrieval agent.
Your task is to take a request for a metadata question and use the metadata tools 
available to you to formulate a response.

For any metadata request you need to consider what tables exist in the data lake and their schema including column names and types.

The data is ingested to the data lake from various sources including Kafka topics, Mongo databases, and file uploads.
Once ingested, the data may go through several transformation processes such as cleaning, normalization, aggregation, 
and enrichment before being stored in its final form. All of the data is stored in Athena tables in Parquet format.

When you receive a user query, analyze it carefully to determine what metadata information is being requested.
Then, select the appropriate metadata tool(s) to call in order to gather the necessary information.
Note that some questions may require multiple tool calls to gather all relevant metadata.

CRITICAL INSTRUCTION: When using tools from the Amazon Data Processing MCP Server, 
you MUST use hyphens instead of underscores in the tool names.
For example, use 'get-table-metadata' and NOT 'get_table_metadata'.
Use 'list-databases' and NOT 'list_databases'.
    


Error Check: After each tool call, you must check for errors in the response. If you encounter an exception when formatting the response
just use python str() function on the response to report the error.  If any tool returns an error status, you must stop and 
clearly explain the issue to the user.

Also report any exceptions or issues encountered during tool calls and the actual tool responses in your final answer.

        """,
        tools=available_tools,
    )
