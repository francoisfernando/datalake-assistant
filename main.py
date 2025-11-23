import asyncio
from dotenv import load_dotenv
from google.adk.runners import InMemoryRunner
from agents.root_agent import app
from logging import basicConfig, DEBUG, INFO, Logger

basicConfig(level=INFO)


logger = Logger("main")

load_dotenv()  # load API keys and settings
# Set a Runner using the imported application object
runner = InMemoryRunner(app=app)


async def main():
    try:
        # run_debug() requires ADK Python 1.18 or higher:
        response = await runner.run_debug("When was sales_data dataset last updated?")

    except Exception as e:
        logger.error("An error occurred during agent execution", exc_info=True)


if __name__ == "__main__":
    asyncio.run(main())
