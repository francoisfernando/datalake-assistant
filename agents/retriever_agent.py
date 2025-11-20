# agents/retriever_agent.py
import logging
from typing import Dict, Any, List

from common.glue_tools import GlueTools
from common.athena_tools import AthenaTools
from common.s3_tools import S3Tools
from common.lineage_tools import LineageTools
from common.quality_tools import QualityTools

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class RetrieverAgent:
    """
    RetrieverAgent:
    - Determines which tools should be called
    - Executes them
    - Returns normalized evidence objects that ReasoningAgent can use
    """

    def __init__(self):
        self.glue = GlueTools()
        self.athena = AthenaTools()
        self.s3 = S3Tools()
        self.lineage = LineageTools()
        self.quality = QualityTools()

    def _to_evidence_list(self, source_prefix: str, data: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Convert arbitrary dict into:
        [
           { "source": "<prefix>.key", "snippet": "value-string" }
        ]
        """
        evidence = []
        for key, value in data.items():
            snippet = str(value)
            evidence.append({
                "source": f"{source_prefix}.{key}",
                "snippet": snippet
            })
        return evidence

    def _route_tools(self, query: str) -> List[str]:
        """
        Very basic heuristic routing.  
        Could be replaced by classification or an LLM router later.
        """
        q = query.lower()

        tools = []

        if "last updated" in q or "when was" in q:
            tools.append("glue")

        if "quality" in q or "null rate" in q or "data quality" in q:
            tools.append("quality")

        if "lineage" in q or "derived" in q or "how is" in q:
            tools.append("lineage")

        if "partition" in q or "storage" in q or "file" in q:
            tools.append("s3")

        # always fall back to metadata
        if not tools:
            tools.append("glue")

        return tools

    async def handle(self, query: str) -> Dict[str, Any]:
        tools = self._route_tools(query)
        logger.info(f"Retriever routing query '{query}' to tools: {tools}")

        all_evidence: List[Dict[str, str]] = []

        for tool in tools:
            try:
                if tool == "glue":
                    meta = self.glue.get_table_metadata("default", "table1")
                    all_evidence.extend(self._to_evidence_list("glue.table1", meta))

                elif tool == "quality":
                    q = self.quality.get_quality_report("table1")
                    all_evidence.extend(self._to_evidence_list("quality.table1", q))

                elif tool == "lineage":
                    lin = self.lineage.get_column_lineage("table1", "columnA")
                    all_evidence.extend(self._to_evidence_list("lineage.columnA", lin))

                elif tool == "s3":
                    storage = self.s3.get_storage_info("my-bucket", "data/table1/")
                    all_evidence.extend(self._to_evidence_list("s3.table1", storage))

            except Exception as e:
                logger.error(f"Error calling tool {tool}: {e}")

        return {
            "agent": "retriever",
            "evidence": all_evidence
        }
