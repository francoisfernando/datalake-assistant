from datetime import datetime
import os

# from google.adk.tools.langchain_tool import LangchainTool
from google.adk.tools.mcp_tool import MCPToolset, StreamableHTTPConnectionParams

from dotenv import load_dotenv
from typing import Optional

# Load environment variables
load_dotenv()

from logging import getLogger

logger = getLogger(__name__)


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
        logger.info("Created MCPToolset for metadata tool")
    except Exception:
        mcp_tools = None
        logger.exception("Failed to create MCPToolset for metadata tool")

    return mcp_tools
