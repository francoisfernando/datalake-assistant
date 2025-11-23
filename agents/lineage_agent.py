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
def get_producing_service(dataset_name: str) -> Dict[str, str]:
    """Looks up the services which produces data included in a given dataset.

    This tool simulates getting the source of data for a dataset.

    Args:
        dataset_name: The name of the dataset to look up.

    Returns:
        Dictionary with status and service and kafka topic information.
        Success: {"status": "success", "service": "service_name", "kafka_topic": "topic_name"}
        Error: {"status": "error", "error_message": "Dataset not found"}
    """
    # return {
    #     "status": "error",
    #     "error_message": f"Dataset '{dataset_name}' not found",
    # }
    logger.info(f"Fetching lineage for dataset: {dataset_name}")
    return {
        "status": "success",
        "service": "IOT API Integration",
        "kafka_topic": "iot_telemetry",
    }


def create_data_lineage_agent() -> LlmAgent:
    """Creates and returns a data lineage agent."""
    return LlmAgent(
        name="DataLineageAgent",
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        instruction="""You are a specialized data lineage retrieval agent.
Your task is to take a request for a data lineage question and use the data lineage tools 
available to you to formulate a response.

For any data lineage request you need to consider how the data arrives into the data lake and the transformations it undergoes.

The data is ingested to the data lake from various sources including Kafka topics, Mongo databases, and file uploads.
Once ingested, the data may go through several transformation processes such as cleaning, normalization, aggregation, 
and enrichment before being stored in its final form. All of the data is stored in Athena tables in Parquet format.

1. Get service or services which produces data to a Kafka topic: Use get_producing_service() tool to determine which services produce the data via which Kafka topic.
2. Error Check: After each tool call, you must check the "status" field in the response. If the status is "error",
    you must stop and clearly explain the issue to the user.
        """,
        tools=[
            get_producing_service,
        ],
    )
