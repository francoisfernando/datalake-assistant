from google.genai import types

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search, AgentTool, ToolContext
from google.adk.code_executors import BuiltInCodeExecutor

from agents.common_config import retry_config
from typing import Dict

from logging import Logger
logger = Logger("data_quality_agent")

# Pay attention to the docstring, type hints, and return value.
def get_last_updated_timestamp(dataset_name: str) -> Dict[str, str]:
    """Looks up the last updated timestamp for a given dataset.

    This tool simulates getting the last updated timestamp for a dataset.

    Args:
        dataset_name: The name of the dataset to look up.

    Returns:
        Dictionary with status and last updated timestamp information.
        Success: {"status": "success", "last_updated": "2024-01-15T12:34:56Z"}
        Error: {"status": "error", "error_message": "Dataset not found"}
    """
    # return {
    #     "status": "error",
    #     "error_message": f"Dataset '{dataset_name}' not found",
    # }
    logger.info(f"Fetching last updated timestamp for dataset: {dataset_name}")
    return {
        "status": "success",
        "last_updated": "2024-01-15T12:34:56Z",
    }


def create_data_quality_agent() -> LlmAgent:
    """Creates and returns a data quality agent."""
    return LlmAgent(
        name="DataQualityAgent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""You are a specialized data quality retrieval agent.
        Your task is to take a request for a data quality question and use the data quality tools 
        available to you to formulate a response.

        For any data quality request:

        1. Get last updated timestamp: Use the get_last_updated_timestamp() tool to determine the last update timestamp.
        2. Error Check: After each tool call, you must check the "status" field in the response. If the status is "error",
           you must stop and clearly explain the issue to the user.
        """,
        tools=[
            get_last_updated_timestamp,
        ],
    )
