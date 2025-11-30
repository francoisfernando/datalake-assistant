import asyncio
from dotenv import load_dotenv
from google.adk.runners import InMemoryRunner
from agents.orchestrator_agent import app
from logging import basicConfig, DEBUG, INFO, Logger
from random import choice

basicConfig(level=INFO)


logger = Logger("main")

load_dotenv()  # load API keys and settings
# Set a Runner using the imported application object
runner = InMemoryRunner(app=app)


test_queries = [
    "How did the sakila.actor table get created?",
    # "What are the columns in sakila.actor table and when was it last updated?",
    # "When was sakila.actor dataset last updated?",
    # "When was telemetry_data dataset last updated?",
    # "Which service produces telemetry_data?",
    # "Which service produces sales_data?",
]


async def main():
    try:
        # run_debug() requires ADK Python 1.18 or higher:
        response = await runner.run_debug(choice(test_queries))

    except Exception as e:
        logger.error("An error occurred during agent execution", exc_info=True)


if __name__ == "__main__":
    asyncio.run(main())
