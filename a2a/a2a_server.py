import logging
from pathlib import Path

from dotenv import load_dotenv
from strands_tools.calculator import calculator
from strands import Agent
from strands.multiagent.a2a import A2AServer

# Load AWS credentials from project root (required for Bedrock)
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

logging.basicConfig(level=logging.INFO)

# Create a Strands agent
strands_agent = Agent(
    name="Calculator Agent",
    description="A calculator agent that can perform basic arithmetic operations.",
    tools=[calculator],
    callback_handler=None
)

# Create A2A server (streaming enabled by default)
a2a_server = A2AServer(agent=strands_agent)

# Start the server
a2a_server.serve()