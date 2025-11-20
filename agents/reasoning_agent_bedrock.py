import os
import json
import asyncio
import logging
from typing import List, Optional, Dict, Any

import boto3
from botocore.config import Config
from botocore.exceptions import BotoCoreError, ClientError

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def _default_prompt_template(query: str, evidence: List[Dict[str, Any]]) -> str:
    """
    Build a prompt that:
      - instructs the model to rely strictly on the provided evidence
      - requests a short answer, a concise explanation, a confidence estimate,
        and a bullet list of sources (IDs/paths) used.
      - If evidence is empty, model should respond with "Insufficient evidence".
    """
    evidence_text = ""
    if evidence:
        # evidence items are expected to be dicts with at least 'source' and 'snippet'
        for i, ev in enumerate(evidence, start=1):
            source = ev.get("source", f"evidence_{i}")
            snippet = ev.get("snippet", ev.get("text", ""))
            evidence_text += f"[{i}] source: {source}\n{snippet}\n\n"
    else:
        evidence_text = "(no evidence provided)\n"

    prompt = f"""
You are a AWS Athena data-lake discovery assistant that must answer queries ONLY using the provided evidence.
If the evidence does not support a factual answer, respond with exactly: "Insufficient evidence".

User question:
{query}

--EVIDENCE--
{evidence_text}
--END EVIDENCE--

Tasks (in order):
1) Provide a one-line short_answer that directly answers the user's question (or "Insufficient evidence").
2) Provide a concise explanation (1-3 sentences) showing which pieces of evidence you used and why.
3) Provide a confidence score between 0.0 and 1.0 that reflects how supported the answer is by the evidence.
4) List the evidence indexes you used (e.g., [1], [2]) and the source identifiers.

Output must be valid JSON with keys: short_answer, explanation, confidence, sources.
Do NOT invent sources or hallucinate facts that are not present in the evidence.
"""

    return prompt.strip()


class ReasoningAgent:
    """
    ReasoningAgent that calls AWS Bedrock (claude sonnet model) via boto3.

    Environment variables:
      - BEDROCK_MODEL_ID: model id to call (e.g. "anthropic.claude-sonnet" or the correct Bedrock model identifier)
      - AWS_REGION: AWS region for the Bedrock endpoint (default: ap-southeast-2)
      - BEDROCK_CLIENT_TIMEOUT: optional timeout seconds for the client (default: 60)

    The agent accepts:
      - query: the user question (string)
      - evidence: optional list of evidence dicts, each with 'source' and 'snippet' or 'text'.
    """

    def __init__(self):
        self.model_id = os.environ.get("BEDROCK_MODEL_ID", "anthropic.claude-sonnet")
        self.region = os.environ.get("AWS_REGION", "ap-southeast-2")
        timeout = int(os.environ.get("BEDROCK_CLIENT_TIMEOUT", "60"))
        # configure retries/timeout sensibly
        botocore_cfg = Config(
            region_name=self.region,
            retries={"max_attempts": 3, "mode": "standard"},
            read_timeout=timeout,
            connect_timeout=10,
        )
        # Bedrock runtime client (invoke_model)
        self.client = boto3.client("bedrock-runtime", config=botocore_cfg)

    async def _invoke_bedrock(self, prompt: str) -> str:
        """
        Invoke Bedrock model synchronously via boto3, wrapped to be async-safe.
        Uses 'contentType': 'text/plain' and sends the prompt as the raw body.
        """
        def _call():
            try:
                response = self.client.invoke_model(
                    modelId=self.model_id,
                    contentType="text/plain",
                    accept="application/json",
                    body=prompt.encode("utf-8"),
                )
                # response['body'] is a StreamingBody
                body_stream = response.get("body")
                if body_stream is None:
                    raise RuntimeError("Empty response body from Bedrock invoke_model")
                # read bytes and decode
                raw = body_stream.read()
                if isinstance(raw, bytes):
                    text = raw.decode("utf-8")
                else:
                    text = str(raw)
                return text
            except (BotoCoreError, ClientError) as e:
                logger.exception("Bedrock invocation failed")
                raise RuntimeError(f"Bedrock invocation error: {e}")

        # run blocking boto3 call in threadpool
        return await asyncio.to_thread(_call)

    async def handle(self, query: str, evidence: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Main handler called by orchestrator. Returns structured dict.
        """
        if evidence is None:
            evidence = []

        prompt = _default_prompt_template(query, evidence)

        try:
            raw_out = await self._invoke_bedrock(prompt)
        except Exception as e:
            logger.error("Bedrock call failed: %s", e)
            return {"agent": "reasoning", "error": str(e)}

        # The model is instructed to output JSON. We try to parse it.
        parsed = None
        try:
            # Some Bedrock models may prepend or append extra text; attempt to locate JSON blob.
            text = raw_out.strip()
            # Attempt direct parse
            parsed = json.loads(text)
        except Exception:
            # attempt to find first '{' and last '}' and parse the substring
            try:
                start = raw_out.find("{")
                end = raw_out.rfind("}") + 1
                if start != -1 and end != -1 and end > start:
                    snippet = raw_out[start:end]
                    parsed = json.loads(snippet)
                else:
                    raise ValueError("JSON not found in model output")
            except Exception as pe:
                logger.exception("Failed to parse Bedrock model output as JSON")
                return {
                    "agent": "reasoning",
                    "error": "Failed to parse model output",
                    "raw_output": raw_out
                }

        # Normalize and return
        # Ensure keys exist
        short_answer = parsed.get("short_answer") or parsed.get("shortAnswer") or ""
        explanation = parsed.get("explanation", "")
        confidence = parsed.get("confidence", None)
        sources = parsed.get("sources", [])

        # Attempt a numeric cast for confidence
        try:
            confidence = float(confidence) if confidence is not None else None
        except Exception:
            confidence = None

        return {
            "agent": "reasoning",
            "result": {
                "short_answer": short_answer,
                "explanation": explanation,
                "confidence": confidence,
                "sources": sources,
                "raw_model_output": raw_out,
            },
        }


# quick local test helper (not invoked automatically)
if __name__ == "__main__":
    import asyncio
    ra = ReasoningAgent()
    sample_evidence = [
        {"source": "glue:db.table1", "snippet": "LastUpdatedTime: 2025-11-12T03:24:00Z"},
        {"source": "quality_report:table1", "snippet": "Null rate for user_id = 0.02"}
    ]

    async def run():
        out = await ra.handle("When was dataset table1 last updated?", evidence=sample_evidence)
        print(json.dumps(out, indent=2))

    asyncio.run(run())
