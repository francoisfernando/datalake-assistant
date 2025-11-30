from datetime import datetime
import os

# from google.adk.tools.langchain_tool import LangchainTool
from google.adk.tools.mcp_tool import MCPToolset, StreamableHTTPConnectionParams

from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv()


def create_metadata_tool() -> Optional[MCPToolset]:
    """
    Create a MCPToolset that provides metadata about AWS Glue datasets.
    """
    try:
        mcp_tools = MCPToolset(
            connection_params=StreamableHTTPConnectionParams(
                url="http://localhost:3000/mcp/",
                # headers={
                #     "Authorization": "Bearer " + os.getenv("xxx_PERSONAL_ACCESS_TOKEN"),
                # },
            ),

            # Limit to specific tools
            tool_filter=[
                "manage_aws_athena_databases_and_tables",
                "manage_aws_glue_crawlers",
                "manage_aws_glue_classifiers",
                "manage_aws_glue_crawler_management",
            ],
        )
    except Exception:
        # GitHub MCP server not available or token missing
        mcp_tools = None

    return mcp_tools

# class MetadataTool:
#     def fetch_metadata(self, dataset):
#         return {"dataset": dataset, "columns": ["id", "value"], "last_modified": "2025-05-01"}

